from flask import render_template, request, jsonify
from app import app
from app.utils.bazi_calculator import calculate_bazi
from app.utils.ziwei_calculator import calculate_ziwei
from app.utils.llm_handler import get_llm_response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bazi', methods=['GET', 'POST'])
def bazi():
    if request.method == 'POST':
        data = request.json
        birth_year = data.get('year')
        birth_month = data.get('month')
        birth_day = data.get('day')
        birth_time = data.get('time')
        model = data.get('model', 'openai')
        
        bazi_result = calculate_bazi(birth_year, birth_month, birth_day, birth_time)
        fortune_reading = get_llm_response(model, "bazi", bazi_result)
        
        return jsonify({
            'bazi': bazi_result,
            'reading': fortune_reading
        })
    
    return render_template('bazi.html')

@app.route('/ziwei', methods=['GET', 'POST'])
def ziwei():
    if request.method == 'POST':
        data = request.json
        birth_info = data.get('birth_info')
        model = data.get('model', 'openai')
        
        ziwei_result = calculate_ziwei(birth_info)
        fortune_reading = get_llm_response(model, "ziwei", ziwei_result)
        
        return jsonify({
            'ziwei': ziwei_result,
            'reading': fortune_reading
        })
    
    return render_template('ziwei.html')
