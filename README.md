# Weather Project
This project was made with Python (Flask) gets the information for weather and forecast from ["OpenWeather API"](https://openweathermap.org/api) and converts this information to a more readable format.
## Returned Dictionary
The dictionary returned uses the Okta and Beaufurt scales to show the cloudiness and wind speed in a more readable way.
```
{   
    "location_name": str,
    "temperature": str,
    "wind": str,
    "cloudiness": str,
    "pressure": str,
    "humidity": str,
    "sunrise": str,
    "sunset": str,
    "geo_coordinates": str,
    "requested_time": str
    "forecast":[
                {
                    "datetime": str,
                    "temperature": str,
                    "wind": str,
                    "cloudiness": str,
                    "pressure": str,
                    "humidity": str,
                },
                ...
            ]
}
```
## How to excecute?
You must to have installed Docker and Docker Compose to run this web app.  
1. Clone this repository in your machine  
2. Rename the .env-example file to .env  
3. Edit the .env file and add your api key for OpenWeather  
4. Run in your terminal inside the cloned repository folder:  
    ```docker-compose -up```  
**Note: You'll need the port 5000 for Flask and the port 6379 for Redis**

## Entry point
GET /weather  
URL parameters:  
    - **city** (required): Is the name of the city you want to search  
    - **country** (required): Is the ISO 3166 code of the country  
    - *temperature_unit* (optional): Sets the unit for temperature values, *f* for fahrenheit, *c* for celcius, defaults return both.  
    - *api_key* (optional): If you don't have access to the .env file to write your API KEY, this can be entered as an URL parameter.  