from wordcounter.config import *
from wordcounter.application import app

# print Config.HOST
app.run(host=DevelopmentConfig.HOST, debug=True)
