from app import app
import os
from dotenv import load_dotenv

load_dotenv()



if __name__ == '__main__':
  PORT = int(os.getenv('PORT', 8000))
  app.run(host='0.0.0.0', port=PORT, debug=True)