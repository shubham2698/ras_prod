from flask import Flask
from ras.config import Config

app = Flask(__name__)
app.config.from_object(Config)


from ras import routes