all: libvoronoi.so libreloadcolors.so


libvoronoi.so: Voronoi.cpp Voronoi.h
	g++ -c -fPIC Voronoi.cpp -o Voronoi.o -O2
	g++ -shared -Wl,-soname,libvoronoi.so -o libvoronoi.so Voronoi.o -O2

libreloadcolors.so: ColorReload.cpp
	g++ -c -fPIC ColorReload.cpp -o ColorReload.o -O2
	g++ -shared -Wl,-soname,libreloadcolors.so -o libreloadcolors.so ColorReload.o -O2
