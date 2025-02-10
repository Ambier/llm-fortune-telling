from datetime import datetime
from typing import Dict, Tuple, List

class BaziCalculator:
    """八字计算器：用于将公历日期转换为天干地支"""
    
    # 天干
    HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    
    # 地支
    EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 五行
    FIVE_ELEMENTS = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }
    
    # 地支五行
    BRANCH_ELEMENTS = {
        "寅": "木", "卯": "木",
        "巳": "火", "午": "火",
        "辰": "土", "戌": "土", "丑": "土", "未": "土",
        "申": "金", "酉": "金",
        "子": "水", "亥": "水"
    }
    
    def __init__(self):
        """初始化八字计算器"""
        pass

    def get_year_pillar(self, year: int) -> Tuple[str, str]:
        """计算年柱"""
        stem_index = (year - 4) % 10
        branch_index = (year - 4) % 12
        return self.HEAVENLY_STEMS[stem_index], self.EARTHLY_BRANCHES[branch_index]

    def get_month_pillar(self, year_stem: str, month: int) -> Tuple[str, str]:
        """计算月柱"""
        # 确定月干偏移
        stem_offset = {
            "甲": 0, "己": 0,
            "乙": 2, "庚": 2,
            "丙": 4, "辛": 4,
            "丁": 6, "壬": 6,
            "戊": 8, "癸": 8
        }
        
        # 计算月干
        month_stem_index = (stem_offset[year_stem] + month - 1) % 10
        # 计算月支（寅月为正月）
        month_branch_index = (month + 1) % 12
        
        return self.HEAVENLY_STEMS[month_stem_index], self.EARTHLY_BRANCHES[month_branch_index]

    def get_day_pillar(self, date: datetime) -> Tuple[str, str]:
        """计算日柱"""
        # 计算距离1900年1月31日的天数
        base_date = datetime(1900, 1, 31)
        days = (date - base_date).days
        
        stem_index = days % 10
        branch_index = days % 12
        
        return self.HEAVENLY_STEMS[stem_index], self.EARTHLY_BRANCHES[branch_index]

    def get_hour_pillar(self, day_stem: str, hour: int) -> Tuple[str, str]:
        """计算时柱"""
        # 将小时转换为地支时辰
        branch_index = hour // 2 % 12
        
        # 根据日干确定时干的起始偏移
        stem_offset = {
            "甲": 0, "己": 5,
            "乙": 2, "庚": 7,
            "丙": 4, "辛": 9,
            "丁": 6, "壬": 1,
            "戊": 8, "癸": 3
        }
        
        stem_index = (stem_offset[day_stem] + branch_index) % 10
        return self.HEAVENLY_STEMS[stem_index], self.EARTHLY_BRANCHES[branch_index]

    def calculate_bazi(self, birth_time: datetime) -> Dict[str, Tuple[str, str]]:
        """计算完整八字"""
        # 获取年柱
        year_stem, year_branch = self.get_year_pillar(birth_time.year)
        
        # 获取月柱
        month_stem, month_branch = self.get_month_pillar(year_stem, birth_time.month)
        
        # 获取日柱
        day_stem, day_branch = self.get_day_pillar(birth_time)
        
        # 获取时柱
        hour_stem, hour_branch = self.get_hour_pillar(day_stem, birth_time.hour)
        
        return {
            "year": (year_stem, year_branch),
            "month": (month_stem, month_branch),
            "day": (day_stem, day_branch),
            "hour": (hour_stem, hour_branch)
        }

    def get_five_elements(self, bazi: Dict[str, Tuple[str, str]]) -> List[str]:
        """获取八字中的五行属性"""
        elements = []
        for pillar in bazi.values():
            stem, branch = pillar
            elements.append(self.FIVE_ELEMENTS[stem])
            elements.append(self.BRANCH_ELEMENTS[branch])
        return elements

    def format_bazi(self, bazi: Dict[str, Tuple[str, str]]) -> str:
        """格式化八字输出"""
        result = []
        for pillar_name, (stem, branch) in bazi.items():
            result.append(f"{stem}{branch}")
        return " ".join(result)

    def analyze_five_elements_distribution(self, bazi: Dict[str, Tuple[str, str]]) -> Dict[str, int]:
        """分析八字中五行的分布"""
        elements = self.get_five_elements(bazi)
        distribution = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        for element in elements:
            distribution[element] += 1
        return distribution
