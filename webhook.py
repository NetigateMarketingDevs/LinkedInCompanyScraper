import requests
import json

webhook_url ='https://hooks.zapier.com/hooks/catch/2597417/bntf8ur/'

data = {'company_name':'siemens','prospect_email':'marcello-trottier@web.de'}

def post_webhook(webhook_url, data):
    response = requests.post(webhook_url, data=json.dumps(data),headers={'Content-Type':'application/json'})
    return print(response)

post_webhook('http://127.0.0.1:5000/webhook',data)