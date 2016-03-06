#include <cmath>
#include <vector>
#include <stdio.h>


struct Point{
	Point(){}
	Point(double x, double y):
		x(x),
		y(y)
	{}
	double x;
	double y;
};

struct Line{
	Point p1;
	Point p2;

	Line(){}

	Line(Point p1, Point p2):
		p1(p1),
		p2(p2)
	{}
};


class Voronoi{
public:

	int getPointsCount(){
		return pointsCount;
	}

	int getLinesCount(int point){
		return lines[point].size();
	}

	double getLineP1X(int point, int lineId){
		return lines[point][lineId].p1.x;
	}
	double getLineP1Y(int point, int lineId){
		return lines[point][lineId].p1.y;
	}
	double getLineP2X(int point, int lineId){
		return lines[point][lineId].p2.x;
	}
	double getLineP2Y(int point, int lineId){
		return lines[point][lineId].p2.y;
	}

	int getNeighborsCount(int point){
		return neighbors[point].size();
	}
	int getNeighbor(int point, int id){
		return neighbors[point][id];
	}

	Voronoi(double *points, int pointsCount):
		points(points),
		pointsCount(pointsCount),
		lines(pointsCount),
		neighbors(pointsCount)
	{
		for(int i=0; i<pointsCount-1; ++i){
			for(int j=i+1; j<pointsCount; ++j){
				Line line;
				if(findLine(i, j, line)){
					// line exist
					neighbors[i].push_back(j);
					neighbors[j].push_back(i);
					lines[i].push_back(line);
					lines[j].push_back(line);
				}
			}
		}
	}

private:
	bool findLine(int p1, int p2, Line& line){
	/*
		find line between p1 and p2 in voronoi diagramm
		rezult stored in line
		return value determine is there any line at all
	*/
		separateLine(p1, p2, line);

		for(int k=0; k<pointsCount; ++k){
			if(k != p1 && k != p2){
				Line halfplane;
				separateLine(p1, k, halfplane);

				if(!reduceByHalfPlane(p1, halfplane, line)){
					return false;
				}
			}
		}
		return true;
	}

	bool reduceByHalfPlane(int p, const Line& halfplane, Line& line){
	/*
		line will remain only on the same halfplane (plane separated with line halfplane) as p
	*/
		Point point(x(p), y(p));

		bool p1OnPSide = pointsOnOneSide(halfplane, point, line.p1);
		bool p2OnPSide = pointsOnOneSide(halfplane, point, line.p2);

		if(p1OnPSide and p2OnPSide){
			return true;
		}else if(p1OnPSide != p2OnPSide){
			linesCross(halfplane, line, p2OnPSide);
			return true;
		}else{
			return false;
		}
	}

	bool pointsOnOneSide(const Line& line, const Point& p1, const Point& p2){
		double normX = line.p1.y - line.p2.y;
		double normY = line.p2.x - line.p1.x;

		double p1DotNorm = normX * p1.x + normY * p1.y;	
		double p2DotNorm = normX * p2.x + normY * p2.y;	
		double linePointDotNorm = normX * line.p1.x + normY * line.p1.y;	

		return (p1DotNorm - linePointDotNorm) * (p2DotNorm - linePointDotNorm) >= 0;
	}

	void separateLine(int p1, int p2, Line& line){
	/*
		create large line with equal distance to points

		p1 - first point id
		p2 - second point id

		line - there result stored
	*/
		double LIMIT = 1e8;

		double cx = (x(p1) + x(p2)) * 0.5;
		double cy = (y(p1) + y(p2)) * 0.5;

		// normal to line beween points
		double directionX = y(p1) - y(p2);
		double directionY = x(p2) - x(p1);

		double len = sqrt(directionX*directionX + directionY*directionY);
		double mul = LIMIT/len;
		directionX *= mul;
		directionY *= mul;

		line.p1.x = cx - directionX;
		line.p1.y = cy - directionY;

		line.p2.x = cx + directionX;
		line.p2.y = cy + directionY;
	}

	double x(int id){
		return points[id*2];
	}
	double y(int id){
		return points[id*2 + 1];
	}

	void linesCross(const Line& l1, Line& l2, bool changePoint){
	/*
		cut line l2 with l1.
		if changePoint cut from first point, in other case from second
	*/
		double cx = -l1.p1.x + l2.p1.x;
		double cy = -l1.p1.y + l2.p1.y;

		double x1 = l1.p2.x - l1.p1.x;
		double y1 = l1.p2.y - l1.p1.y;

		double x2 = l2.p2.x - l2.p1.x;
		double y2 = l2.p2.y - l2.p1.y;

		double t1 = (y2*cx - x2*cy) / (x1*y2 - x2*y1);
		
		if(changePoint){
			l2.p1.x = l1.p1.x + t1 * (l1.p2.x - l1.p1.x);
			l2.p1.y = l1.p1.y + t1 * (l1.p2.y - l1.p1.y);
		}else{
			l2.p2.x = l1.p1.x + t1 * (l1.p2.x - l1.p1.x);
			l2.p2.y = l1.p1.y + t1 * (l1.p2.y - l1.p1.y);
		}
	}

private:
	int pointsCount;
	double *points;

	std::vector<std::vector<Line> > lines;
	std::vector<std::vector<int> > neighbors;
};
