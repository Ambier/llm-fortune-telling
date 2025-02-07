import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    ZHIPU_API_KEY = os.environ.get('ZHIPU_API_KEY')
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
