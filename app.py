print("Click on link to open the app : http://127.0.0.1:5000/ ")

from flask import Flask, render_template, request
from main import process_query

app = Flask(__name__)

def get_bot_response(user_input):
    return process_query(user_input)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = get_bot_response(user_input)
    return response

if __name__ == '__main__':
    app.run(debug=True)


