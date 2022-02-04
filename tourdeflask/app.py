# Import třídy Flask z knihovny flsk
from flask import Flask

# Vytvoření app objektu, který tvoří jádro naší aplikace
# (Pro zajemce: wsgi aplikace)
app = Flask(__name__)


# Při zadání 127.0.0.1:5000/ se spustí funkce hello. V tomto kontextu se o ní bavíme jako o view.
@app.route('/')
def hello():
    return 'Welcome to Tour de Flask!\nThe tour will start on 1st July 2022'
