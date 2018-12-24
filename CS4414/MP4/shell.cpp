/*
 * Gabriel  Groover (gtg3vv)
 * HW4 - Simple Shell
 * Due: 3/17/2018
 * shell.cpp
 */
 
#include "shell.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/wait.h>

using namespace std;

//Split string into vector based on delim
vector<string> tokenize(string s, const char* delim) 
{
    vector<string> tokens;
    size_t start = 0;
    size_t loc = s.find(delim);
    
    //While delim in string
    while (loc != string::npos)
    {   
        //Add string from last delim to current to vector
        tokens.push_back(s.substr(start, loc-start));
        start = loc+strlen(delim);
        
        loc = s.find(delim, loc+1);
    }
    //Push remainder
    tokens.push_back(s.substr(start, s.length()));
    return tokens;
}

//Remove leading/trailing/doubled spaces
string removeSpace(string s)
{
    string oneSpace = "";
    bool afterSpace = true;    
    size_t lastLetter = s.find_last_not_of(" ");
    
    for (int i = 0; i < s.length(); i++)
    {
        //If repeated space, skip
        if (s[i] == ' ' && afterSpace)
           continue;

        afterSpace = s[i] == ' ';
        if (i <= lastLetter) oneSpace += s[i];
    }
    return oneSpace;
}

//Validate line
bool isValid(string inputLine)
{
    vector<string> groups = tokenize(inputLine, " | ");
    bool valid = true;
    
    //Iterate over token groups
    for (int i = 0; i < groups.size(); i++)
    {
        vector<string> tokens = tokenize(groups[i], " ");
        bool allow_operator = false; //Op allowed at position i
        bool allow_argument = true; //arg or command allowed at i
        bool foundIn = false; //found filein operator
        bool foundOut = false; //found fileout operator
        
        //Check leftover pipes
        if (groups[i].find_first_of("|") != string::npos)
            valid = false;
        
        
        //Iterate over tokens in group
        for (int j = 0; j < tokens.size(); j++)
        {
            if (tokens[j].find_first_of("<>") == string::npos)
            {
                if (allow_argument) allow_operator = true;
                else valid = false;
                
                allow_argument = !(foundIn || foundOut);
            }
            else
            {
                if (!allow_operator) //Operator at beginning or after other op
                    valid = false;
                else if (tokens[j].compare(">") != 0 && tokens[j].compare("<") != 0) //If extra chars around op
                    valid = false;
                else if (tokens[j].compare(">") == 0 && (!(i == groups.size()-1) || foundOut)) //If not last item or already found
                    valid = false;
                else if (tokens[j].compare("<") == 0 && (!(i == 0) || foundOut || foundIn)) //If not first item already found <>
                    valid = false;
                else
                {
                    allow_operator = false;
                    allow_argument = true;
                }
                
                foundIn = foundIn || (tokens[j].compare("<") == 0);
                foundOut = foundOut || (tokens[j].compare(">") == 0);
            }
        }
        //If never had file arg
        if (allow_argument && (foundIn || foundOut)) valid = false;
    }
    
    return valid;
    
}

//Main input loop
int main() {
    char temp[100];
    string cwd = string(getcwd(temp, 100));

    //Read input until eof
    while (true)
    {
        string inputLine;
        
        fflush(stdout);
        cout << ">";
        getline(cin, inputLine);
        
        if (inputLine.empty() || inputLine.compare("exit") == 0)
            return 0;
            
        inputLine = removeSpace(inputLine);
        
        //Validate input line
        if (inputLine.length() > 100)
        {
            cout << "invalid input" << endl;
            continue;
        }
        if (inputLine.find_first_not_of("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._/<>| ") != string::npos)
        {
            cout << "input input" << endl;
            continue;
        }
        if (!isValid(inputLine))
        {
            cout << "invalid input" << endl;
            continue;
        }
        
        vector<string> groups = tokenize(inputLine, " | ");
        vector<int> exitCodes;
        vector<string> commands;
        int pipes[(groups.size()-1)*2];
        int pids[groups.size()];
        int lastPid = -1;
        
        //Init pipes
        for (int i = 0; i < groups.size() - 1; i++)
        {
            pipe(&pipes[2*i]);
        }
        
        //Iterate over token groups
        for (int i = 0; i < groups.size(); i++)
        {
            //Fork child for command
            pids[i] = fork();
            if (pids[i] == 0)
            {
                //Find last argument index
                vector<string> tokens = tokenize(groups[i], " ");
                int countArgs = 0;
                for (int j = 0; j < tokens.size(); j++)
                {
                    if(tokens[j].find_first_of("<>") != string::npos)
                        break;
                    countArgs++;
                }
                
                string curCmd = tokens[0];
                //Add cwd if needed
                if (tokens[0][0] != '/')
                    tokens[0] = cwd + "/" + tokens[0];
                
                //Build argv
                char **argv = new char*[countArgs+1];
                for (int j = 0; j < countArgs; j++)
                {
                    char *temp = new char[tokens[j].length() + 1]; 
                    strcpy(temp, tokens[j].c_str());
                    argv[j] = temp;
                }
                argv[countArgs] = NULL;
                
                //Handle file redirects
                int infile, outfile;
                for (int j = countArgs; j < tokens.size(); j++)
                {
                    if (tokens[j].compare("<") == 0)
                    {
                        infile = open(tokens[++j].c_str(), O_RDONLY | O_NONBLOCK);
                        if (infile == -1)
                        {
                            fprintf(stderr, "Failed to open file for reading\n");
                            exit(1);
                        }
                        dup2(infile, 0);
                    }
                    else if (tokens[j].compare(">") == 0)
                    {
                        outfile = open(tokens[++j].c_str(), O_RDWR | O_CREAT, 0666);
                        if (outfile == -1)
                        {
                            fprintf(stderr, "Failed to open file for writing\n");
                            exit(1);
                        }
                        dup2(outfile, 1);
                    }
                }
                
                //Pipe to next process
                if (i == 0) //First
                {
                    close(pipes[2*i]);
                    dup2(pipes[2*i+1], 1);
                }
                else if (i != groups.size() - 1) //Middle
                {
                    close(pipes[2*(i-1)+1]);
                    close(pipes[2*i]);
                    dup2(pipes[2*(i-1)], 0);
                    dup2(pipes[2*i+1], 1);
                }
                else //Last
                {
                    close(pipes[2*(i-1)+1]);
                    dup2(pipes[2*(i-1)], 0);
                }
                
                //Handle exec or fail
                execv(tokens[0].c_str(), argv);
                fprintf(stderr,"Command %s failed to execute\n", curCmd.c_str());
                exit(1);
            } else
            {
                //Cleanup for parent
                commands.push_back(tokenize(groups[i]," ")[0]);
                if (i != 0)
                {
                    close(pipes[2*(i-1)]);
                    close(pipes[2*(i-1)+1]);
                }
            }
        }
        
        //Wait for each child
        for (int i = 0; i < commands.size(); i++)
        {
            
            int status;
            waitpid(pids[i], &status, 0);
            status = WEXITSTATUS(status);
            exitCodes.push_back(status);
        }
        
        //Print exit codes 
        for (int i = 0; i < commands.size(); i++)
        {
           fprintf(stderr, "%s exited with exit code %d\n", commands[i].c_str(), exitCodes[i]);
        }
    }
 
}

