#include "Voronoi.h"


extern "C"{
	void* generateVoronoi(double *points, int pointsCount){
		return new Voronoi(points, pointsCount);
	}

	void freeVoronoi(Voronoi *obj){
		delete obj;
	}

	double getLineP1X(Voronoi *obj, int point, int line){
		return obj->getLineP1X(point, line);
	}
	double getLineP1Y(Voronoi *obj, int point, int line){
		return obj->getLineP1Y(point, line);
	}
	double getLineP2X(Voronoi *obj, int point, int line){
		return obj->getLineP2X(point, line);
	}
	double getLineP2Y(Voronoi *obj, int point, int line){
		return obj->getLineP2Y(point, line);
	}

	int getLinesCount(Voronoi *obj, int point){
		return obj->getLinesCount(point);
	}

	int getNeighborsCount(Voronoi *obj, int point){
		return obj->getNeighborsCount(point);
	}

	int getNeighbor(Voronoi *obj, int point, int id){
		return obj->getNeighbor(point, id);
	}
}
