from flask import Flask
from restapi.resources import fast_text_api
app = Flask(__name__)

url_pref = "/metubot/v1"

app.register_blueprint(fast_text_api.fast_text, url_prefix=url_pref)

def run():

    try:
        app.run(host="0.0.0.0", port="8080", debug=False)

    except:
        app.run()

if __name__ == "__main__":
    print("server started")
    run()
