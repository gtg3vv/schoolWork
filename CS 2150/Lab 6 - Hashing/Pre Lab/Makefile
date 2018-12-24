# Makefile for CS 2150 in-lab 5

CXX	= clang++

CXXFLAGS	= -lrt

OFILES	= wordPuzzle.o HashNode.o timer.o hashTable.o


.SUFFIXES: .o .cpp

main:	$(OFILES)
	$(CXX) $(CXXFLAGS) $(OFILES)
clean:
	/bin/rm -f *.o *~
wordPuzzle.o: wordPuzzle.cpp hashTable.h HashNode.h timer.h
HashNode.o: HashNode.cpp HashNode.h
hashTable.o: hashTable.cpp hashTable.h HashNode.h
timer.o: timer.cpp timer.h

