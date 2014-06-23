great-circle-distance
=====================

Testing different ways in relational databases to calculate the distance between 2 latitude/longitude coordinates.

Timings and Results
---

### Time to find records near arbitrary lat/lon
|                     | Regular Haversine | Haversine precomputed radians | Straight Distance Formula | Postgres `earthdist`  |
| -------------       |:-------------:    | :-----:                       | :------:                  |:------:               |
| 10000 Records       | 13.2ms            | 8.66ms                        | 5.83ms                    | 2.00ms                |
| 100000 Records      | 99.5ms            | 81.1ms                        | 55.7ms                    | 2.55ms                |
| 1000000 Records     | 1190ms            | 821 ms                        | 575 ms                    | 8.10ms                |

### Number of records returned for arbitrary lat/lon
|                     | Regular Haversine | Haversine precomputed radians | Straight Distance Formula | Postgres `earthdist`  |
| -------------       |:-------------:    | :-----:                       | :------:                  |:------:               |
| 10000 Records       | 5                 | 5                             | 0                         | 8                     |
| 100000 Records      | 32                | 32                            | 9                         | 51                    |
| 1000000 Records     | 272               | 384                           | 135                       | 486                   |
