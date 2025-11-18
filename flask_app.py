from application import create_app
from application.extensions import db
import os

app = create_app('ProductionConfig')
