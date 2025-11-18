from application import create_app
from application.extensions import db
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = create_app('ProductionConfig')

