from .utils.extent import Extent



class RowsAndColumns:
    def __init__(self, extent: Extent, rows: int = 10, columns: int = 10) -> None:
        """Iterator that yields sub-extents by dividing the given extent into a grid of rows and columns.

        Args:
            extent (Extent): The geographic extent to be divided.
            rows (int, optional): Number of rows to divide the extent into. Defaults to 10.
            columns (int, optional): Number of columns to divide the extent into. Defaults to 10.
        """
        if rows <= 0:
            raise ValueError("Rows must be a positive integer larger than zero.")
        if columns <= 0:
            raise ValueError("Columns must be a positive integer larger than zero.")

        self._extent = extent
        self._rows = rows
        self._columns = columns

        self._cell_width = (extent.max_x - extent.min_x) / columns
        self._cell_height = (extent.max_y - extent.min_y) / rows

        self._current_row = 0
        self._current_column = 0

    def __iter__(self):
        return self

    def __next__(self) -> Extent:
        """Yields the next sub-extent in the grid.

        Returns:
            Extent: The next sub-extent.
        """
        min_x = self._extent.min_x + self._current_column * self._cell_width
        max_x = min_x + self._cell_width
        min_y = self._extent.min_y + self._current_row * self._cell_height
        max_y = min_y + self._cell_height

        ext = Extent(min_x, min_y, max_x, max_y, crs=self._extent.crs)

        if self._current_row >= self._rows:
            raise StopIteration

        self._current_column += 1
        if self._current_column >= self._columns:
            self._current_column = 0
            self._current_row += 1

        return ext
