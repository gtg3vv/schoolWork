/*
 * Gabriel  Groover (gtg3vv)
 * HW1 - FileSystem  Read API
 * 
 */

//User head files
#include "myfat.h"

//C++ libraries
#include <stdio.h>
#include <iostream>
#include <cstdlib>
#include <cmath>
#include <queue> 
#include <locale>
#include <algorithm>

//Sys call dependent includes
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <string.h>

//Initialize file system from boot block
void initFS()
{
  const char *path = std::getenv("FAT_FS_PATH");
  fatFd = open(path, O_RDONLY);
  lseek(fatFd,0,SEEK_SET);
  bB = (bpbFat32*) malloc(sizeof(bpbFat32));
  read(fatFd, bB, sizeof(bpbFat32));  
  calcRootDir();
}

//Calculate Root Dir location and initalize other boot block parameters
void calcRootDir()
{
  RootDirSectors = round(((bB->bpb_rootEntCnt * 32) + (bB->bpb_bytesPerSec - 1)) / bB->bpb_bytesPerSec);
  
  clusSize = bB->bpb_secPerClus * bB->bpb_bytesPerSec;
  
  //Determine FAT size
  uint32_t FATSz;
  if (bB->bpb_FATSz16 != 0)
    FATSz = bB->bpb_FATSz16;
  else
    FATSz = bB->bpb_FATSz32;
  
  //Locate beginning of data
  FirstDataSector = bB->bpb_rsvdSecCnt + (bB->bpb_numFATs * FATSz) + RootDirSectors;
  
  //FAT Type Determination
  uint32_t TotSec;
  if (bB->bpb_totSec16 != 0)
    TotSec = bB->bpb_totSec16;
  else
    TotSec = bB->bpb_totSec32;
  
  uint32_t DataSec = TotSec - (bB->bpb_rsvdSecCnt + (bB->bpb_numFATs * FATSz) + RootDirSectors);
  uint32_t CountofClusters = floor(DataSec / bB->bpb_secPerClus);
  if (CountofClusters < 4085) {/* FAT 12 */}
  else if (CountofClusters < 65525) {
    std::cout << "Volume is fat16" << std::endl;
    fatType = 16;
  }
  else {
    std::cout << "Volume is fat32" << std::endl;
    fatType = 32;
  }
  
  //Initialize Values based  on fat type
  if (fatType == 16)
  {
    rootClusNum = 2;
    eofVal = 0xFFF8;
    badClus = 0xFFF7;
    
    //Calculate root cluster based on offset from cluster formula
    int rootOffset = (FirstDataSector - RootDirSectors) * bB->bpb_bytesPerSec;
    int clusOffset = (((-2) * bB->bpb_secPerClus) + FirstDataSector) * bB->bpb_bytesPerSec;
    rootClusNum = (rootOffset - clusOffset) / clusSize;
  } else if (fatType == 32)
  {
    rootClusNum = bB->bpb_RootClus;
    eofVal = 0x0FFFFFF8;
    badClus = 0x0FFFFFF7;
  }
  
  //Set default path to root dir
  cwdPath = (char*) malloc(2);
  cwdPath[0] = '/';
  cwdPath[1] = '\0';
}

