# VoronoiCWrap
g++ -c -fPIC Voronoi.cpp -o Voronoi.o -O2
g++ -shared -Wl,-soname,libvoronoi.so -o libvoronoi.so Voronoi.o -O2

# reloadColors for VoronoiRender
g++ -c -fPIC Voronoi.cpp -o Voronoi.o -O2
g++ -shared -Wl,-soname,libvoronoi.so -o libvoronoi.so Voronoi.o -O2
