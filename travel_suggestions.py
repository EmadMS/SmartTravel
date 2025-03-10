import requests

class TravelSuggestions:
    # OpenTripMap API key 
    OPENTRIPMAP_API_KEY = "5ae2e3f221c38a28845f05b69fa00559c50dcf59509b52317b928005"

    @staticmethod
    def find_tourist_activities(location, radius=5000, limit=10):
        """
        Find tourist activities near a location using OpenTripMap.
        Returns only the top `limit` activities.
        """
        try:
            # Geocode the location to get coordinates
            geocode_url = "https://api.opentripmap.com/0.1/en/places/geoname"
            geocode_params = {
                "name": location,
                "apikey": TravelSuggestions.OPENTRIPMAP_API_KEY,
            }
            geocode_response = requests.get(geocode_url, params=geocode_params).json()

            # Debug: Print the geocode response
            print("Geocode Response:", geocode_response)  # Debug print

            if not geocode_response:
                print("Geocode failed for location:", location)  # Debug print
                return []

            # Get coordinates from geocode response
            lat = geocode_response["lat"]
            lon = geocode_response["lon"]

            # Search for tourist activities using OpenTripMap
            activities_url = "https://api.opentripmap.com/0.1/en/places/radius"
            activities_params = {
                "radius": radius,  # Search radius in meters
                "lat": lat,
                "lon": lon,
                "format": "json",
                "apikey": TravelSuggestions.OPENTRIPMAP_API_KEY,
            }
            activities_response = requests.get(activities_url, params=activities_params).json()

            # Debug: Print the activities response
            print("OpenTripMap Activities Response:", activities_response)  # Debug print

            # Return only the top `limit` activities
            return activities_response[:limit]
        except Exception as e:
            print(f"Error finding tourist activities: {e}")
            return []