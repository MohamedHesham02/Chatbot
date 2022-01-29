import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
import requests

from keras.models import load_model
import json
import random

# importing pre-trained model and dataset
model = load_model('model.h5')
intents = json.loads(open('data.json').read())
words = pickle.load(open('texts.pkl','rb'))
classes = pickle.load(open('labels.pkl','rb'))

# doing morphological analysis of the words to get the base words of dataset
lemmatizer = WordNetLemmatizer()

def clean_up_sentence(sentence):
    # tokenize the pattern - split text into words array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - take basic form for word 
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words) 

    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
                    
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        # returning class name and propability of predicted class
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

# choose the response needed for the question or sentence written by user based on the class predicted 
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

# Using countries list API to guide the user for his required info about the country and return final response
def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    url = requests.get('https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCountries').content
    json_file = json.loads(url)
    print(ints)
    if ints[0]['intent'] == 'countries':
        return 'Choose the country from this list: '+str(json_file['body'])+' ...and required data whether its a population or capital of the country in the following format i.e... Tell me the (capital or population) of Finland'
    elif ints[0]['intent'] == 'wrong_country':
        return 'Wrong Country, please choose a country from this list: '+str(json_file['body'])+' ...and required data whether its a population or capital of the country in the following format i.e... Tell me the (capital or population) of Finland'
    else:
        return res

from flask import Flask, render_template, request

# importing html file and test the app using rest api
app = Flask(__name__,template_folder='templates')
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

# get user message to apply the app or machine learning model on it 
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)


if __name__ == "__main__":
    app.run()