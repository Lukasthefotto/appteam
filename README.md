# API Usage Guide

This API provides functionality for managing and retrieving workout data, as well as providing health and weather information related to workouts.

## Endpoints

### 1. `POST /workouts/`

This endpoint allows you to add a new workout to the database.

**Request:**
- Method: POST
- Endpoint: `/workouts/`
- Body: JSON payload with workout data including `duration_minutes`, `distance_km`, `route_nickname`, `heart_rate_avg`, `age`, `date_time`, `zipcode`, `weight`, and `image`.

**Response:**
- JSON response with the details of the added workout.

### 2. `GET /workouts/`

This endpoint allows you to retrieve a list of all workouts in the database.

**Request:**
- Method: GET
- Endpoint: `/workouts/`

**Response:**
- JSON response with a list of all workouts.

### 3. `GET /workouts/{workout_id}`

This endpoint allows you to retrieve a specific workout by its `workout_id`.

**Request:**
- Method: GET
- Endpoint: `/workouts/{workout_id}`
- Path Parameter: `workout_id` (integer) - The ID of the workout to retrieve.

**Response:**
- JSON response with the details of the specified workout if found, or a 404 error if not found.

### 4. `GET /healthinfo/{workout_id}`

This endpoint allows you to retrieve health-related information for a specific workout by its `workout_id`. It calculates and returns data such as calories burned, target heart rate range, steps estimator, and speed in kilometers per hour.

**Request:**
- Method: GET
- Endpoint: `/healthinfo/{workout_id}`
- Path Parameter: `workout_id` (integer) - The ID of the workout to calculate health information for.

**Response:**
- JSON response with health information for the specified workout if found, or a 404 error if not found.

### 5. `GET /weatherinfo/{workout_id}`

This endpoint allows you to retrieve weather information for a specific workout by its `workout_id`. It requires an API key for weather data retrieval.

**Request:**
- Method: GET
- Endpoint: `/weatherinfo/{workout_id}`
- Path Parameter: `workout_id` (integer) - The ID of the workout to retrieve weather information for.
- Query Parameter: `api_key` (string) - Your API key for accessing weather data (default key provided in the code).

**Response:**
- JSON response with weather information for the specified workout if found, or a 404 error if not found.

### 6. `GET /summarizedinfo/`

This endpoint allows you to retrieve summarized information about all workouts in the database. It provides average values for heart rate, duration, age, weight, and distance, as well as lists of individual values for further analysis.

**Request:**
- Method: GET
- Endpoint: `/summarizedinfo/`

**Response:**
- JSON response with summarized information about all workouts.

## Python Functions

The API includes Python functions for adding workouts and retrieving data from the database. You can use these functions in your Python code:

- `add_workout(workout)`: Adds a new workout to the database.
- `get_workouts()`: Retrieves a list of all workouts.
- `get_health(wkid)`: Retrieves health information for a specific workout by `workout_id`.
- `get_weather(wkid)`: Retrieves weather information for a specific workout by `workout_id`.
- `get_summarized()`: Retrieves summarized information about all workouts.

# Function Descriptions

## `heart_rate_range(a: int)`
This function takes an integer `a` as input, representing age, and returns a heart rate range based on the age value. It uses conditional statements to determine the appropriate heart rate range for the given age.

- **Input:**
  - `a` (integer): Age of the person.

- **Output:**
  - Heart rate range as a string.

## `steps_estimator(km: int)`
This function estimates the number of steps taken based on the distance in kilometers (`km`). It generates a random number of steps per kilometer within a specific range and multiplies it by the given distance to estimate the total number of steps.

- **Input:**
  - `km` (integer): Distance in kilometers.

- **Output:**
  - Estimated number of steps as an integer.

## `calorie_burned(w: int, d: int, t: int)`
This function calculates the calories burned during a workout based on weight (`w` in kilograms), distance (`d` in kilometers), and duration (`t` in minutes). It uses the MET (Metabolic Equivalent of Task) value, speed, and a formula to compute calorie expenditure.

- **Input:**
  - `w` (integer): Weight of the person in kilograms.
  - `d` (integer): Distance covered in kilometers.
  - `t` (integer): Duration of the workout in minutes.

- **Output:**
  - Estimated calories burned as a floating-point number.

## `get_weather(zip: int, api: str)`
This function fetches weather information for a specific location based on a ZIP code (`zip`) and an API key (`api`). It constructs an API request to OpenWeather API using the provided ZIP code and API key, retrieves the weather data, and returns it as a JSON object.

- **Input:**
  - `zip` (integer): ZIP code for the location.
  - `api` (string): API key for accessing weather data.

- **Output:**
  - Weather information as a JSON object.

## `information_extractor(zip: int, api: str)`
This function uses the `get_weather` function to fetch weather information for a specific location and then extracts relevant data from the JSON response. The extracted information includes temperature, pressure, humidity, visibility, cloud coverage, and the location name.

- **Input:**
  - `zip` (integer): ZIP code for the location.
  - `api` (string): API key for accessing weather data.

- **Output:**
  - Weather information as a dictionary containing various attributes.

These functions serve different purposes, including calculating health-related data, estimating steps, computing calorie burn, and fetching weather information. Make sure to provide the appropriate inputs when using these functions in your code.



## Dependencies

This API is built using Python and relies on several external libraries and modules to function properly. Below is a list of the main dependencies used in this project:

1. **FastAPI**: FastAPI is a modern web framework for building APIs quickly. It simplifies the process of creating web applications and APIs in Python.

2. **HTTPException**: Part of the FastAPI framework, the HTTPException class is used to raise HTTP exceptions with specific status codes and error details when necessary.

3. **typing**: The typing module is used for type hinting in Python. It helps indicate the expected types of function arguments and return values, enhancing code readability and maintainability.

4. **datetime**: The datetime module is a standard Python library that allows working with date and time information. It is used in this project for handling timestamps and date-related operations.

5. **requests**: The requests library is used for making HTTP requests to external APIs. It enables communication with external services to fetch weather data.

6. **threading**: Threading is a Python module that provides tools for working with threads. In this project, threading is used for concurrent or asynchronous data processing.

7. **random**: The random module is a standard Python library that allows generating random numbers and values. It is utilized for various purposes, such as generating random data or making random selections.

8. **statistics**: The statistics module is part of the Python standard library and offers functions for statistical operations. It is used in the project to compute average values and perform basic statistical calculations.