//Read a single directory from a path
dirEnt * OS_readDir(const char *dirname)
{ 
  //Check initialization
  if (!initialized)
  {
    initFS(); 
    initialized = true;
  }
  
  std::string pathName(dirname);
  std::string desiredEntry = getNextPathName(pathName);
  uint32_t currentClus = rootClusNum;
  bool hasNextCluster = true;
  bool endOfDirectory = false;
  bool rootDir = false;
  
  //Check for relative path and add cwd if necessary
  if (dirname[0] != '/')
  {
    if (!cwdPath)
      return nullptr;
    
    std::string currentPath(cwdPath);
    if (currentPath[currentPath.size()-1] != '/')
      pathName.insert(0, "/");
    pathName.insert(0,  currentPath);
    return OS_readDir(pathName.c_str());
    
  } else if (stringCompare(pathName, "/") != 1)
      pathName = pathName.substr(desiredEntry.size()+1,pathName.size());
  else 
    rootDir = true;
  
  //Continue iterating until reached the end of a directory
  while (hasNextCluster && !endOfDirectory)
  {
    dirEnt *dir = (dirEnt*) malloc(clusSize);
    lseek(fatFd, (((currentClus - 2) * bB->bpb_secPerClus) + FirstDataSector) * bB->bpb_bytesPerSec , SEEK_SET);
    read(fatFd, dir, clusSize);     
    
    hasNextCluster = getFATEntry(currentClus) < eofVal;
    currentClus = getFATEntry(currentClus);

    //std::cout << desiredEntry << " " <<  pathName << std::endl;
    
    for (int i = 0; i < 64; i ++)
    {
      std::string entryName = strip(dir[i].dir_name);
      //std::cout << entryName << std::endl;      
    
      //End of directory marker
      if (dir[i].dir_name[0] == 0)
      {
	//entry not found
	endOfDirectory = true;	

	if (rootDir)
	  return dir;
	free(dir);
	return nullptr;
	break;
      }
      //If found desired entry and it is actually a directory
      if (stringCompare(entryName,desiredEntry) == 1 && (dir[i].dir_attr & 0x10))
      {
	  std::cout << "Located " << desiredEntry << std::endl;
	  
	  unsigned int highWord = (unsigned int) dir[i].dir_fstClusHI << 16;
	  unsigned int lowWord = (unsigned int) dir[i].dir_fstClusLO;
	  
	  currentClus = highWord | lowWord;
	  hasNextCluster = true;
	  
	  //Check root .. case
	  if (currentClus == 0)
	    currentClus = rootClusNum;
	  
	  //If path complete, return directory pointer
	  if (pathName.size() <= 0 || (pathName.size() == 1  && pathName[0] == '/'))
	  {
	    free(dir);
	    return readClusForCurrentDir(currentClus);
	  }
	  
	  desiredEntry = getNextPathName(pathName);
	  pathName = pathName.substr(desiredEntry.size()+1,pathName.size());
	 break;
      }
    }
    
    free(dir);
   }
   return nullptr;
}

//Handle reading clusters for final return
dirEnt * readClusForCurrentDir(uint32_t startClus)
{
    std::queue<uint32_t> clusters;
    clusters.push(startClus);
    
    //Add all clusters for current directory to queue
    while (getFATEntry(startClus) < eofVal)
    {
      startClus = getFATEntry(startClus);
      clusters.push(startClus);
    }
    
    //Read each cluster from queue into dir*
    unsigned int clusCount = clusters.size();
    dirEnt *dir = (dirEnt*) malloc(clusCount * clusSize);
    unsigned int dirOffset = 0;
    while (!clusters.empty())
    {
      uint32_t offset = (((clusters.front() - 2) * bB->bpb_secPerClus) + FirstDataSector) * bB->bpb_bytesPerSec;
      clusters.pop();
     
      lseek(fatFd, offset , SEEK_SET);
      read(fatFd, dir + dirOffset, clusSize);   
      dirOffset += clusSize;
    }
   
    return dir;    
}


int OS_open(const char* path)
{
  //Check initialization
  if (!initialized)
  {
    initFS(); 
    initialized = true;
  }
  
  //extract filename from path
  std::string s(path);
  if (s[s.size()-1] == '/')
    s = s.substr(0, s.size()-1);
  size_t lastDelim = s.find_last_of('/');
  std::string fileName;
  if (lastDelim != std::string::npos)
    fileName = s.substr(lastDelim+1, s.size());
  else fileName = s;
  
  char pathSlice[lastDelim+2];
  strncpy(pathSlice, path, lastDelim+1);
  pathSlice[lastDelim+1] = '\0';
  
  //std::cout << pathSlice << " " << fileName  << std::endl;
  
  //If directory exists, search it for file
  dirEnt* dir;
  dir = OS_readDir(pathSlice);
  if (dir)
  { 	
    int i = 0;
    while (1)
    {
      std::string entryName = strip(dir[i].dir_name);
      //std::cout << entryName << "#" << std::endl;
  
      //End of directory marker found
      if (dir[i].dir_name[0] == 0)
      {
	//entry not found	
	std::cout << "last entry in directory" << std::endl;
	return -1;
	break;
      }
      //Found entry matching  filename that isnt directory
      if (stringCompare(entryName,fileName) == 1 && !(dir[i].dir_attr & 0x10))
      {
	std::cout << "Located " << fileName << std::endl;
	
	unsigned int highWord = (unsigned int) dir[i].dir_fstClusHI << 16;
	unsigned int lowWord = (unsigned int) dir[i].dir_fstClusLO;
	unsigned int fileCluster = highWord | lowWord;
	
	//Check file table for open space
	for (int j = 0; j < 127; j ++)
	{
	  if (fileTable[j] == 0)
	  {
	    fileTable[j] = fileCluster;
	    return j;
	  }
	}
	return -1;
      }
      i++;
    }
  } 
  return -1;
}

