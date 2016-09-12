from flask import Flask

app = Flask(__name__)

import restaurate.views
import restaurate.database