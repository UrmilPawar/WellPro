import tensorflow
import keras
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_KERAS'] = '0'
from keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from flask import Flask, request, jsonify
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import io
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Loading the trained model
model = load_model('best_skin_model.h5')
diseases_names=pickle.load(open('skin_diseases_names.pkl','rb'))

#preprocess_image function to preprocess the uploaded image
@app.route('/predict2', methods=['POST'])
def predict():
    # Getting the image file from the request
    file = request.files['image']

    # Reading the image file contents as bytes
    #This line is reading the contents of the uploaded image file as bytes(actual language of the coputer)
    file_contents = file.read()

    #Preprocessing
    img = load_img(io.BytesIO(file_contents), target_size=(256, 256,3))#This line is using the Keras load_img function to load the image from the bytes in file_contents. The io.BytesIO class is used to convert the byte string to a file-like object that can be read by load_img.
    img_array = img_to_array(img)#converts into 3D array
    img_array = np.expand_dims(img_array, axis=0)#this is used to add an extra dimention to satisfy the requirement of batchsize
    img_array = img_array.astype('float32') / 255

    # Making a prediction with the model
    prediction = model.predict([img_array, img_array, img_array, img_array])#returns 1 hot encoded probablities
    predicted_class = np.argmax(prediction)#returns index of maximum probablity

    # Returning the predicted class as a response
    return jsonify({'disease': diseases_names[predicted_class]})

if __name__ == '__main__':
    app.run()



