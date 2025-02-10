import os
from datetime import datetime
from typing import Dict, Optional

import zhipuai
from loguru import logger

from .base import BaseLLM

class ZhipuLLM(BaseLLM):
    """智谱AI LLM实现"""

    def __init__(self):
        """初始化智谱AI客户端"""
        super().__init__()
        api_key = os.getenv("ZHIPUAI_API_KEY")
        api_key = "b36dfc57dc8d4ed49eae828a917687a1.OzMaHx87fXf1UsS1"
        if not api_key:
            raise ValueError("ZHIPUAI_API_KEY environment variable is not set")
        zhipuai.api_key = api_key

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
            response = zhipuai.model_api.invoke(
                model="chatglm_turbo",
                prompt=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                top_p=0.9,
                max_tokens=2000
            )
            
            # 检查响应状态
            if response["code"] != 200:
                logger.error(f"Zhipu API error: {response}")
                return "抱歉，分析过程中出现错误，请稍后重试。"
            
            # 提取分析结果
            analysis = response["data"]["choices"][0]["content"]
            
            return analysis

        except Exception as e:
            logger.exception("Error while analyzing bazi with Zhipu AI")
            return f"分析过程中发生错误: {str(e)}"
