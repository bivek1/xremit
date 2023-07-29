import requests
import pycountry

def get_country_name(country_code):
    try:
        country = pycountry.countries.get(alpha_2=country_code.upper())
        return country.name
    except AttributeError:
        return "Invalid Country Code"
    
def get_user_country():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        country = data.get('country')
        region = data.get('region')
        city = data.get('city')
        dust = {
            'country':country,
            'region':region,
            'city':city
        }
        
        return dust
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

# if __name__ == "__main__":
#     country = get_user_country()
#     if country:
#         print(f"User's country: {country}")
#     else:
#         print("Could not determine user's country.")