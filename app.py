from flask import Flask
app = Flask(__name__)

@app.route('/')
def inici():
    return "L'aplicació de Flask funciona!"

if __name__ == '__main__':
    app.run(debug=True)