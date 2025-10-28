from mangum import Mangum
import sys
import os
from api.app import app  

handler = Mangum(app)
