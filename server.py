from main import *
from flask import Flask, request, abort

#MySecretCredentials
email = 'testie.testieson@gmail.com'
password = 'ScrapingStuff2022!'

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        company_name = request.json['company_name']
        prospect_email = request.json['prospect_email']
        driver = create_webdriver()
        linkedin_login(email,password,driver)
        dict = create_single_company_dict(company_name,driver)
        dict['prospect_email'] = prospect_email
        print(dict)
        driver.close()
        #post_webhook('https://hooks.zapier.com/hooks/catch/2597417/bnt0msn/', data_dict=dict)
        return 'success', 200
    else:
        abort(400)

if __name__ == "__main__": app.run()
