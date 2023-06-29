from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
import pandas as pd
from datetime import date, timedelta


def one_day_data():
    url = 'https://api.open-meteo.com/v1/forecast?latitude=21.97&longitude=96.08&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,surface_pressure,windspeed_10m&forecast_days=1&timezone=auto'
    data = pd.read_json(url)
    return data

def rain_predict(data):
    rain_model = tf.keras.models.load_model(r"C:\Users\nyans\Documents\weather_forecast\saved_model\rain_model")
    rain_label = ['No rain', 'Light rain', 'Moderate rain', 'Heavy rain']
    
    data = pd.DataFrame(data)
    data = tf.convert_to_tensor(data)
    percents = rain_model.predict(data)
    score = tf.nn.softmax(percents[0])
    score = list(np.array(score))
    percents = list(percents[0])
    print(percents)
    label = percents.index(max(percents))
    print(rain_label[label])
    return str(round(max(score)*100, 2))+'% '+rain_label[label], rain_label[label]

def model_predict():
    
    min_t_model = tf.keras.models.load_model(r"C:\Users\nyans\Documents\weather_forecast\saved_model\min_temp_model")
    max_t_model = tf.keras.models.load_model(r"C:\Users\nyans\Documents\weather_forecast\saved_model\max_temp_model")
    
    # api from  "https://open-meteo.com/"
    url = 'https://api.open-meteo.com/v1/forecast?latitude=21.97&longitude=96.08&daily=temperature_2m_max,temperature_2m_min&past_days=30&forecast_days=1&timezone=auto'
    data = pd.read_json(url)
    json_max_temp = data['daily']['temperature_2m_max']
    max_t_prediction = max_t_model.predict([json_max_temp[-30:]])[0][0]
    print('The prediction of the highest temperature for tomorrow is ' , round(max_t_prediction, 3), '*C')
    
    print()
    
    json_min_temp = data['daily']['temperature_2m_min']
    min_t_prediction = min_t_model.predict([json_min_temp[-30:]])[0][0]
    print('The prediction of the lowest temperature for tomorrow is ', round(min_t_prediction, 3), '*C') 

    a = json_max_temp.copy()

    for i in range(6):
        prediction = max_t_model.predict([a[-30:]])[0][0]
        a.append(prediction)
        print(prediction)
        
        
    b = json_min_temp.copy()

    for i in range(6):
        prediction = min_t_model.predict([b[-30:]])[0][0]
        b.append(prediction)
        print(prediction)
        
        
    pdate = data['daily']['time']
    
    previous_lis = []
    for i in range(len(a[-31:])):
        xy_d = {}
        xy_d['x'] = pdate[i]
        y_lis = [int(a[i]),int(b[i])]
        y_lis.sort()
        xy_d['y'] = y_lis
        previous_lis.append(xy_d)
    
    # Get today's date
    today = date.today()
    
    # Calculate dates for the next five days
    next_five_days = [str(today + timedelta(days=i)) for i in range(6)]
    max_t = []
    min_t = []
    future_lis = []
    for i in range(len(a[31:])):
        xy_d = {}
        xy_d['x'] = next_five_days[i]
        y_lis = [int(a[31+i]),int(b[31+i])]
        max_t.append(round(a[31+i], 2))
        min_t.append(round(b[31+i], 2))
        y_lis.sort()
        xy_d['y'] = y_lis
        future_lis.append(xy_d)
    
    print(future_lis)

    return future_lis, previous_lis, next_five_days, max_t, min_t
  
def cloud_image_chooser(t):
    if t < 30:
        path = 'static/icons/large_cloud.png'
    elif t >= 30 and t < 32:
        path = 'static/icons/small_cloud.png'
    else:
        path = 'static/icons/no_cloud.png'
    
    return path
  
app = Flask(__name__)

@app.route('/')
def home():
    
    data = one_day_data()
    year, month, day = data['hourly']['time'][-1][:10].split('-')
    
    max_temp = max(data['hourly']['temperature_2m'])
    min_temp = min(data['hourly']['temperature_2m'])
    avg_temp = round(sum(data['hourly']['temperature_2m'])/len(data['hourly']['temperature_2m']), 2)
    
    max_hum = max(data['hourly']['relativehumidity_2m'])
    min_hum = min(data['hourly']['relativehumidity_2m'])
    avg_hum = round(sum(data['hourly']['relativehumidity_2m'])/len(data['hourly']['relativehumidity_2m']), 2)
    
    max_dp = max(data['hourly']['dewpoint_2m'])
    min_dp = min(data['hourly']['dewpoint_2m'])
    avg_dp = round(sum(data['hourly']['dewpoint_2m'])/len(data['hourly']['dewpoint_2m']), 2)
    

    avg_ws = round(sum(data['hourly']['windspeed_10m'])/len(data['hourly']['windspeed_10m']), 2)
    avg_p =  round(sum(data['hourly']['surface_pressure'])/len(data['hourly']['surface_pressure']), 2)
    
    
    
    df = {
        'Max_Temperature':[max_temp],
        'Avg_Temperature':[avg_temp], 
        'Min_Temperature':[min_temp], 
        'Max_Dew Point':[max_dp], 
        'Avg_Dew Point':[avg_dp], 
        'Min_Dew Point':[min_dp], 
        'Max_Humidity':[max_hum], 
        'Avg_Humidity':[avg_hum], 
        'Min_Humidity':[min_hum]
    }
    
    p_label, label = rain_predict(df)
    print(label)
    print(avg_dp, avg_hum, avg_temp, avg_ws)
    
    future_lis, previous_lis, next_five_days, max_t, min_t = model_predict()
    
    
    t1 = (max_t[1]+min_t[1])/2
    t2 = (max_t[2]+min_t[2])/2
    t3 = (max_t[3]+min_t[3])/2
    t4 = (max_t[4]+min_t[4])/2
    t5 = (max_t[5]+min_t[5])/2  
    
    d1_img = cloud_image_chooser(t1)
    d2_img = cloud_image_chooser(t2)
    d3_img = cloud_image_chooser(t3)
    d4_img = cloud_image_chooser(t4)
    d5_img = cloud_image_chooser(t5)
    
    print(t1, t2, t3, t4, t5)
    
    return render_template('index.html',
                           future_lis = future_lis,
                           previous_lis = previous_lis,
                           today_date = next_five_days[0],
                           d1 = next_five_days[1],
                           d2 = next_five_days[2],
                           d3 = next_five_days[3],
                           d4 = next_five_days[4],
                           d5 = next_five_days[5],
                           d1_img = d1_img,
                           d2_img = d2_img,
                           d3_img = d3_img,
                           d4_img = d4_img,
                           d5_img = d5_img,
                           max_t1 = max_t[1],
                           max_t2 = max_t[2],
                           max_t3 = max_t[3],   
                           max_t4 = max_t[4],
                           max_t5 = max_t[5],
                           min_t1 = min_t[1],
                           min_t2 = min_t[2],
                           min_t3 = min_t[3],
                           min_t4 = min_t[4],
                           min_t5 = min_t[5],
                           avg_dp = avg_dp,
                           avg_hum = avg_hum,
                           avg_temp = avg_temp,
                           avg_wind = avg_ws,
                           avg_p = avg_p,
                           rain = p_label,
                           rlabel = label,
                           )


    
if __name__ == '__main__':
    app.run()
