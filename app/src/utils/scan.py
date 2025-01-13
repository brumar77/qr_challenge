
import requests


def get_country_from_ip(ip: str):
    access_key_ipstack = "841251801b5670c34e5f8412815ee430"
        
    url = f"http://api.ipstack.com/{ip}?access_key={access_key_ipstack}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        country_name = data.get('country_name', 'Unknown')
        city = data.get('city', 'Unknown')
        current_time = data.get('time_zone', {}).get('id', 'Unknown')
        
        return country_name, city, current_time
    
    return 'Unknown', 'Unknown', 'Unknown'