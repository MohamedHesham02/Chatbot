import uvicorn
from fastapi import FastAPI
import random
import urllib, json
import urllib.request
import requests

app = FastAPI()

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
            


Country = ["USA","Greece","Sweden","Australia","Finland","Japan","Russia",'India']
Country_s = ["usa","greece","sweden","australia","finland","japan","russia",'india']

Dataset = { 'usa' : { 'capital': 'Washington, D.C.', 'population': '331,893745 Millions'},
            'greece' : { 'capital': 'Athens', 'population': '10,700000 Millions'},
            'sweden' : { 'capital': 'Stockholm', 'population': '10,350000 Millions'},
            'australia' : { 'capital': 'Canberra', 'population': '25,690000 Millions'},
            'finland' : { 'capital': 'Helsinki', 'population': '5,531000 Millions'},
            'japan' : { 'capital': 'Tokyo', 'population': '125,800000 Millions'},
            'russia' : { 'capital': 'Moscow', 'population': '144,100000 Millions'},
            'india' : { 'capital': 'Delhi', 'population': '1,380,000000 Millions'} }

countries_input = ['data', 'countries', 'survey', 'tell', 'me', 'capital', 'population']

def check_input(user_response):
    flag_2 = False
    for word in user_response.split():
        if (word.lower() in countries_input) or (word.lower() in Country_s):
            flag_2 = True
            
    if flag_2 == True:
        print('ROBO: choose your country from', Country)
        sele_country = input()
            
        if sele_country.lower() in Country_s:
            selected_feature = input('ROBO: Do you want to display capital or population ? ')
            
        else:
            print("ROBO: Wrong selection....Please select one country from the written below...")
            print('ROBO: choose your country from', Country)
            sele_country = input()
            
        flag_2 = False
        return Dataset[sele_country.lower()][selected_feature.lower()]
        

@app.get('/get_country')      
def getting_countries():
    url = "https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCountries"
    with urllib.request.urlopen(url) as link:
        countries = link.read()
    body = {"country": "Australia"}
    r = requests.post('https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getPopulation',data=body)
    return countries,r.text

print("ROBO: My name is Robo. I will provide you the information you want. If you want to exit, type Bye!")
"""
@app.post('/capital')
def find_cap(country:str):
    url = "https://qcooc59re3.execute-api.us-east-1.amazonaws.com/dev/getCapital"+str()
    capitals = urllib.urlopen(url)
    return countries
"""

def chat(user_response:str):

    flag=True
    while(flag==True):
        #user_response = input()
        user_response=user_response.lower()
    
        if(user_response!='bye'):
        
            if(user_response=='thanks' or user_response=='thank you' ):
                flag=False
                return ("ROBO: You are welcome..")
                        
            elif(greeting(user_response)!=None):
                return ("ROBO: "+greeting(user_response))
                
            else:
                return ("ROBO: "+check_input(user_response))
                
        else:
            flag=False
            return ("ROBO: Bye! take care..")
    


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)


