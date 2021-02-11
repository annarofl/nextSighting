import geopandas
import geopy
import pandas as pd
from geopy.extra.rate_limiter import RateLimiter
import folium
import folium.plugins as plugins


def pull_address_list(filename="address.csv"):

    df = pd.read_csv(filename)

    # convert address columns to type string to concat them
    address_columns = ['Address1', 'Address2', 'City', 'State', 'Zip', 'country']

    df[address_columns] = df[address_columns].fillna('').astype(str)

    df['ADDRESS'] = df[address_columns].agg(', '.join, axis=1)

    return df


def convert_lon_lat(df):
    locator = geopy.Nominatim(user_agent="myGeocoder")

    # convenient function to delay between geocoding calls
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

    df['location'] = df['ADDRESS'].apply(geocode)
    # 3 - create longitude, latitude and altitude from location column (returns tuple)
    df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
    df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)

    return df


def visualize_locations(df):

    folium_map = folium.Map(location=[30.1690815, -97.83705505214803],
                            zoom_start=1,  #the world
                            tiles='CartoDB dark_matter')

    plugins.FastMarkerCluster(data=list(zip(df['latitude'].values, df['longitude'].values))).add_to(folium_map)
    folium.LayerControl().add_to(folium_map)
    folium_map.save("loc.html")
