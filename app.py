import streamlit as st
import requests
import pandas as pd
import base64
import io
from streamlit_extras.dataframe_explorer import dataframe_explorer
from PIL import Image
import plotly.express as px

# Data Frame
df = None

# Temp Value for Zipcode
zipcode = 0

# APIS
api_key = "fedbba368fc68a5b3f3fc1e627152a82"
API_BASE_URL = "http://127.0.0.1:8000"


# Post request to add workout
def add_workout(workout):
    response = requests.post(f"{API_BASE_URL}/workouts/", json=workout)
    return response.json()

# Get request to retrieve workouts
def get_workouts():
    response = requests.get(f"{API_BASE_URL}/workouts/")
    return response.json()

# Get request to retrieve weather information
def get_weather(wkid: int):
    response = requests.get(f"{API_BASE_URL}/weatherinfo/{wkid}")
    return response.json()

# Get request to retrieve health information
def get_health(wkid: int):
    response = requests.get(f"{API_BASE_URL}/healthinfo/{wkid}")
    return response.json()

# Get request to retrieve aggregated data
def get_summarized():
    response = requests.get(f"{API_BASE_URL}/summarizedinfo/")
    return response.json()

st.title('Running Workouts Tracker')

with st.form("workout_form", clear_on_submit=True):
    st.write("## Add New Workout")
    duration_minutes = st.number_input("Duration (minutes)", min_value=1, value=30)
    distance_km = st.number_input("Distance (km)", min_value=0.1, value=5.0, step=0.1)
    route_nickname = st.text_input("Route Nickname")
    age = st.number_input("Age", min_value=18, max_value=120,step=1, value=18)
    heart_rate_avg = st.number_input("Heart Rate", min_value=60, max_value=200, step=1, value=60)
    weight = st.number_input("Weight",step=1,value=150)
    zipcode = st.text_input("Zipcode")
    date_time = st.date_input("Date")
    image = st.file_uploader("Workout Selfie!", type=["png", 'jpg'])
    if image:
        encoded_image = base64.b64encode(image.read())
        encoded_image = encoded_image.decode()
    else:
        encoded_image = None
    submit = st.form_submit_button("Submit")

    if submit:
        workout = {
            "duration_minutes": duration_minutes,
            "distance_km": distance_km,
            "route_nickname": route_nickname or None,
            "heart_rate_avg": heart_rate_avg if heart_rate_avg > 0 else None,
            "date_time": date_time.isoformat(),
            "age": age,
            "weight": weight,
            "zipcode": zipcode,
            "image": encoded_image
        }
        result = add_workout(workout)
        if result:
            st.success("Workout added successfully!")

with st.expander("Weather Data"):
     with st.form("Workout Id Weather"):
         id = st.number_input("Workout Id", step=1, min_value=0)
         s = st.form_submit_button("Submit")
         wk = get_workouts()
         try:
            weather = get_weather(id)
            st.write(weather)
         except:
             st.write("Workout id not found")

with st.expander("Health Details"):
    with st.form("Workout Id Health"):
        id = st.number_input("Workout Id", step=1, min_value=0)
        s = st.form_submit_button("Submit")
        wk = get_workouts()
        try:
            health = get_health(id)
            st.write(health)
        except:
            st.write("Workout id not found")


def helper_func(iterations, step):
    temp_array = []
    counter = 0
    for i in range(1,iterations+1):
        counter += 1
        temp = step * counter
        temp_array.append(temp)
    return temp_array

with st.expander("Aggregated Data Summary"):
    st.write("5 workouts in database minimum!!!")
    wk = get_workouts()
    if len(wk) > 5:
        summarized_data = get_summarized()
        average_heart = summarized_data["hr"]
        average_duration = summarized_data["dr"]
        average_age = summarized_data["age"]
        average_distance = summarized_data["distance"]
        st.write("Average Heart Rate: " + str(average_heart))
        st.write("Average Duration: " + str(average_duration))
        st.write("Average Age: " + str(average_age))
        st.write("Average Distance: " + str(average_distance))
        fig1 = px.scatter(x=helper_func(len(summarized_data["heart_list"]),1), y = summarized_data["heart_list"], title= "Heart rates")
        st.write(fig1)
        fig2 = px.scatter(x=helper_func(len(summarized_data["distance_list"]),1), y=summarized_data["distance_list"],
                          title="Distances")
        st.write(fig2)
        fig3 = px.scatter(x=helper_func(len(summarized_data["duration_list"]),1), y=summarized_data["duration_list"],
                          title="Durations")
        st.write(fig3)
        fig4 = px.scatter(x=helper_func(len(summarized_data["age_list"]), 1), y=summarized_data["age_list"],
                          title="Ages")
        st.write(fig4)

    else:
        st.write("You do not have the minimum workouts necessisary")
st.write("## View Workouts")

if st.button("Refresh"):
    workouts = get_workouts()
    df = dataframe_explorer(pd.DataFrame.from_dict(workouts))
    st.write(df)
    with st.expander("Detailed View"):
        for workout in workouts:
            st.write(f"### Workout ID: {workout['id']}")
            st.write(f"**Duration**: {workout['duration_minutes']} minutes")
            st.write(f"**Distance**: {workout['distance_km']} km")
            if workout['route_nickname']:
                st.write(f"**Route**: {workout['route_nickname']}")
            if workout['heart_rate']:
                st.write(f"**Heart Rate**: {workout['heart_rate']} bpm")
            st.write(f"**Date**: {workout['date_time']}")
            if workout["image"]:
                encoded_image = workout["image"]
                image = Image.open(io.BytesIO(base64.b64decode(encoded_image)))
                st.image(image, use_column_width=True)
            st.write("---")
        else:
            st.write("No workouts found, please add some and try again!")
