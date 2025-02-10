import gradio as gr
from datetime import datetime
from typing import Dict, Type
import asyncio
from loguru import logger

from ..bazi.calculator import BaziCalculator
from ..llm.base import BaseLLM
from ..llm.zhipu import ZhipuLLM
# from ..llm.qwen import QwenLLM

class FortuneTellingUI:
    """八字算命界面类"""
    
    def __init__(self):
        """初始化界面"""
        self.calculator = BaziCalculator()
        self.llm_models: Dict[str, Type[BaseLLM]] = {
            "智谱 AI": ZhipuLLM,
            # "通义千问": QwenLLM,
        }

    def create_interface(self) -> gr.Blocks:
        """创建Gradio界面"""
        with gr.Blocks(title="AI 八字算命", theme=gr.themes.Soft()) as interface:
            gr.Markdown("""
            # 神算机 (The Augury Machine)
            
            欢迎使用AI八字算命系统！请输入您的出生信息，选择想要使用的AI模型，系统将为您提供详细的命理分析。
            """)
            
            with gr.Row():
                with gr.Column():
                    # 输入部分
                    birth_date = gr.Textbox(
                        label="出生日期",
                        placeholder="YYYY-MM-DD",
                        info="请输入您的出生日期，格式：YYYY-MM-DD"
                    )
                    birth_time = gr.Textbox(
                        label="出生时间",
                        placeholder="HH:MM",
                        info="请输入您的出生时间，格式：HH:MM（24小时制）"
                    )
                    model_choice = gr.Dropdown(
                        choices=list(self.llm_models.keys()),
                        label="选择AI模型",
                        value="智谱 AI"
                    )
                    analyze_btn = gr.Button("开始分析", variant="primary")
                
                with gr.Column():
                    # 显示八字信息
                    bazi_info = gr.Textbox(
                        label="您的八字",
                        interactive=False
                    )
                    elements_info = gr.Textbox(
                        label="五行分布",
                        interactive=False
                    )
            
            # 分析结果
            with gr.Row():
                analysis_result = gr.Markdown(
                    value="请点击\"开始分析\"按钮获取命理分析结果。"
                )
            
            async def analyze(date: str, time: str, model_name: str) -> tuple:
                """分析八字并返回结果"""
                try:
                    # 解析日期时间
                    birth_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
                    
                    # 计算八字
                    bazi = self.calculator.calculate_bazi(birth_datetime)
                    bazi_str = self.calculator.format_bazi(bazi)
                    
                    # 分析五行
                    elements = self.calculator.analyze_five_elements_distribution(bazi)
                    elements_str = " ".join([f"{k}:{v}" for k, v in elements.items()])
                    
                    # 获取LLM分析
                    llm_class = self.llm_models[model_name]
                    llm = llm_class()
                    analysis = await llm.analyze_bazi(birth_datetime, bazi_str, elements)
                    
                    return bazi_str, elements_str, analysis
                
                except ValueError as e:
                    logger.error(f"Input error: {e}")
                    return "", "", f"输入格式错误：{str(e)}"
                except Exception as e:
                    logger.exception("Analysis error")
                    return "", "", f"分析过程中发生错误：{str(e)}"
            
            analyze_btn.click(
                fn=analyze,
                inputs=[birth_date, birth_time, model_choice],
                outputs=[bazi_info, elements_info, analysis_result]
            )
            
            gr.Markdown("""
            ### 使用说明
            
            1. 输入您的出生日期（格式：YYYY-MM-DD）
            2. 输入您的出生时间（格式：HH:MM，24小时制）
            3. 选择想要使用的AI模型
            4. 点击"开始分析"按钮获取分析结果
            
            ### 注意事项
            
            - 请确保输入准确的出生时间，这将直接影响分析结果的准确性
            - 不同的AI模型可能会给出不同的分析视角
            - 分析结果仅供参考，请理性对待
            """)
        
        return interface

    def launch(self, **kwargs):
        """启动Gradio界面"""
        interface = self.create_interface()
        interface.launch(**kwargs)
