"""Module defining the Extent class for geographic extents.
"""
import math
from .utils import haversine


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

    @property
    def area(self) -> float:
        """Calculates and returns the area of the extent in square meters."""
        ext = self.transform_to("EPSG:4326")
        width = haversine(ext.min_x, ext.min_y, ext.max_x, ext.min_y)
        height = haversine(ext.min_x, ext.min_y, ext.min_x, ext.max_y)
        return width * height

    def copy(self) -> 'Extent':
        """Returns a copy of the Extent object."""
        return Extent(self.min_x, self.min_y, self.max_x, self.max_y, crs=self.crs)

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

    def transform_to(self, target_crs: str) -> 'Extent':
        """
        Transforms the extent to a different coordinate reference system (CRS).
        Returns a new Extent object.
        """
        import pyproj

        if self.crs == target_crs:
            return self

        if self.crs is None:
            raise ValueError("Current CRS is not defined, cannot transform.")

        transformer = pyproj.Transformer.from_crs(self.crs, target_crs, always_xy=True)
        min_x, min_y = transformer.transform(self.min_x, self.min_y)
        max_x, max_y = transformer.transform(self.max_x, self.max_y)

        min_x, max_x = min(min_x, max_x), max(min_x, max_x)
        min_y, max_y = min(min_y, max_y), max(min_y, max_y)

        return Extent(min_x, min_y, max_x, max_y, crs=target_crs)

    def to_rasterio_bounds(self) -> 'rasterio.coords.BoundingBox':
        import rasterio
        return rasterio.coords.BoundingBox(self.min_x, self.min_y, self.max_x, self.max_y)

    def to_geometry(self) -> 'shapely.geometry.Polygon':
        from shapely.geometry import box
        geom = box(self.min_x, self.min_y, self.max_x, self.max_y)
        return geom

    def to_geojson(self) -> dict:
        import geojson
        geom = self.to_geometry()
        return geojson.Feature(geometry=geom, properties={})

    def as_list(self) -> list:
        """Returns the extent as a list of coordinates [min_x, min_y, max_x, max_y].

        Returns:
            list[float]: the list [min_x, min_y, max_x, max_y]
        """
        return [self.min_x, self.min_y, self.max_x, self.max_y]

    def as_dict(self) -> list:
        """Returns the extent as a list of coordinates [min_x, min_y, max_x, max_y].

        Returns:
            list[float]: the list [min_x, min_y, max_x, max_y]
        """
        return {
            "left": self.min_x,
            "bottom": self.min_y,
            "right": self.max_x,
            "top": self.max_y,
        }

    @staticmethod
    def from_rasterio_bounds(bounds: 'rasterio.coords.BoundingBox', crs: str = None) -> 'Extent':
        return Extent(bounds.left, bounds.bottom, bounds.right, bounds.top, crs=crs)

    @staticmethod
    def from_tile_coordinates(xtile: int, ytile: int, zoom: int) -> 'Extent':
        """Get the geographic extent of a tile given its x, y coordinates and zoom level.

        Args:
            xtile (int): X tile coordinate.
            ytile (int): Y tile coordinate.
            zoom (int): Zoom level.

        Returns:
            Extent: The geographic extent of the tile.
        """
        n = 2.0 ** zoom
        lon_min = xtile / n * 360.0 - 180.0
        lat_rad_max = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_max = math.degrees(lat_rad_max)
        lon_max = (xtile + 1) / n * 360.0 - 180.0
        lat_rad_min = math.atan(math.sinh(math.pi * (1 - 2 * (ytile + 1) / n)))
        lat_min = math.degrees(lat_rad_min)

        return Extent(lon_min, lat_min, lon_max, lat_max, crs="EPSG:4326")

    @staticmethod
    def from_string(bounds: str, crs: str = None) -> 'Extent':
        """Creates an Extent object from a string representation.

        Args:
            bounds (str): A string representation of the extent in the format "min_x,min_y,max_x,max_y".
            crs (str, optional): Coordinate reference system of the extent. Defaults to None.

        Raises:
            ValueError: If the input string does not contain exactly four comma-separated values.
        Returns:
            Extent: The created Extent object.
        """

        bounds_arr = [float(coord) for coord in bounds.split(',')]
        if len(bounds_arr) != 4:
            raise ValueError("Extent must contain exactly four values: left, bottom, right, top.")
        return Extent(bounds_arr[0], bounds_arr[1], bounds_arr[2], bounds_arr[3], crs=crs)


WEB_MERCATOR_EXTENT = Extent(-20037508.342789244, -20037508.342789244, 20037508.342789244, 20037508.342789244, crs="EPSG:3857")
WORLD_EXTENT = Extent(-180, -90, 180, 90, crs="EPSG:4326")
