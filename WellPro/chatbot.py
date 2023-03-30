from flask import Flask, request,jsonify
from keras.models import load_model
import numpy as np
import pickle
from flask_cors import CORS
import requests

wikipedia = Flask(__name__)
CORS(wikipedia)

@wikipedia.route('/chatbot',methods=['POST'])
def wiki():
    endpoint = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",#"prop": "extracts" specifies that the response should include the text extracts from the page(s) requested.
        "exintro": True,#Tells that the responce should include intro only
        "explaintext": True,
    }
    # Defining the disease that we  want to search for
    response=request.get_json()
    disease=response['queryResult']['parameters']['Disease-name']

    # Adding the disease name to the query parameters
    params["titles"] = disease

    # Sending the request and get the response in  json form (we re not converting it to json)
    response1 = requests.get(endpoint, params=params).json()
     
    # Check if the page exists in the wikipedia API
    if '-1' in response1['query']['pages']:
        additional_response = {"additional": "Additional data about this disease cannot be retrieved."}
        return jsonify(additional_response), 404

    # Extracting the text of the first page (the only page available)
    pages = response1["query"]["pages"]
    page_id = next(iter(pages))#we are not using[] because it is not in that form
    if "extract" not in pages[page_id]:
        additional_response = {"additional": "Additional data about this disease cannot be retrieved."}
        return jsonify(additional_response), 404
    text = pages[page_id]["extract"]


    description = []
    for line in text.split("."):
        if line.strip(): #check if the line is not null(string is empty or not?)(if not empty then it is true)
            description.append(line.strip())#Here line.strip() removes unnecessary indentation from front and back

    #Creating another request for extracting treatment
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": disease,
        "exsectionformat": "wiki",#This parameter specifies the format of the section titles in the returned text. If set to "wiki", the section titles are in wiki markup format.(wiki is a markup language)
        "explaintext": 1,#This parameter indicates that the API should return only plain text for the page content, without any formatting or markup.
        "exsectiontree": 1 #This parameter indicates that the API should return the section hierarchy of the page, which is useful for identifying the structure of the content.
        #By default, the API returns the page content in HTML format (exformat=html) and includes section headings (exsectionformat=wiki) but not the section tree (exsectiontree=0). 
        # If you want to retrieve the page content in plain text format without any markup, you can set explaintext=1 in your request.
    }

    response2 = requests.get(endpoint, params=params)

    # Check if the request was successful
    if response2.status_code == 200:
        pages = response2.json()["query"]["pages"]
        page = list(pages.values())[0]
        extract = page["extract"]
        start_index = extract.find("Treatment")
        end_index = extract.find("Prevention")
        treatment_first_two_lines = extract[start_index:end_index].split('.')[:2] #Here we dont apply splitting because we are just using 1st two lines
        #start_index:end_index implies split extract from start index to end index
    #Combining the output
    additional = description + treatment_first_two_lines
    # additional_response = {"additional": additional}
    additional_response={'fulfillmentText': ' '.join(additional)}
    return jsonify(additional_response)

if __name__ == '__main__':
    wikipedia.run(port=5002)
