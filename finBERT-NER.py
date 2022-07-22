import requests
import json
import pandas as pd

# jsonista taulukko

df=pd.read_json('S-ryhmä_tweet_sentiments.json')

#taulukosta otetaan 10 kpl otos

df2  =df.sample(10)

l = []

#lähetän otoksen tekstit localhostiin

for text in df2['cleanContent']:
    
    response = requests.get('http://localhost:5000/', data=text.encode())
    
    #tässä on pilkottu responsea ja sitten tungen sen listana uuteen taulukkoon, en tiedä onko mitään järkeä. 
    
    x = response.text.split("\n")
    x = [i for i in x if not ('\tO' in i)]
    x = [sub.replace('\t', ' ') for sub in x]
    resp_dict= {
        'ents': x,
        'cleanContent':text,
    }
    l.append(resp_dict)
    
# yksi entiteetti voi myös olla peräkkäisiä sanoja joissa "B-" etuliite merkitsee ensimmäistä sanaa ja "I-" seuraavia
df3 = pd.DataFrame(l)
df3
