from abc import ABC, abstractmethod
from typing import Dict, Optional
import os
from datetime import datetime

class BaseLLM(ABC):
    """基础LLM类，定义与大语言模型交互的接口"""

    def __init__(self):
        """初始化基础LLM类"""
        self.system_prompt = """你是一位经验丰富的命理大师，精通八字算命。
你需要根据用户的生辰八字信息，结合五行生克制化理论，对命主人的性格特征、事业发展、感情状况等方面进行分析。
请确保你的分析：
1. 专业且严谨，运用传统命理学的核心理论
2. 语言平实易懂，避免过于专业的术语
3. 重点分析命局特点和关键信息
4. 建议和引导要积极正面，避免过于消极的预测
"""

    @abstractmethod
    async def analyze_bazi(
        self,
        birth_time: datetime,
        bazi_str: str,
        five_elements: Dict[str, int]
    ) -> str:
        """分析八字并返回解读结果"""
        pass

    def _format_birth_info(self, birth_time: datetime) -> str:
        """格式化出生信息"""
        return birth_time.strftime("%Y年%m月%d日 %H时")

    def _format_analysis_prompt(
        self,
        birth_time: datetime,
        bazi_str: str,
        five_elements: Dict[str, int]
    ) -> str:
        """格式化分析提示"""
        birth_info = self._format_birth_info(birth_time)
        elements_info = " ".join([f"{k}:{v}" for k, v in five_elements.items()])
        
        return f"""请根据以下信息进行八字命理分析：

出生信息：{birth_info}
八字：{bazi_str}
五行分布：{elements_info}

请从以下方面进行分析：
1. 命局特征：分析八字组合的特点，以及五行的分布情况
2. 性格分析：根据八字特征分析性格优势和潜在短板
3. 事业发展：分析适合的事业方向和发展机会
4. 财运分析：分析财运特点和理财建议
5. 感情姻缘：分析感情特征和桃花运势
6. 健康提醒：根据五行分布提供健康建议

请给出详细的分析结果。"""
