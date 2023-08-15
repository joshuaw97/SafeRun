from flask import Flask, render_template, request
import requests
from forms import RunForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route("/", methods=['GET', 'POST'])
def index():
    form = RunForm()
    if request.method == 'POST':
        userLocation = form.username.data
        pace = int(form.userpace.data)
        data = {
            'auth': '',
            'locate': userLocation,
            'region': 'US',
            'json': 1,
        }
        response = requests.post('https://geocode.xyz', data=data)
        responseJson = response.json()

        latitude = responseJson['latt']
        longitude = responseJson['longt']

        latitudeInt = int(float(latitude))
        longitudeInt = int(float(longitude))

        weatherUrl = f'https://api.weather.gov/points/{latitudeInt:.4f},{longitudeInt:.4f}'
        weatherResponse = requests.get(weatherUrl)
        weatherData = weatherResponse.json()

        newDataUrl = f'https://api.weather.gov/points/{latitude},{longitude}'
        newDataResponse = requests.get(newDataUrl)
        newData = newDataResponse.json()
        gridId = newData["properties"]["cwa"]
        gridX = newData["properties"]["gridX"]
        gridY = newData["properties"]["gridY"]

        hourlyUrl = f"https://api.weather.gov/gridpoints/{gridId}/{gridX},{gridY}/forecast/hourly"
        hourlyResponse = requests.get(hourlyUrl)
        hourlyData = hourlyResponse.json()

        temp = hourlyData["properties"]["periods"][0]["temperature"]
        dew = hourlyData["properties"]["periods"][0]["dewpoint"]["value"]
        dewFahrenheit = (dew * 9/5) + 32
        tempAndDewpoint = temp + dewFahrenheit

        paceAdjustment = 0.0
        if 100 <= tempAndDewpoint <= 110:
            paceAdjustment = 0.005
        elif 111 <= tempAndDewpoint <= 120:
            paceAdjustment = 0.01
        elif 121 <= tempAndDewpoint <= 130:
            paceAdjustment = 0.02
        elif 131 <= tempAndDewpoint <= 140:
            paceAdjustment = 0.03
        elif 141 <= tempAndDewpoint <= 150:
            paceAdjustment = 0.045
        elif 151 <= tempAndDewpoint <= 160:
            paceAdjustment = 0.06
        elif 161 <= tempAndDewpoint <= 170:
            paceAdjustment = 0.08
        elif 171 <= tempAndDewpoint <= 180:
            paceAdjustment = 0.1
        elif tempAndDewpoint > 180:
            paceAdjustment = None

        adjustedPaceMinutes = int(pace) * (1 + paceAdjustment)
        adjustedPaceMinutesInt = int(adjustedPaceMinutes)
        adjustedPaceSeconds = (adjustedPaceMinutes - adjustedPaceMinutesInt) * 60
        adjustedPaceSecondsInt = int(adjustedPaceSeconds)
        adjustedPaceFormatted = f"{adjustedPaceMinutesInt}:{adjustedPaceSecondsInt:02d}"

        return render_template('form.html', dew=tempAndDewpoint, pace=adjustedPaceFormatted, form=form)

    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)






