/*
 * Gabriel  Groover (gtg3vv)
 * HW4 - Simple Shell
 * Due: 3/17/2018
 * shell.h
 */
 
#ifndef SHELL_H
#define SHELL_H

//Included libraries
#include <string.h>
#include <iostream>
#include <vector>

//Methods
std::vector<std::string> tokenize(std::string s, const char* delim); //Split a string into a vector based on delim
std::string removeSpace(std::string s); //Trim whitespace from ends and remove double spaces
bool isValid(std::string inputLine); //Check if a given input line is a valid format

#endif