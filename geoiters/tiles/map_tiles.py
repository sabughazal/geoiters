import math
from geoiters.utils import Extent
from geoiters.utils import haversine



class TilesIterator:
    def __init__(self, extent: Extent, zoom_level: int) -> None:
        """Iterator that yields tile coordinates (xtile, ytile, z) by dividing the given extent into tiles at the specified zoom level.

        Args:
            extent (Extent): The geographic extent to be divided into tiles.
            zoom_level (int): Zoom level for the tiles.
        """
        if zoom_level < 0 or zoom_level > 24:
            raise ValueError("zoom_level must be between 0 and 24.")

        self._extent = extent
        self._extent_coords = self._extent.transform_to("EPSG:4326")
        self._zoom_level = zoom_level

        self._xtile_min, self._ytile_max = self.coords_to_tile(self._extent_coords.min_y,
                                                   self._extent_coords.min_x, self._zoom_level)
        self._xtile_max, self._ytile_min = self.coords_to_tile(self._extent_coords.max_y,
                                                   self._extent_coords.max_x, self._zoom_level)

        self._width_in_tiles = self._xtile_max - self._xtile_min + 1
        self._height_in_tiles = self._ytile_max - self._ytile_min + 1

        self._current_row = 0
        self._current_column = 0

    def __iter__(self):
        return self

    def __next__(self) -> tuple:
        """Yields the next tile coordinates in the grid.

        Returns:
            tuple: (xtile, ytile, z) tile coordinates and zoom level.
        """
        xtile = self._current_column + self._xtile_min
        ytile = self._current_row + self._ytile_min
        z = self._zoom_level

        if self._current_row >= self._height_in_tiles:
            raise StopIteration

        self._current_column += 1
        if self._current_column >= self._width_in_tiles:
            self._current_column = 0
            self._current_row += 1

        return xtile, ytile, z

    @staticmethod
    def coords_to_tile(lat: float, lon: float, zoom: int):
        """Convert latitude and longitude to tile coordinates at a given zoom level."""
        lat_rad = math.radians(lat)
        n = 2.0 ** zoom
        xtile = int((lon + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
        return xtile, ytile
