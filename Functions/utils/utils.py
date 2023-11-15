from datetime import datetime
from geopy.geocoders import Nominatim

def get_iso_datetime(datetime_obj, input_format):
    print(datetime_obj)
    # input_format = "%B %d, %Y %H:%M IST"
    output_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    try:
        return datetime.strptime(datetime_obj, input_format).strftime(output_format)
    except:
        input_format = "%d-%m-%Y at %H:%M IST"
        return datetime.strptime(datetime_obj, input_format).strftime(output_format)
    
def get_country(city):
    geolocator = Nominatim(user_agent="city-to-country")
    try:
        location = str(geolocator.geocode(city))
    except:
        return "" #If API is down
    # print(type(location))
    if location:
        return location.split(", ")[-1]
    return ""

# print(get_country("pune"))
# print(get_iso_datetime("September 24, 2023 02:38 pm", "%B %d, %Y %I:%M %p"))