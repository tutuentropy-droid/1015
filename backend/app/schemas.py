from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal
from enum import Enum


class Province(str, Enum):
    BEIJING = "北京"
    SHANGHAI = "上海"
    GUANGDONG = "广东"
    JIANGSU = "江苏"
    ZHEJIANG = "浙江"
    SHANDONG = "山东"
    HENAN = "河南"
    SICHUAN = "四川"
    HUBEI = "湖北"
    HUNAN = "湖南"
    HEBEI = "河北"
    ANHUI = "安徽"
    FUJIAN = "福建"
    SHAANXI = "陕西"
    LIAONING = "辽宁"
    CHONGQING = "重庆"
    TIANJIN = "天津"
    JIANGXI = "江西"
    GUANGXI = "广西"
    YUNNAN = "云南"
    GUIZHOU = "贵州"
    SHANXI = "山西"
    HEILONGJIANG = "黑龙江"
    JILIN = "吉林"
    NEIMENGGU = "内蒙古"
    XINJIANG = "新疆"
    GANSU = "甘肃"
    HAINAN = "海南"
    NINGXIA = "宁夏"
    QINGHAI = "青海"
    XIZANG = "西藏"


class CollegeLevel(str, Enum):
    C9 = "C9联盟"
    PROJECT_985 = "985工程"
    PROJECT_211 = "211工程"
    DOUBLE_FIRST_CLASS = "双一流"
    ORDINARY = "普通本科"


class CollegeType(str, Enum):
    COMPREHENSIVE = "综合类"
    SCIENCE = "理工类"
    NORMAL = "师范类"
    AGRICULTURAL = "农林类"
    MEDICAL = "医药类"
    FINANCE = "财经类"
    POLITICAL = "政法类"
    LANGUAGE = "语言类"
    ART = "艺术类"
    SPORT = "体育类"
    MILITARY = "军事类"


class SubjectCombination(str, Enum):
    PHYSICS_CHEMISTRY_BIOLOGY = "物理+化学+生物"
    PHYSICS_CHEMISTRY_GEOGRAPHY = "物理+化学+地理"
    PHYSICS_CHEMISTRY_POLITICS = "物理+化学+政治"
    PHYSICS_BIOLOGY_GEOGRAPHY = "物理+生物+地理"
    PHYSICS_BIOLOGY_POLITICS = "物理+生物+政治"
    PHYSICS_GEOGRAPHY_POLITICS = "物理+地理+政治"
    HISTORY_GEOGRAPHY_POLITICS = "历史+地理+政治"
    HISTORY_BIOLOGY_POLITICS = "历史+生物+政治"
    HISTORY_BIOLOGY_GEOGRAPHY = "历史+生物+地理"
    HISTORY_CHEMISTRY_POLITICS = "历史+化学+政治"
    HISTORY_CHEMISTRY_BIOLOGY = "历史+化学+生物"
    HISTORY_CHEMISTRY_GEOGRAPHY = "历史+化学+地理"


class Category(str, Enum):
    REACH = "冲"
    STABLE = "稳"
    SAFE = "保"


class AdmissionData(BaseModel):
    year: int
    province: str
    score: int
    rank: int
    batch: str
    subject_combination: Optional[str] = None


class DisciplineLevel(str, Enum):
    A_PLUS = "A+"
    A = "A"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B = "B"
    B_MINUS = "B-"
    C_PLUS = "C+"
    C = "C"
    C_MINUS = "C-"


class Major(BaseModel):
    id: str
    name: str
    subject_requirements: List[str]
    employment_direction: List[str]
    typical_positions: List[str]
    description: Optional[str] = None
    discipline_level: Optional[DisciplineLevel] = None


class College(BaseModel):
    id: str
    name: str
    province: str
    city: str
    level: CollegeLevel
    college_type: CollegeType
    description: Optional[str] = None
    majors: List[Major] = []
    admission_data: List[AdmissionData] = []
    tags: List[str] = []
    employment_rate: Optional[float] = None
    average_salary: Optional[int] = None


class UserInput(BaseModel):
    province: str
    score: int
    rank: int
    subject_combination: str
    acceptable_cities: List[str] = []
    target_major_directions: List[str] = []
    accept_adjustment: bool = True
    volunteer_count: int = Field(default=10, ge=1, le=30)


class CollegePrediction(BaseModel):
    college: College
    predicted_rank: int
    predicted_score: int
    probability: float
    category: Category
    size_year_pattern: str
    adjustment_impact: str
    recent_admission_data: List[AdmissionData]
    matching_majors: List[Major] = []


class VolunteerItem(BaseModel):
    order: int
    college: College
    probability: float
    category: Category
    predicted_rank: int
    predicted_score: int
    recommended_major: Major
    size_year_pattern: str
    adjustment_impact: str


class VolunteerPlan(BaseModel):
    user_input: UserInput
    volunteers: List[VolunteerItem]
    reach_count: int
    stable_count: int
    safe_count: int
    overall_success_probability: float
