#include "VoronoiDiagramGenerator.h"
#include <stdio.h>

extern "C"{
	struct VoronoiEdge{
		int id1;
		int id2;
		float x1;
		float y1;
		float x2;
		float y2;
	};

	void* createVoronoi(float *xValues, float *yValues, int count, \
			float minX, float maxX, float minY, float maxY){

		VoronoiDiagramGenerator* g(new VoronoiDiagramGenerator);
		g->generateVoronoi(xValues, yValues, count, \
				minX, maxX, minY, maxY);
		g->resetIterator();
		return g;
	}	

	
	bool getNextEdge(VoronoiDiagramGenerator *generator, VoronoiEdge* edge){
		return generator->getNext(edge->x1, edge->y1, edge->x2, edge->y2\
				, edge->id1, edge->id2)?1:0;
	}


	void freeVoronoi(VoronoiDiagramGenerator *generator){
		delete generator;
	}
};
