from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()


db = []


class City(BaseModel):
    name: str
    timezone: str


WEATHERSTACK_API_KEY = 'e92a9eb34cd84339b4eca0e07ceea1b3'


def get_weather_data(city_name):
    url = f"http://api.weatherstack.com/current?access_key={WEATHERSTACK_API_KEY}&query={city_name}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Weatherstack API error")
    weather_data = response.json()
    if 'current' not in weather_data:
        raise HTTPException(status_code=404, detail="City weather data not found")
    return weather_data['current']


@app.get('/cities/')
def get_cities():
    results = []
    for index, city in enumerate(db):
        t(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
        current_time = time_response.json().get('datetime', 'N/A')  
        # Get the weather data
        weather = get_weather_data(city['name'])

        
        results.append({
            'id': index + 1,
            'name': city['name'],
            'timezone': city['timezone'],
            'current_time': current_time,
            'temperature': weather.get('temperature', 'N/A'),
            'feels like':weather.get('feelslike','N/A'),
            'humidity': weather.get('humidity', 'N/A'),
            'weather_condition': weather.get('weather_descriptions', ['N/A'])[0],
        })
    return results


@app.get('/cities/{city_id}/')
def get_city(city_id: int):
    if city_id < 1 or city_id > len(db):
        raise HTTPException(status_code=404, detail="City not found")
    
    city = db[city_id - 1]
    
    time_response = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
    current_time = time_response.json().get('datetime', 'N/A')

    
    weather = get_weather_data(city['name'])

    return {
        'id': city_id,
        'name': city['name'],
        'timezone': city['timezone'],
        'current_time': current_time,
        'temperature': weather.get('temperature', 'N/A'),
        'humidity': weather.get('humidity', 'N/A'),
        'weather_condition': weather.get('weather_descriptions', ['N/A'])[0],
    }


@app.post('/cities/')
def add_city(city: City):
    db.append(city.dict())
    return {'id': len(db), **db[-1]}


@app.delete('/cities/{city_id}/')
def delete_city(city_id: int):
    if city_id < 1 or city_id > len(db):
        raise HTTPException(status_code=404, detail="City not found")
    
    db.pop(city_id - 1)
    return {'message': f'City with id {city_id} has been deleted'}
