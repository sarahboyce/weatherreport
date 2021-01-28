<h1 align="center">
  <br>
  <img src="weatherreport/static/icons/android-chrome-192x192.png" alt="Weather Report" width="192">
  <br>
</h1>

<h4 align="center">
    A django project to return the current weather forecast in cities
</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#docker-set-up">Docker Set Up</a>
</p>

---

## Key Features

### City Search
The main purpose of the weather report app is the city search with uses the <a href="https://openweathermap.org/api">OpenWeather API</a>. This will return the current weather forecast in a city found using this API.<br>

<img src="weatherreport/static/readme/city-search.gif" alt="City Search Demo" width="750">

### Languages
The weather report app currently supports 3 languages:
- English
- German
- French

You can select and update the language in the top nav bar.<br>

<img src="weatherreport/static/readme/language.gif" alt="Language Demo" width="750">
---

## Docker Set Up

In the root of the repository:
- Copy and paste `django.local.env` and rename to `django.env`
- <b>Create a free openweather account at https://openweathermap.org/ and update OPEN_WEATHER_API_KEY to your api key</b> 
- In the command line run 

`docker-compose up --build -d`

- When all of your containers have successfully been built, navigate to http://localhost:8000/ and enjoy :tada:
