#!/bin/bash
python3.4 -m cProfile -o voronoi.pyprof VoronoiRender.py
pyprof2calltree -i voronoi.pyprof -k
