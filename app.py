from flask import Flask, render_template, request, flash
from carbon_calculator import CarbonCalculator
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import openrouteservice as ors
import os
from travel_suggestions import TravelSuggestions

app = Flask(__name__)

# secret keys 
app.secret_key = os.getenv('d9a2bd134c4e8129c765cd6808a3710b', 'e4d3855d5231e37ddcb0da95539cc587')

# OpenRouteService client
ors_client = ors.Client(key='5b3ce3597851110001cf624883d22606f1484088bffacfad3308b3d0') 

# Geopy geocoder
geolocator = Nominatim(user_agent="sustainable_travel_assistant")

def geocode_location(location_name):
    """
    Convert a location name (e.g., "New York, USA") into latitude and longitude using Geopy.
    Returns a tuple (lat, lon) or None if the location cannot be found.
    """
    try:
        location = geolocator.geocode(location_name)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        origin = request.form.get("origin")
        destination = request.form.get("destination")
        mode = request.form.get("mode")

        # Geocode origin and destination
        origin_coords = geocode_location(origin)
        destination_coords = geocode_location(destination)

        if not origin_coords:
            flash(f"Could not find coordinates for origin: {origin}", "error")
            return render_template("index.html")
        if not destination_coords:
            flash(f"Could not find coordinates for destination: {destination}", "error")
            return render_template("index.html")

        # Calculate distance based on mode
        if mode == "flight":
            # Use Geopy to calculate distance for flights
            distance_km = great_circle(origin_coords, destination_coords).km
            print("Flight Distance (km):", distance_km)  # Debug print
        elif mode == "car":
            # Use OpenRouteService to calculate driving distance
            try:
                coords = [
                    [origin_coords[1], origin_coords[0]],  # OpenRouteService expects [lon, lat]
                    [destination_coords[1], destination_coords[0]]
                ]
                route = ors_client.directions(coordinates=coords, profile='driving-car', format='geojson')
                distance_km = route['features'][0]['properties']['segments'][0]['distance'] / 1000
                print("Car Distance (km):", distance_km)  # Debug print
            except Exception as e:
                flash(f"Error calculating car distance: {str(e)}", "error")
                return render_template("index.html")
        else:
            # For train, assume the user inputs the distance manually
            try:
                distance_km = float(request.form.get("distance_km"))
                print("Train Distance (km):", distance_km)  # Debug print
            except ValueError:
                flash("Invalid distance input for train. Please enter a valid number.", "error")
                return render_template("index.html")

        # Debug: Print the calculated distance
        print("Final Distance (km):", distance_km)  # Debug print

        # Calculate carbon emissions,round to 2 decimal places
        emissions = round(CarbonCalculator.calculate_emissions(distance_km, mode), 2)

        # Debug: Print the calculated emissions
        print("Calculated Emissions (kg CO2):", emissions)  # Debug print

        # Automatically calculate the eco-friendly travel mode
        eco_mode = CarbonCalculator.suggest_eco_friendly_mode(distance_km)

        # Debug: Print the suggested eco-friendly mode
        print("Suggested Eco-Friendly Mode:", eco_mode)  # Debug print

        # Find tourist activities near the destination
        tourist_activities = TravelSuggestions.find_tourist_activities(destination)

        # Debug: Print the number of tourist activities found
        print("Number of Tourist Activities Found:", len(tourist_activities))  # Debug print

        return render_template(
            "results.html",
            emissions=emissions,
            eco_mode=eco_mode,
            tourist_activities=tourist_activities,
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)