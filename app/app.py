from flask import Flask

app = Flask(__name__)

from flask import Flask

app = Flask(__name__)




# ✅ IMPORTANT: import AFTER app creation
from webhook import *

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


