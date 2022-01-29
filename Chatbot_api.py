#!/usr/bin/env python
# coding: utf-8

import uvicorn
from fastapi import FastAPI
import random
import requests, json

app = FastAPI()

# Greetings possible inputs from user and possibilties of responses to randomly choose from them
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]

# normalize words to lower case to be compatible of understanding various changes in capital and small words 
def greeting(sentence):
    # tokenize the input to understand the type of input on scale of words
    for word in sentence.split():
        # checking that input in greeting type 
        if word.lower() in GREETING_INPUTS:
            # randomly choose from responses
            return random.choice(GREETING_RESPONSES)


# read json data from the API 
url = requests.get('https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCountries').content
json_file = json.loads(url)
Country = json_file['body']
# covert the list of countries to lower case for better understanding various changes in capital and small words
Country_s = []
for i in range(len(Country)):
    Country_s.append(Country[i].lower())

# capitals and population of countries
Dataset = { 'usa' : { 'capital': 'Washington, D.C.', 'population': '331,893745 Millions'},
            'greece' : { 'capital': 'Athens', 'population': '10,700000 Millions'},
            'sweden' : { 'capital': 'Stockholm', 'population': '10,350000 Millions'},
            'australia' : { 'capital': 'Canberra', 'population': '25,690000 Millions'},
            'finland' : { 'capital': 'Helsinki', 'population': '5,531000 Millions'},
            'japan' : { 'capital': 'Tokyo', 'population': '125,800000 Millions'},
            'russia' : { 'capital': 'Moscow', 'population': '144,100000 Millions'},
            'india' : { 'capital': 'Delhi', 'population': '1,380,000000 Billions'} }

# countries asking possible inputs from user
countries_input = ['data', 'countries', 'survey', 'tell', 'me', 'capital', 'population', 'crowded']

def check_input(user_response):
    flag_2 = False
    # tokenize the input to understand the type of input on scale of words
    for word in user_response.split():
        # checking that input in countries survey type 
        if (word.lower() in countries_input) or (word.lower() in Country_s):
            flag_2 = True
    # country selection        
    if flag_2 == True:
        print('ROBO: choose your country from', Country)
        sele_country = input()
            
        if sele_country.lower() in Country_s:
            # select the required feature to display
            selected_feature = input('ROBO: Do you want to display capital or population ? ')
            
        else:
            # in case of wrong country selection
            print("ROBO: Wrong selection....Please select one country from the written below...")
            print('ROBO: choose your country from', Country)
            sele_country = input()
            selected_feature = input('ROBO: Do you want to display capital or population ? ')
            
        flag_2 = False
        return Dataset[sele_country.lower()][selected_feature.lower()]    

## trial of 2nd API but unfortunately failed, also in 3rd API same problem
## 
"""
@app.get('/get_country')      
def getting_countries():
    url = "https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCountries"
    with urllib.request.urlopen(url) as link:
        countries = link.read()
    body = {"country": "Australia"}
    r = requests.post('https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getPopulation',data=body)
    return countries,r.text
"""

# Chatbot implementation
@app.post('/chat')
def chat(user_response:str):
    flag=True
    print("ROBO: My name is Robo. I will provide you the information you want. If you want to exit, type Bye!")

    while(flag==True):
        user_response = input('You: ')
        # normalize input 
        user_response=user_response.lower()
        # checking input class to provide suitable responses 
        if(user_response!='bye'):
        
            if(user_response=='thanks' or user_response=='thank you' ):
                flag=False
                print("ROBO: You are welcome..")
                        
            elif(greeting(user_response)!=None):
                return("ROBO: "+greeting(user_response))
                
            else:
                return("ROBO: "+check_input(user_response))
                
        else:
            flag=False
            return("ROBO: Bye! take care..")
            
      


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
