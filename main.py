from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime
import requests
import threading
import random
import statistics
# Used Open Weather API for precise weather data


app = FastAPI()

# In-memory storage for demonstration
workouts = []
data_lock = threading.Lock()

@app.post("/workouts/")
def create_workout(workout_data: dict):
    workout = {
        "id": len(workouts) + 1,
        "duration_minutes": workout_data["duration_minutes"],
        "distance_km": workout_data["distance_km"],
        "route_nickname": workout_data.get("route_nickname"),
        "heart_rate": workout_data.get("heart_rate_avg"),
        "age": workout_data.get("age"),
        "date_time": datetime.fromisoformat(workout_data["date_time"]),
        "zipcode": workout_data.get("zipcode"),
        "weight": workout_data.get("weight"),
        "image": workout_data.get("image")
    }
    with data_lock:
        workouts.append(workout)
    return workout

@app.get("/workouts/", response_model=List[dict])
def read_workouts():
    return workouts

@app.get("/workouts/{workout_id}", response_model=dict)
def read_workout(workout_id: int):
    for workout in workouts:
        if workout["id"] == workout_id:
            return workout
    raise HTTPException(status_code=404, detail="Workout not found")

@app.get("/healthinfo/{workout_id}", response_model = dict)
def health(workout_id: int):
    for workout in workouts:
        if workout["id"] == workout_id:
            km = workout["distance_km"]
            time = workout["duration_minutes"]
            heart_rate = workout["heart_rate"]
            weight = workout["weight"]
            age = workout["age"]
            #calculations
            calories = calorie_burned(weight,km,time)
            target_hr = heart_rate_range(age)
            steps = steps_estimator(km)
            km_per_hr = float(km / (time/60))
            return {
                "Calories Burned" : calories,
                "Target Heart Rate Range": target_hr,
                "Steps Estimator" : steps,
                "Km per hour": km_per_hr
            }
    raise HTTPException(status_code=404, detail="Workout not found")

@app.get("/weatherinfo/{workout_id}", response_model=dict)
def weather(workout_id: int, api_key: str = "fedbba368fc68a5b3f3fc1e627152a82"):
    for workout in workouts:
        if workout["id"] == workout_id:
            zipcode = workout["zipcode"]
            weather_info = information_extracter(zipcode, api_key)  # Call the function to get weather info
            return weather_info
    raise HTTPException(status_code=404, detail="Workout not found")

@app.get("/summarizedinfo/", response_model=dict)
def summarized_info():
    heart_rate = []
    duration = []
    age = []
    weight = []
    distance = []
    for workout in workouts:
        heart_rate.append(workout["heart_rate"])
        duration.append(workout["duration_minutes"])
        age.append(workout["age"])
        weight.append(workout["weight"])
        distance.append(workout["distance_km"])
    avg_hr = statistics.mean(heart_rate)
    avg_dr = statistics.mean(duration)
    avg_age = statistics.mean(age)
    avg_w = statistics.mean(weight)
    avg_dis = statistics.mean(distance)


    return {
        "hr": avg_hr,
        "dr": avg_dr,
        "age": avg_age,
        "weight": avg_w,
        "distance": avg_dis,
        "heart_list": heart_rate,
        "duration_list": duration,
        "distance_list": distance,
        "weight_list": weight,
        "age_list": age
    }




def heart_rate_range(a: int):
    if a > 70:
        return "75-128"
    elif a > 60:
        return "80-136"
    elif a > 50:
        return "85-145"
    elif a > 40:
        return "90-153"
    elif a > 30:
        return "95-162"
    elif a > 18:
        return "100-170"
    else:
        return "100-170"

def steps_estimator(km: int):
    steps_per_km = random.randint(1265,1515)
    return steps_per_km * km

def calorie_burned(w:int, d: int, t: int):
    met = 0
    t = float(t / 60)
    kph = float(d / t)

    if kph > 11:
        met = 11.2
    elif kph > 9:
        met = 8.8
    elif kph > 5:
        met = 5.4
    else:
        met = 3

    formula = ((met * w * 3.5) / 200) * 60
    return formula


def get_weather(zip: int, api):
    url = "http://api.openweathermap.org/data/2.5/weather?"
    params = {
        "zip": zip,
        "appid": api,
        "units": "imperial"
    }
    response = requests.get(url,params=params)
    return response.json()

def information_extracter(zip: int, api):
    info = get_weather(zip, api)
    weather_info = {
        "temperature": info['main']['temp'],
        "pressure": info['main']['pressure'],
        "humidity": info['main']["humidity"],
        'visibility': info.get("visibility", "N/A"),
        "clouds": info["clouds"]["all"],
        "name": info["name"]
    }
    return weather_info




