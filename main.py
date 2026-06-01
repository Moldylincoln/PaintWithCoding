from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    print("received") 
    return "received"

app.run(host='0.0.0.0', port=8080)
