extern "C"{
	#include <stdio.h>

	struct CellColor{
		int triangleCount;
		int state;
	};

	const float ColorTable[][3] = {{0, 0, 0},
				       {.8, 0, 0},
			    	       {.3, .6, .6}};

	void reloadColors(const CellColor *array, int size, float *colors){
		int triangleId = 0;
		// for every cell
		for(int i=0; i<size; ++i){
			int state = array[i].state;
			// for every verticle
			for(int j=0; j<array[i].triangleCount * 3; ++j){ 
				int index = triangleId*3 + j;
				for(int k=0; k<3; ++k){
					colors[index*3 + k] = ColorTable[state][k];
				}
			}
			triangleId += array[i].triangleCount;
		}
	}

}
