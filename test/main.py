# これはflaskのテストファイルです
from flask import Flask, render_template

app = Flask(__name__)

CERTFILE = "C://ssl/certificate/location"
KEYFILE = "C://ssl/key/location"
context = (CERTFILE, KEYFILE)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=context)

