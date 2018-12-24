%.o: %.cpp 
	g++ -fPIC -std=gnu++0x -c $< -o $@
libFAT.so: fatdriver.o
	g++ -shared $^ -o $@
clean:
	rm -f *.o *.so a.out