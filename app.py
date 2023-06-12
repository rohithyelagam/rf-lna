from flask import Flask, request, render_template
import pickle
import pandas as pd
import os

TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
model = pickle.load(open('model.pkl', 'rb'))
data = pd.read_csv('data.csv')

def encode(temp,data):
    ans = []
    x=0
    for col in ['operating_frequency','S11 (dB20)','S21 (dB20)','NF (dB10)']:
        ans.append((temp[x]-min(data[col]))/(max(data[col])-min(data[col])))
        x=x+1
    return ans

def decode(temp,data):
    ans = []
    x=0
    for col in ['Lg','Ls','Ld','W']:
        ans.append(temp[x]*(max(data[col])-min(data[col]))+min(data[col]))
        x=x+1
    return ans

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict',methods=['POST'])
def predict():
    """Grabs the input values and uses them to make prediction"""
    opfreq = float(request.form["opfreq"])
    s11 = float(request.form["s11"])
    s21 = float(request.form["s21"])
    nf = float(request.form["nf"])

    output = decode(model.predict([encode([opfreq,s11,s21,nf],data)])[0],data)
    print(output[0])
    return render_template('index.html', lg=f'{output[0]}',ls=f'{output[1]}',ld=f'{output[2]}',w=f'{output[3]}')

if __name__ == "__main__":
    app.run()