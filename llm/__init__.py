# src/llm/__init__.py
"""
LLM集成模块
"""

from .base import BaseLLM
from .zhipu import ZhipuLLM

__all__ = ['BaseLLM', 'ZhipuLLM']
