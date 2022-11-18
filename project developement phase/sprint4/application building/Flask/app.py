from flask import Flask, render_template, request
# Flask-It is our framework which we are going to use to run/serve our application.
# request-for accessing file which was uploaded by the user on our application.
import os
import numpy as np  # used for numerical analysis

from tensorflow.keras.models import load_model  # to load our trained model
from tensorflow.keras.preprocessing import image
import requests

app = Flask(__name__, template_folder="template")  # initializing a flask app
# Loading the model
model = load_model('nutrition.h5')


@app.route('/')  # route to display the home page
def home():
    return render_template('home.html')  # rendering the home page


@app.route('/image')
def image1():
    return render_template("image.html")


@app.route('/predict', methods=['GET', 'POST']) # route to show the predictions in a web UI
def launch():
    if request.method == 'POST':
        f = request.files['image']
        basepath = os.path.dirname('__file__')
        filepath = os.path.join(basepath, "uploads", f.filename)
        f.save(filepath)

        img = image.load_img(filepath, grayscale=False,
                             target_size=(64, 64))  # Loading of the image
        x = image.img_to_array(img)  # image to array
        x = np.expand_dims(x, axis=0)  # changing the shape
        pred = np.argmax(model.predict(x))
        print(pred, model.predict(x))

        op = ['APPLES', 'BANANA', 'ORANGE', 'PINEAPPLE', 'WATERMELON']  # Creating list of output categories
        result = op[pred]
        print(result)
        x = result
        result = nutrition(result)
        print(result)
        return render_template("imageprediction.html", y=(result), x=(x))


def nutrition(index):
    url = "https://calorieninjas.p.rapidapi.com/v1/nutrition"
    querystring = {"query": index}
 
    headers = {
        'x-rapidapi-key': "5d797ab107mshe668f26bd044e64p1ffd34jsnf47bfa9a8ee4",
        'x-rapidapi-host': "calorieninjas.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    return response.json()['items']
if __name__=='__main__':
    app.run()
