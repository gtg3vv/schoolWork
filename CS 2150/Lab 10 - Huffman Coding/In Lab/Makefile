# Makefile
#Gabriel Groover (gtg3vv) Makefile

CXX	= clang++

OFILES	= huffmandec.o huffNode.o


.SUFFIXES: .o .cpp

main:	$(OFILES)
	$(CXX) $(OFILES)
clean:
	/bin/rm -f *.o *~ 

huffmandec.o: huffmandec.cpp huffNode.h
huffNode.o: huffNode.cpp huffNode.h
