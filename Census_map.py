import pandas as pd # library for data analsysis
import json # library to handle JSON files
import geojson
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values
import requests # library to handle requests
import numpy as np
import folium # map rendering library
import streamlit as st
from streamlit_folium import folium_static
#------------------------------------------------

select_state = st.selectbox(
    "Select state",
    ("NSW", "VIC","QLD","WA","SA","TAS","ACT")
)

if select_state in ['WA','SA']:
    key = select_state.lower()+'_local_2'  
else:
    key = select_state.lower()+'_loca_2'

geojson_links = {
'NSW':r'GeoJson-Data-master\suburb-2-nsw.geojson'
,'QLD':r'GeoJson-Data-master\suburb-2-qld.geojson'
,'VIC':r'GeoJson-Data-master\suburb-2-vic.geojson'
,'WA':r'GeoJson-Data-master\suburb-2-wa.geojson'
,'SA':r'GeoJson-Data-master\suburb-2-sa.geojson'
,'TAS':r'GeoJson-Data-master\suburb-2-tas.geojson'
,'ACT':r'GeoJson-Data-master\suburb-2-act.geojson'
}

centre = {
'NSW':[-33.8696806,151.1872784]
,'QLD':[-27.4707241,153.0245904]
,'VIC':[-37.811262,144.9543962]
,'WA':[-31.943326,115.8353351]
,'SA':[-34.9256337,138.5657491]
,'TAS':[-42.8631354,147.3340212]
,'ACT':[-35.313899,148.9896991]
}

def my_color_function(feature):
    if feature['properties'].get('1st_Ancestry'):
        if feature['properties']['1st_Ancestry'] == 'Chinese':
            return '#ff0000'
        elif feature['properties']['1st_Ancestry'] == 'English':
            return '#086EA1'
        elif feature['properties']['1st_Ancestry'] == 'Turkish':
            return '#D28E1F'
        elif feature['properties']['1st_Ancestry'] == 'Italian':
            return '#B4EE1B'
        elif feature['properties']['1st_Ancestry'] == 'Filipino':
            return '#D2BC1F'
        elif feature['properties']['1st_Ancestry'] == 'French':
            return '#24D21F'
        elif feature['properties']['1st_Ancestry'] == 'German':
            return '#D21FA1'
        elif feature['properties']['1st_Ancestry'] == 'Greek':
            return '#1FAFD2'
        elif feature['properties']['1st_Ancestry'] == 'Indian':
            return '#5D3005'
        elif feature['properties']['1st_Ancestry'] == 'Korean':
            return '#D21F96'
        elif feature['properties']['1st_Ancestry'] == 'Lebanese':
            return '#7E1FD2'
        elif feature['properties']['1st_Ancestry'] == 'Maltese':
            return '#BFD21F'
        elif feature['properties']['1st_Ancestry'] == 'Vietnamese':
            return '#DE3C7C'
        else:
            return '#3DD21F'
    else:
        return '#3DD21F'

map = folium.Map(location=centre[select_state], zoom_start=11,width='100%',height='100%')
st.title('Ancestry by Postcode (2016 Census)')

with open(geojson_links[select_state]) as f:
    geo_json_data = geojson.load(f)

folium.GeoJson(
    geo_json_data,
    style_function=lambda feature: {
        'fillColor': my_color_function(feature),
        'color' : 'black',
        'weight' : 2,
        'dashArray' : '5, 5'
        }
    ).add_to(map)
# Add hover functionality.
style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
label = folium.GeoJson(
    geo_json_data,
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
        fields=[key,'1st_Ancestry_stat','2nd_Ancestry_stat','3rd_Ancestry_stat'],
        aliases=['Suburb: ','1st Ancestry: ', '2nd Ancestry: ','3rd Ancestry: '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 11px; padding: 5px;")
    )
)
map.add_child(label)
map.keep_in_front(label)
folium_static(map)

# st.text('Note: This chart is based on 2016 Census data in Australia. It is for research and entertaining purpose only. The author do NOT guarantee the accuracy of the results')
st.caption('This chart is based on 2016 Census data in Australia. It is for research and entertaining purpose only. The author do NOT guarantee the accuracy of the results.')

st.write("Contact the author: info@moneyrecreation.com")