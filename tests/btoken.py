import requests
import json

ip="http://192.168.77.116/"

def get_token():
    body = {
        "grant_type": "password",
        "client_id": "2",
        "client_secret": "23IzWSgkX5MUlpxSAYJr2o1sM8DRkLXI7vlZFExW",
        "username": 'director',
        "password": 'pass'
           }
    response = requests.post(ip + '/oauth/token', data=body)  # Запрос на добавление результата звонка
    requestdict = json.loads(response.content)
    headers = {"Authorization": 'Bearer ' + requestdict['access_token']}
    return headers
