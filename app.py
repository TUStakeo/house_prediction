# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 01:50:25 2020

@author: ASUS
"""

from pycaret.classification import load_model, predict_model
import streamlit as st
import pandas as pd
import numpy as np


def predict_quality(model, df):
    
    predictions_data = predict_model(estimator = model, data = df)
    
    return predictions_data['Label'][0]
    
model = load_model('random_forest_model')

place_list = ["世田谷区",	"中央区",	"中野区",	"北区",	"千代田区",	"台東区",	"品川区",	"墨田区",	"大田区",	"文京区",	"新宿区",	"板橋区",	"江戸川区","江東区"	,"渋谷区",	"港区","目黒区"	,"練馬区",	"荒川区",	"葛飾区",	"豊島区",	"足立区"]
dist_list  = ["とても近い", "やや近い", "やや遠い", "遠い"]
convinience_list =["1駅で十分", "2駅は欲しい" ,"3駅くらいのところに住みたい"]
old_list =["新築じゃないとイヤ", "こだわりなし"]

st.title('houseprising prediction Web App')
st.write('東京23区の賃貸の価格予測アプリを簡易的に作ってみた')


layout = st.text_input("お探しの間取りを教えてください")                   
place = st.selectbox(
    "住みたい区を選んでください",
    place_list
)
old = st.selectbox(
    "建物の古さはどうですか?",
    old_list
)
dist = st.selectbox(
    "最寄りからどれくらいの距離に住みたいですか",
    dist_list
)
conv = st.selectbox(
    "住居の近くにどれくらい駅が欲しいですか?",
    convinience_list
)
print(place)
 
#入力データをまとめる
data_place = np.zeros(len(place_list))
for i in range(0,len(place_list)):
  if place == place_list[i]:
    data_place[i] = 1
data_place = pd.DataFrame(data_place.reshape(1,len(place_list)),columns=place_list)
room_number = int(layout[0])
DK = 0
K  = 0
L  = 0
S  = 0
if "DK" in layout:
  DK = 1
elif "K" in layout:
  K = 1
else:
  DK = 0
  K  = 0
if "L" in layout:
  L = 1
if "S" in layout:
  S = 1
for place_element in place_list:
  if place_element == place:
    exec('{} = {}'.format(place_element, 1))
  else:
    exec('{} = {}'.format(place_element, 0))

for old_element in old_list:
  if old_element == old:
    exec('{} = {}'.format(old_element, 1))
  else:
    exec('{} = {}'.format(old_element, 0))

for place_element in place_list:
  if place_element == place:
    exec('{} = {}'.format(place_element, 1)) 
  else:   
    exec('{} = {}'.format(place_element, 0)) 

conv_out = 0
for i in range(0,len(convinience_list)):
  if convinience_list[i] == conv:
   conv_out = i+1

for dist_element in dist_list:
  if dist_element == dist:
    exec('{} = {}'.format(dist_element, 1)) 
  else:   
    exec('{} = {}'.format(dist_element, 0)) 

features = {'room_number': room_number, 
            'DK': DK ,
            'K': K,
            'L': L,
            'S': S,
            'convenience':conv_out,
            'new':新築じゃないとイヤ,
            'old':こだわりなし,
            'far':やや遠い,
            'near':やや近い,
            'very far':遠い,
            'very near':とても近い,
            '世田谷区':世田谷区,
            '中央区':中央区,
            '中野区':中野区,
            '北区':北区,
            '千代田区':千代田区,
            '台東区':台東区, 
            '品川区':品川区,
            '墨田区':墨田区,
            '大田区':大田区,
            '文京区':文京区,
            '新宿区':新宿区,
            '板橋区':板橋区,
            '江戸川区':江戸川区,
            '江東区':江東区,
            '渋谷区':渋谷区,
            '港区':港区,
            '目黒区':目黒区,
            '練馬区':練馬区,
            '荒川区':荒川区,
            '葛飾区':葛飾区,
            '豊島区':豊島区, 
            '足立区':足立区,
            }
features_df  = pd.DataFrame([features])

st.table(features_df)  
#予測ボタンを押したら→クオリティーを出力
if st.button('Predict'):
    
    prediction = predict_quality(model, features_df)
    
    st.write(' あなたのお探しの物件の平均家賃は '+ str(prediction)+'円です')
   
   