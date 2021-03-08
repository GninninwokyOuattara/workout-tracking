import requests
import datetime as dt
import os


APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
SHEET_ENDPOINT=os.environ.get("SHEET_ENDPOINT")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
TOKEN = os.environ.get("TOKEN")

nx_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

today = dt.datetime.now()
today = today.strftime("%d/%m/%Y")

query = input("Tell me which exercise you did : ")

post_params = {
    "query" : query,
}

post_headers = {
    "x-app-id" : APP_ID,
    "x-app-key" : API_KEY,
    "Content-Type": "application/json"
}

sheety_headers = {
    "Authorization": TOKEN
}

response = requests.post(url=nx_endpoint, json=post_params, headers = post_headers)
nx_datas = response.json()


# Sheety Post
for nx_data in nx_datas["exercises"]:
    time = dt.datetime.now()
    time = time.strftime("%H:%M:%S")
    body = {
        "workout" : {
            "date" : today,
            "exercise" : nx_data["name"].title(),
            "time" : time,
            "duration" : nx_data["duration_min"],
            "calories" : nx_data["nf_calories"],
        }
    }

    response = requests.post(url=SHEET_ENDPOINT, json=body, headers = sheety_headers)
    print(response.text)

