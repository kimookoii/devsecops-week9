import logging
import os
from flask import Flask

app = Flask(__name__)

LOG_DIR = "/app"
LOG_FILE = "/app/app.log"

# pastikan folder log ada
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

@app.route("/")
def home():
    app.logger.info("User accessed home page")
    return "Hello DevSecOps"

@app.route("/login")
def login():
    app.logger.warning("Failed login attempt")
    return "Login failed"

@app.route("/error")
def error():
    app.logger.error("Application error occurred")
    return 1 / 0

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
