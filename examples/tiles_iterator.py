# %%
from geoiters.utils import Extent
from geoiters.tiles import TilesIterator

try:
    import plotly.graph_objects as go
except ImportError:
    raise ImportError("This example requires plotly. Please install it via 'pip install plotly'.")



ext = Extent(-74.2, 40.65, -73.7, 40.85, crs="EPSG:4326")

square_coords = ext.to_box_coordinates()
lons, lats = zip(*square_coords)

fig = go.Figure()

fig.add_trace(go.Scattermapbox(
    mode="lines",
    lon=lons,
    lat=lats,
    line=dict(width=3, color='red'),
    name="Square"
))

# use the iterator
itr = TilesIterator(ext, zoom_level=13)
for i, (xtile, ytile, zoom) in enumerate(itr):
    patch = Extent.from_tile_coordinates(xtile, ytile, zoom) # just to be able to draw the tile as a box
    patch_coords = patch.to_box_coordinates()
    lons, lats = zip(*patch_coords)

    fig.add_trace(go.Scattermapbox(
        mode="lines",
        lon=lons,
        lat=lats,
        line=dict(width=1, color='black'),
        name=f"Tile {i+1}"
    ))
    print(f"Tile {i+1}, Area {patch.area:,.3f} sqm, {patch}")

fig.update_layout(
    mapbox_style="open-street-map",
    mapbox=dict(center=dict(lat=40.75, lon=-73.95), zoom=10),
    margin={"r":0,"t":0,"l":0,"b":0}
)

fig.show()
# %%
