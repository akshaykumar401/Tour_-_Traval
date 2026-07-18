import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

url = "http://127.0.0.1:8000/admin/send-emails/"
# Let's post to the view directly!
# But we need CSRF.
# Let's write a django management command or script to test the view logic.
