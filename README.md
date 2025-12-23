# GeoIters

<img align="left" src="assets/banner.png">
A simple package for geospatial iterators.

## Installation

```bash
pip install geoiters
```

## Usage

#### Grid by Rows and Columns
```python
from geoiters.grid import GridIterator
from geoiters.utils import Extent

ext = Extent(-74.2, 40.65, -73.7, 40.85, crs="EPSG:4326")
itr = GridIterator(ext, rows=10, columns=10)

for i, patch in enumerate(itr):
    print(i, patch)
```
See the complete example [here](examples/by_rows_and_columns.py).
<img style="margin-bottom: 1.5rem" align="left" src="assets/examples_standard.png">


#### Grid by Max Patch Area
```python
from geoiters.grid import GridIterator
from geoiters.utils import Extent

ext = Extent(-74.2, 40.65, -73.7, 40.85, crs="EPSG:4326")
itr = GridIterator(ext, patch_max_area=10_000_000) # area in sqm

for i, patch in enumerate(itr):
    print(i, patch)
```
See the complete example [here](examples/by_max_patch_area.py).
<img style="margin-bottom: 1.5rem" align="left" src="assets/example_by_area.png">


#### To Use with Multiprocessing
```python
import multiprocessing as mp
from geoiters.utils import Extent
from geoiters.grid import GridIterator

def worker(patch: Extent):
    time.sleep(1) # simulate a time-consuming task
    print(f"Worker {mp.current_process().name}: "
          f"Processing patch with extent {patch}")

ext = Extent(-74.2, 40.65, -73.7, 40.85, crs="EPSG:4326")
itr = GridIterator(ext, rows=4, columns=4) # area in sqm

pool = mp.Pool(processes=4)
pool.map(worker, itr)
pool.close()
pool.join()
```
See the complete example [here](examples/with_multiprocessing.py).


## Features
- Lightweight and easy to use.
- Efficient iteration over geospatial grids.
- Divide a geographical extent into patches and iterate through them.
- Divide a geographical extent by the number of rows and the number of columns.
- Divide a geographical extent by the maximum area of a single patch.

## To be Implemented
- Implement a hexagonal tessellation iterator.
- Implement a map tile iterator.
