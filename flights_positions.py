import os
import requests
import time
from kafka_utils import get_kafka_producer
import json

# Replace 'https://api.example.com/endpoint' with the actual API endpoint URL
api_endpoint = f'https://airlabs.co/api/v9/flights?_fields=hex,reg_number,dep_icao,arr_icao,flag,lat,lng,dir,alt&airline_icao=RYR&api_key={os.getenv("FLIGHT_API_KEY")}'

producer = get_kafka_producer()

while True:
    response = requests.get(api_endpoint)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response content (assuming it's in JSON format)
        data = response.json()
        # print('Data from the API endpoint:', data["response"])
    else:
        raise Exception(f'Failed to fetch data. Status code: {response.status_code}')
    message = json.dumps(data["response"])
    producer.send('flight_map_topic', message.encode('ascii'))
    producer.flush()
    time.sleep(2)
