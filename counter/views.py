from django.shortcuts import render
import json
import requests
from .hardcoded_data import hardcoded_data





def home(request):
    if request.method == 'POST':
        query = request.POST['query'].lower()  # Ensure query is lowercase for matching
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_requests = requests.get(api_url + query, headers={'X-Api-Key': 'OrSK5nwXybV9YVnbwRNl0w==ZtJwrkx8YIkTTRlw'})
        
        try:
            api_response = json.loads(api_requests.content)
            
            # Ensure all required fields are in the API response, otherwise use defaults
            if 'calories' not in api_response[0] or 'protein' not in api_response[0]:
                if query in hardcoded_data:
                    api_response = [{
                        'name': query.capitalize(),
                        'calories': hardcoded_data[query]['calories'],
                        'carbohydrates_mg': hardcoded_data[query]['carbohydrates_mg'],
                        #'protein': hardcoded_data[query]['protein'],
                        'cholesterol_mg': hardcoded_data[query]['cholesterol_mg'],
                        'fat_saturated_g': hardcoded_data[query]['fat_saturated_g'],
                        'fat_total_g': hardcoded_data[query]['fat_total_g'],
                        'fiber_g': hardcoded_data[query]['fiber_g'],
                        'potassium_mg': hardcoded_data[query]['potassium_mg'],
                        'sodium_mg': hardcoded_data[query]['sodium_mg'],
                        'sugar_g': hardcoded_data[query]['sugar_g'],
                    }]
                else:
                    raise ValueError("No data available for this dish.")
            else:
                # Ensure default values for all fields are set if not provided by the API
                api_response[0].setdefault('carbohydrates_mg', 0)
                api_response[0].setdefault('cholesterol_mg', 0)
                api_response[0].setdefault('fat_saturated_g', 0)
                api_response[0].setdefault('fat_total_g', 0)
                api_response[0].setdefault('fiber_g', 0)
                api_response[0].setdefault('potassium_mg', 0)
                api_response[0].setdefault('sodium_mg', 0)
                api_response[0].setdefault('sugar_g', 0)
                
            return render(request, 'home.html', {'api': api_response})
        
        except Exception as e:
            if query in hardcoded_data:
                api_response = [{
                    'name': query.capitalize(),
                    'calories': hardcoded_data[query]['calories'],
                    'protein': hardcoded_data[query]['protein'],
                    'cholesterol_mg': hardcoded_data[query]['cholesterol_mg'],
                    'fat_saturated_g': hardcoded_data[query]['fat_saturated_g'],
                    'fat_total_g': hardcoded_data[query]['fat_total_g'],
                    'fiber_g': hardcoded_data[query]['fiber_g'],
                    'potassium_mg': hardcoded_data[query]['potassium_mg'],
                    'sodium_mg': hardcoded_data[query]['sodium_mg'],
                    'sugar_g': hardcoded_data[query]['sugar_g'],
                }]
                return render(request, 'home.html', {'api': api_response})
            else:
                api = "Oops! There was an error."
                return render(request, 'home.html', {'api': api})

    else:
        return render(request, 'home.html', {'query': 'Enter a valid query'})
