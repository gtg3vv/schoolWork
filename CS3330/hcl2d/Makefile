YAS=./tools/yas
HCL2D=./tools/hcl2d
DC=dmd
DFLAGS=-O
DOT=dot

all:
	(cd tools; make all)

.SUFFIXES: .ys .yo
.ys.yo:
	$(YAS) $*.ys

.SUFFIXES: .hcl .exe
.hcl.exe:
	$(HCL2D) $*.hcl
	$(DC) $(DFLAGS) $*_hcl.d -of$*.exe

.SUFFIXES: .dot .png
.dot.png: 
	$(DOT) -Tpng $*.dot > $*.png

clean:
	(cd tools; make clean)
	rm -f *.exe *.o *.obj *~ core.* *_hcl.d *_hcl.dot *_hcl.png

archive:
	tar -cvf hcl2d.tar --xform 's!^.!hcl2d!' --exclude hcl2d.tar --exclude=hcl2d-not-permissive.d --exclude=*.o --exclude=yis --exclude=yas --exclude-vcs --exclude=hcl2d --exclude=tests .

.PHONY: all clean archive	
