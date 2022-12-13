from main import *
from flask import Flask, request, abort


app = Flask(__name__)

email = ask_for_linkedin_username()
password = ask_for_linkedin_password()
driver = create_webdriver()
linkedin_login(email, password, driver)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        company_name = request.json['company_name']
        prospect_email = request.json['prospect_email']
        dict = create_single_company_dict(company_name,driver)
        dict['prospect_email'] = prospect_email
        print(dict)
        linkedin_go_to_home_page(driver)
        return 'success', 200
    else:
        abort(400)

if __name__ == "__main__": app.run()
