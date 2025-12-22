"""Module defining the Extent class for geographic extents.
"""


class Extent(object):
    """
    Represents a geographic extent defined by its minimum and maximum coordinates.
    """

    def __init__(self, min_x: float, min_y: float, max_x: float, max_y: float, crs: str = None):
        """Initializes an Extent object.

        Args:
            min_x (float): Minimum x-coordinate (longitude).
            min_y (float): Minimum y-coordinate (latitude).
            max_x (float): Maximum x-coordinate (longitude).
            max_y (float): Maximum y-coordinate (latitude).
            crs (str, optional): Coordinate reference system. Defaults to None.
        """
        super().__init__()
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.crs = crs

    def __repr__(self):
        """Returns a string representation of the Extent object."""
        return f"Extent(min_x={self.min_x}, min_y={self.min_y}, max_x={self.max_x}, max_y={self.max_y}, crs={self.crs})"

    def copy(self) -> 'Extent':
        """Returns a copy of the Extent object."""
        return Extent(self.min_x, self.min_y, self.max_x, self.max_y, crs=self.crs)

    # def to_rasterio_window(self, transform) -> 'rasterio.windows.Window':
    #     from rasterio.windows import from_bounds
    #     window = from_bounds(*self.as_list(), transform)
    #     return window

    def to_box_coordinates(self) -> list:
        """Returns the extent as a list of a closed box coordinates.
        This first and last coordinate are the same to close the box.
        """
        return [
            [self.min_x, self.min_y],
            [self.max_x, self.min_y],
            [self.max_x, self.max_y],
            [self.min_x, self.max_y],
            [self.min_x, self.min_y],
        ]


WEB_MERCATOR_EXTENT = Extent(-20037508.342789244, -20037508.342789244, 20037508.342789244, 20037508.342789244, crs="EPSG:3857")
WORLD_EXTENT = Extent(-180, -90, 180, 90, crs="EPSG:4326")
