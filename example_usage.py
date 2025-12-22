# %%
import geoiters
from geoiters.utils import Extent

try:
    import plotly.graph_objects as go
except ImportError:
    raise ImportError("This example requires plotly. Please install it via 'pip install plotly'.")



ext = Extent(-74.0, 40.7, -73.9, 40.8, crs="EPSG:4326")

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

# use the iterator to create patches
itr = geoiters.RowsAndColumns(ext, rows=10, columns=10)
for i, patch in enumerate(itr):
    patch_coords = patch.to_box_coordinates()
    lons, lats = zip(*patch_coords)

    fig.add_trace(go.Scattermapbox(
        mode="lines",
        lon=lons,
        lat=lats,
        line=dict(width=2, color='blue'),
        name=f"Patch {i+1}"
    ))

fig.update_layout(
    mapbox_style="open-street-map",
    mapbox=dict(center=dict(lat=40.75, lon=-73.95), zoom=10),
    margin={"r":0,"t":0,"l":0,"b":0}
)

fig.show()
