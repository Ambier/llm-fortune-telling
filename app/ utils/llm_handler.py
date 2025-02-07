
import openai
import zhipuai
from app import app

def get_llm_response(model_name, fortune_type, data):
    if model_name == 'openai':
        return get_openai_response(fortune_type, data)
    elif model_name == 'zhipu':
        return get_zhipu_response(fortune_type, data)
    # Add more models as needed
    
def get_openai_response(fortune_type, data):
    openai.api_key = app.config['OPENAI_API_KEY']
    
    if fortune_type == "bazi":
        prompt = f"Based on the following Bazi calculation results, provide a detailed fortune reading:\n{data}"
    else:
        prompt = f"Based on the following Ziwei Doushu calculation results, provide a detailed fortune reading:\n{data}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an experienced Chinese fortune teller."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

# Add similar functions for other LLM providers
