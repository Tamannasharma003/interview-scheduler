from flask import Flask

app = Flask(__name__)

# Import webhook routes AFTER creating app
import webhook

if __name__ == "__main__":
    app.run()


