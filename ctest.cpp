#include "Voronoi.h"

#include <iostream>


int main(){
	double points[] =	{ 
						100.0, 100.0, 
						400.0, 100.0,
						100.0, 400.0
						};

	int count = 3;

	Voronoi vor(points, count);

	for(int i=0; i<count; ++i){
		std::cout << "- - - - - -\n\n";

		int lineCount = vor.getLinesCount(i);
		for(int j=0; j<lineCount; ++j){
			double p1x = vor.getLineP1X(i, j);
			double p1y = vor.getLineP1Y(i, j);
			double p2x = vor.getLineP2X(i, j);
			double p2y = vor.getLineP2Y(i, j);

			std::cout << "(" << p1x << ", " << p1y << ")";
			std::cout << ", (" << p2x << ", " << p2y << ")\n";
		}
	}
	return 0;
}
