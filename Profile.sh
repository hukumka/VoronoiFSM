#!/bin/bash
python3.4 -m cProfile -o voronoi.pyprof Window.py
pyprof2calltree -i voronoi.pyprof -k
