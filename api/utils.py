"""
Helper functions
"""


def get_data_open_weather_api(response):
    """
    Given the open weather api data, return a dictionary of only the required data
    Format the wind direction into N/E/S/W
    Format the description to be title case for nice rendering in template
    """

    wind_deg = response["wind"]["deg"]
    if 45 < wind_deg <= 135:
        wind_direction = "E"  # East
    elif 135 < wind_deg <= 225:
        wind_direction = "S"  # South
    elif 225 < wind_deg <= 315:
        wind_direction = "W"  # West
    else:
        wind_direction = "N"  # North

    return {
        "description": response["weather"][0]["description"].title(),
        "icon": response["weather"][0]["icon"],
        "temp": response["main"]["temp"],
        "temp_min": response["main"]["temp_min"],
        "temp_max": response["main"]["temp_max"],
        "pressure": response["main"]["pressure"],
        "humidity": response["main"]["humidity"],
        "wind_speed": response["wind"]["speed"],
        "wind_direction": wind_direction,
    }
