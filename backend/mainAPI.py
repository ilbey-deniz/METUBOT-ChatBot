from flask import Flask
app = Flask(__name__)

url_pref = "/metubot/v1"

def run():

    try:
        app.run(host="0.0.0.0", port="8080", debug=False)

    except:
        app.run()

if __name__ == "__main__":
    print("server started")
    run()
