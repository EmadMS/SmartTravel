class CarbonCalculator:
   # Emission factors (in kg CO2 per km per passenger)
   EMISSION_FACTORS = {
       "flight": 0.18,  # Average for short-haul flights
       "train": 0.035,  # Average for electric trains
       "car": 0.12,     # Average for a petrol car
   }
   @staticmethod
   def calculate_emissions(distance_km, mode):
       """Calculate carbon emissions for a given travel mode."""
       if mode not in CarbonCalculator.EMISSION_FACTORS:
           raise ValueError(f"Unsupported travel mode: {mode}")
       return distance_km * CarbonCalculator.EMISSION_FACTORS[mode]
   @staticmethod
   def suggest_eco_friendly_mode(distance_km):
       """Suggest the most eco-friendly travel mode."""
       emissions = {
           mode: CarbonCalculator.calculate_emissions(distance_km, mode)
           for mode in CarbonCalculator.EMISSION_FACTORS
       }
       return min(emissions, key=emissions.get)