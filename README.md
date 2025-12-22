# GeoIters

<img align="left" src="assets/banner.png">
A simple package for geospatial iterators.

## Installation

```bash
pip install geoiters
```

## Usage

```python
import geoiters
from geoiters.utils import Extent

ext = Extent(-74.0, 40.7, -73.9, 40.8, crs="EPSG:4326")
itr = geoiters.RowsAndColumns(ext, rows=10, columns=10)

for i, patch in enumerate(itr):
    print(i, patch)
```

## Features

- Efficient iteration over geospatial grids
- Lightweight and easy to use
