import time
import multiprocessing as mp
from geoiters.utils import Extent
from geoiters.grid import GridIterator



def worker(patch: Extent):
    time.sleep(1) # simulate a time-consuming task
    print(f"Worker {mp.current_process().name}: "
          f"Processing patch with extent {patch}")

def main():
    ext = Extent(-74.2, 40.65, -73.7, 40.85, crs="EPSG:4326")
    itr = GridIterator(ext, rows=4, columns=4)

    pool = mp.Pool(processes=4)

    t0 = time.perf_counter()
    pool.map(worker, itr)
    pool.close()
    pool.join()
    t1 = time.perf_counter()

    print(f"All patches have been processed in {t1 - t0:.2f} seconds.")

if __name__ == "__main__":
    main()
