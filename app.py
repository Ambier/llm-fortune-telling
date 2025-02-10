import os
from dotenv import load_dotenv
from loguru import logger
import asyncio

from src.ui.interface import FortuneTellingUI

def setup_logging():
    """配置日志"""
    logger.add(
        "logs/app.log",
        rotation="500 MB",
        retention="10 days",
        level="INFO",
        encoding="utf-8"
    )

def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()
    
    # 配置日志
    os.makedirs("logs", exist_ok=True)
    setup_logging()
    
    logger.info("Starting Fortune Telling Application...")
    
    try:
        # 创建并启动UI
        ui = FortuneTellingUI()
        ui.launch(
            server_name="0.0.0.0",  # 允许外部访问
            server_port=7860,
            share=True,  # 创建公开可访问的链接
        )
        
    except Exception as e:
        logger.exception("Application error")
        raise

if __name__ == "__main__":
    main()
