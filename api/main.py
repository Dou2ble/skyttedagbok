import flask as fl


from so import so
from api import api

app = fl.Flask(__name__)
app.register_blueprint(so, url_prefix="/api/so")
app.register_blueprint(api, url_prefix="/api")



if __name__ == "__main__":
    app.run(debug=True, port=8080)