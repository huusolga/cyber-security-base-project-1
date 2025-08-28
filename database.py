from os import getenv
from app import app
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = "bf1f2fcec822b67461c6c2d108694427"
db = SQLAlchemy(app)
