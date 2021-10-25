import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(location=[45.06, 24.35], zoom_start=6, titles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes")
for coordinates in [[45.134300, 24.084313], [45.075182, 24.217967]]:
    fgv.add_child(folium.CircleMarker(radius = 6, location=coordinates, popup="Bita's House", color='grey', fill_color = 'green', fill_opacity=0.7))

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(radius = 6, location=[lt, ln], popup=folium.Popup(iframe), color= 'grey',fill_color = color_producer(el), fill_opacity=0.7))

fgp = folium.FeatureGroup(name='Population')
fgp.add_child(folium.GeoJson(data=open('world.json', mode='r', encoding='utf-8-sig').read(), style_function=lambda x: {'fillColor':'green' if
x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")
