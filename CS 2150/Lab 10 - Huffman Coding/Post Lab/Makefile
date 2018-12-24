# Makefile
#Gabriel Groover (gtg3vv) Makefile

CXX	= clang++

OFILES	= huffmandec.o huffNode.o
OFILES2 = huffmanenc.o huffNode.o heap.o 
OUTPUT1 = -o encoder
OUTPUT2 = -o decoder


.SUFFIXES: .o .cpp

main:	$(OFILES) $(OFILES2)
	$(CXX) $(OFILES2) $(OUTPUT1)
	$(CXX) $(OFILES) $(OUTPUT2)
clean:
	/bin/rm -f *.o *~ 


