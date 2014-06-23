great-circle-distance
=====================

Testing different ways in relational databases to calculate the distance between 2 latitude/longitude coordinates.

Timings and Results
---
1. Regular Haversine
  * Total number of results: 269
  * haversine function took 925.794 ms
2. Precomputed radian Haversine
  * Total number of results: 269
  * haversine_radians function took 828.921 ms
3. Straight Distance Formula
  * Total number of results: 269
  * straight_line function took 559.122 ms