//Read from an open file
int OS_read(int fildes, void *buf, int nbyte, int offset)
{
  //Handle Initialization
  if (!initialized)
  {
    initFS(); 
    initialized = true;
  }
  //Check to see file is actually open
  if (fildes < 0 || fildes > 127 || fileTable[fildes] == 0)
    return -1;
  
  //Determine offset from start cluster of file
  unsigned int startClus = offset / clusSize;
  unsigned int currentClus = fileTable[fildes];
  int bytesRead = 0;
  int bytesLeft = nbyte;
  
  //Iterate clusters to correct part of file
  while (startClus > 0)
  {
    currentClus = getFATEntry(currentClus);
    if (currentClus >= eofVal)
      return -1;
    startClus--;
  }
  
  //Check to see if there is enough space in the cluster to read remaining bytes
  offset = offset % clusSize;
  lseek(fatFd, ((((currentClus - 2) * bB->bpb_secPerClus) + FirstDataSector) * bB->bpb_bytesPerSec) + offset , SEEK_SET);
  if (clusSize - offset > bytesLeft)
  {
    read(fatFd, buf, nbyte); 
    return nbyte;
  } 
  else
  {
    read(fatFd, buf, clusSize - offset);
    bytesRead = clusSize - offset;
    bytesLeft -= bytesRead;
    currentClus = getFATEntry(currentClus);
  }
  
  //Continue reading next cluster until all bytes read, or end of file reached
  while(bytesLeft > 0)
  {
    if (currentClus >= eofVal)
      return bytesRead;
    
    lseek(fatFd, ((((currentClus - 2) * bB->bpb_secPerClus) + FirstDataSector) * bB->bpb_bytesPerSec), SEEK_SET);
    if (bytesLeft >= clusSize)
    {
      read(fatFd, buf+bytesRead, clusSize);
      bytesLeft -= clusSize;
      bytesRead += clusSize;
    } else
    {
      read(fatFd, buf+bytesRead, bytesLeft);
      bytesLeft -= bytesLeft;
      bytesRead += bytesLeft;
    }
  }
  return bytesRead;
}

//Close an existing file descriptor
int OS_close(int fd) 
{
  //Check initialization
  if (!initialized)
  {
    initFS(); 
    initialized = true;
  }
  
  //Close file if it exists
  if (fileTable[fd] != 0)
  {
    fileTable[fd] = 0;
    return 1;
  } else
    return -1;
}

//Compare filesystem name (s1) to user supplied path (s2)
int stringCompare(std::string s1, std::string s2)
{
  //Remove . if not relative path, uppercase all dirent names
  s1.erase(std::remove(s1.begin(), s1.end(), ' '), s1.end());
  if (s2[0] != '.')
    s2.erase(std::remove(s2.begin(), s2.end(), '.'), s2.end());
  
  std::locale loc;
  
  //Compare sizes and check remaining chars for equality
  if (s1.size() != s2.size()) 
    return -1;
  for (int i = 0; i < s1.size(); i++)
  {
    if (std::toupper(s2[i],loc) != s1[i])
      return -1;
  }
  return 1;
}

