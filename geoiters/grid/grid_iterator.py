import math
from geoiters.utils import Extent
from geoiters.utils import haversine



class GridIterator:
    def __init__(self, extent: Extent, rows: int = 10, columns: int = 10, patch_max_area: float = None) -> None:
        """Iterator that yields sub-extents by dividing the given extent into a grid of rows and columns.

        Args:
            extent (Extent): The geographic extent to be divided.
            rows (int, optional): Number of rows to divide the extent into. Defaults to 10.
            columns (int, optional): Number of columns to divide the extent into. Defaults to 10.
            patch_max_area (float, optional): Maximum area for each patch. If this is given,
            the grid will be calculated based on this area and the `rows` and `columns` arguments
            will be ignored. Defaults to None.
        """
        if rows <= 0:
            raise ValueError("Rows must be a positive integer larger than zero.")
        if columns <= 0:
            raise ValueError("Columns must be a positive integer larger than zero.")
        if extent.crs is None:
            raise ValueError("Extent must have a defined CRS.")

        self._patch_max_area = patch_max_area
        self._extent = extent
        self._extent_coords = self._extent.transform_to("EPSG:4326")
        # self._extent_meters = self._extent.transform_to("EPSG:3857")

        if patch_max_area == None:
            self._rows = rows
            self._columns = columns

        elif self._patch_max_area > 0:
            x_meters = haversine(self._extent_coords.min_x, self._extent_coords.min_y,
                                self._extent_coords.max_x, self._extent_coords.min_y)
            y_meters = haversine(self._extent_coords.min_x, self._extent_coords.min_y,
                                self._extent_coords.min_x, self._extent_coords.max_y)
            patch_width_meters = self._patch_max_area ** 0.5
            patch_height_meters = patch_width_meters
            self._rows = math.ceil(y_meters / patch_height_meters)
            self._columns = math.ceil(x_meters / patch_width_meters)

        elif patch_max_area <= 0:
            raise ValueError("patch_max_area must be a positive float larger than zero.")

        # the patch width and height should be in the original CRS units
        self._x_delta = (self._extent.max_x - self._extent.min_x) / self._columns
        self._y_delta = (self._extent.max_y - self._extent.min_y) / self._rows

        self._current_row = 0
        self._current_column = 0

    def __iter__(self):
        return self

    def __next__(self) -> Extent:
        """Yields the next sub-extent in the grid.

        Returns:
            Extent: The next sub-extent.
        """
        min_x = self._extent.min_x + self._current_column * self._x_delta
        max_x = min_x + self._x_delta
        min_y = self._extent.min_y + self._current_row * self._y_delta
        max_y = min_y + self._y_delta

        ext = Extent(min_x, min_y, max_x, max_y, crs=self._extent.crs)

        if self._current_row >= self._rows:
            raise StopIteration

        self._current_column += 1
        if self._current_column >= self._columns:
            self._current_column = 0
            self._current_row += 1

        return ext
