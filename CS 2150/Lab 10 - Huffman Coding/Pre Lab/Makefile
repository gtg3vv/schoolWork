# Makefile
#Gabriel Groover (gtg3vv) Makefile

CXX	= clang++

OFILES	= heap.o huffmanenc.o huffNode.o


.SUFFIXES: .o .cpp

main:	$(OFILES)
	$(CXX) $(OFILES)
clean:
	/bin/rm -f *.o *~ 
huffmanenc.o: huffmanenc.cpp heap.h huffNode.h
heap.o: heap.cpp heap.h huffNode.h
huffNode.o: huffNode.cpp huffNode.h
