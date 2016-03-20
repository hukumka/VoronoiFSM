CPPFLAGS=-fpermissive -fPIC

all: libvoronoi.so libreloadcolors.so

libvoronoi.so: Voronoi/Voronoi.o Voronoi/VoronoiDiagramGenerator.o
	g++ -shared -Wl,-soname,libvoronoi.so -o libvoronoi.so Voronoi/Voronoi.o Voronoi/VoronoiDiagramGenerator.o -O2

libreloadcolors.so: ColorReload.o
	g++ -shared -Wl,-soname,libreloadcolors.so -o libreloadcolors.so ColorReload.o -O2

clear:
	rm -rf libvoronoi.so libreloadcolors.so Voronoi/Voronoi.o Voronoi/VoronoiDiagramGenerator.o
