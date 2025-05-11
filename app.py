from flask import Flask, request
import os
from twilio.rest import Client
import openai

app = Flask(__name__)

# Load secrets
twilio = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_AUTH'))
openai.api_key = os.getenv('OPENAI_KEY')

@app.route('/sms', methods=['POST'])
def sms():
    symptoms = request.form['Body']
    ai_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": "Provide 2 possible medical conditions."
        }, {
            "role": "user",
            "content": symptoms
        }]
    )
    
    twilio.messages.create(
        body=ai_response.choices[0].message.content,
        from_=os.getenv('TWILIO_NUMBER'),
        to=request.form['From']
    )
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)