import os
from datetime import datetime
from typing import Dict, Optional

from zhipuai import ZhipuAI
from loguru import logger

from .base import BaseLLM

class ZhipuLLM(BaseLLM):
    """智谱AI LLM实现"""

    def __init__(self):
        """初始化智谱AI客户端"""
        super().__init__()
        api_key = os.getenv("ZHIPUAI_API_KEY")
        if not api_key:
            raise ValueError("ZHIPUAI_API_KEY environment variable is not set")
        self.client=ZhipuAI(api_key=api_key)

    async def analyze_bazi(
        self,
        birth_time: datetime,
        bazi_str: str,
        five_elements: Dict[str, int]
    ) -> str:
        """使用智谱AI分析八字"""
        try:
            # 构建分析提示
            prompt = self._format_analysis_prompt(birth_time, bazi_str, five_elements)
            
            # 调用智谱AI API
            response = self.client.chat.completions.create(
                    model="chatglm_turbo",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                temperature=0.7,
                top_p=0.9,
                max_tokens=2000)

            analysis = response.choices[0].message.content.strip()
            return analysis

        except Exception as e:
            logger.exception("Error while analyzing bazi with Zhipu AI")
            return f"分析过程中发生错误: {str(e)}"