//Change current working directory to path
int OS_cd(const char *path)
{
  //Check initialization
  if (!initialized)
  {
    initFS(); 
    initialized = true;
  }
  
  //Check directory exists
  void* dir = OS_readDir(path);
  if (dir)
  {
    free(dir);
    //Check if path  is absolute and ovewrite cwd
    if (path[0] == '/')
    {
      if (cwdPath)
	free(cwdPath);
      cwdPath = (char*) malloc(strlen(path)+1);
      strcpy(cwdPath, path);
      cwdPath[strlen(path)] = '\0';
      
      std::cout << "New Working Dir: " << cwdPath << std::endl;
      return 1;
    }
    //If path is relative, append to end of cwdPath
    else
    {
      if (!cwdPath)
	return -1;
      //Add trailing  / to cwdPath
      if (cwdPath[strlen(cwdPath)-1] != '/')
      {
	char* tempPath = (char*) malloc(strlen(path) + strlen(cwdPath) + 2);
	strcpy(tempPath+strlen(cwdPath)+1, path);
	strcpy(tempPath, cwdPath);
	tempPath[strlen(cwdPath)] = '/';
	tempPath[strlen(path) + strlen(cwdPath) + 1] = '\0';
	
	free(cwdPath);
	cwdPath = tempPath;
	std::cout << "New Working Dir: " << cwdPath << std::endl;
	return 1;
      }
      //cwdPath already has trailing /
      else
      {
	char* tempPath = (char*) malloc(strlen(path) + strlen(cwdPath) + 1);
	strcpy(tempPath, cwdPath);
	strcpy(tempPath+strlen(cwdPath), path);
	tempPath[strlen(path) + strlen(cwdPath)] = '\0';
	
	free(cwdPath);
	cwdPath = tempPath;
	std::cout << "New Working Dir: " << cwdPath << std::endl;
	return 1;
      }
    } 
    return 1;
  } else return -1;
}

//Get next / delimited element of path
std::string getNextPathName(const std::string& s)
{
  size_t firstDelim = s.find_first_of('/');
  size_t nextDelim = s.find_first_of('/',firstDelim+1);
  if (nextDelim == std::string::npos)
    return s.substr(firstDelim+1, s.size() - firstDelim);
  return s.substr(firstDelim+1, nextDelim - firstDelim - 1);
}


//Remove trailing  whitespace
std::string strip(uint8_t* dirName)
{ 
  char* str;
  for (int i = 10; i >= 0; i--)
  {
    if (dirName[i] != 32)
    {
      str = (char*) malloc(i+2);
      strncpy(str, (const char*)dirName, i+1);
      str[i+1] = 0;
      break;
    }
  } 
  std::string s(str);
  free(str);
   
  return s;
}


//Get entry in fat table for a given index
unsigned int getFATEntry(int n)
{
  //Fat offset determination
  uint32_t fatoffset;
  if (fatType == 16)
    fatoffset = n * 2;
  else
    fatoffset = n * 4;
  
  uint32_t fatSecNum = bB->bpb_rsvdSecCnt + (fatoffset / bB->bpb_bytesPerSec);
  uint32_t fatEntOffset = fatoffset % bB->bpb_bytesPerSec;
  
  //Read fat entry
  lseek(fatFd, fatSecNum * bB->bpb_bytesPerSec ,SEEK_SET);
  unsigned char buffer[bB->bpb_bytesPerSec];
  read(fatFd, buffer, bB->bpb_bytesPerSec); 
  
  //fat 16 extraction
  if (fatType == 16)
    unsigned short table_value = *(unsigned short*) &buffer[fatEntOffset];
  //fat 32 extraction
  else
    unsigned int table_value = *(unsigned int*) &buffer[fatEntOffset] & 0x0FFFFFFF;
}

//Pre-defined functions

int OS_rmdir(const char *path)
{
  return 1;
}
int OS_mkdir(const char *path)
{
  return 1;
}
int OS_rm(const char *path)
{
  return 1;
}
int OS_creat(const char *path)
{
  return 1;
}
int OS_write(int fildes, const void *buf, int nbyte, int offset)
{
  return 1;
}

