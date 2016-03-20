#include "VoronoiDiagramGenerator.h"
#include <stdio.h>

struct VoronoiEdge{
	int id1;
	int id2;
	float x1;
	float y1;
	float x2;
	float y2;
};


int main(){
	float x[] = {0, 0, 1, 1};
	float y[] = {0, 1, 0, 1};

	int count = 4;

	VoronoiDiagramGenerator g;
	g.generateVoronoi(x, y, count, -10, 10, -10, 10);
	g.resetIterator();

	VoronoiEdge edge;
	while(g.getNext(edge.x1, edge.y1, edge.x2, edge.y2\
				, edge.id1, edge.id2)){
		printf("%d %d: %f %f %f %f\n", edge.id1, edge.id2, edge.x1, edge.y1, \
				edge.x2, edge.y2);
	}
}
