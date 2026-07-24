from flask import Flask, jsonify, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
load_dotenv()  

# SMTP Server Configurations (Example using Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Credentials
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER') 
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER')

mail = Mail(app)

@app.route('/')
def index():
  return jsonify({'message': 'Welcome to the Mail Service API!'})


# Is HTML code or plain text
def is_html(content):
  soup = BeautifulSoup(content, 'html.parser')
  return bool(soup.find())

@app.route('/send-mail', methods=['POST'])
def send_mail():
  email_data = request.get_json()
  recipients = email_data.get('recipients')
  body = email_data.get('body')
  subject = email_data.get('subject')
  
  print(recipients, body, subject)
  print(type(recipients), type(body), type(subject))
  
  # Validating the input data
  if not body or not subject or not recipients:
    return jsonify({
      "error": "Missing required fields: body, subject, and recipients are required.",
      "data": None,
      "status": 400
    }), 400

  # Sending the email
  try:
    msg = Message(
      subject=subject,
      recipients=[recipients],
    )
    # Validating is the body contains HTML or plain text
    if is_html(body):
      msg.html = body
    else:
      msg.body = body
    mail.send(msg)
    return jsonify({
      'message': 'Email sent successfully!',
      'data': None,
      'status': 200
    }), 200
  except Exception as e:
    print(e)
    return jsonify({
      'error': str(e),
      'data': None,
      'status': 500
    }), 500
  
  