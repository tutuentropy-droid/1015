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


class DataSource(str, Enum):
    OFFICIAL = "官方就业报告"
    THIRD_PARTY = "第三方统计"


class EmploymentCityDistribution(BaseModel):
    city: str
    province: str
    count: int
    percentage: float
    avg_salary: Optional[int] = None


class EmploymentIndustryDistribution(BaseModel):
    industry: str
    count: int
    percentage: float
    avg_salary: Optional[int] = None


class EmploymentPositionDistribution(BaseModel):
    position_type: str
    count: int
    percentage: float
    avg_salary: Optional[int] = None


class EmploymentDataDetail(BaseModel):
    college_id: str
    college_name: str
    year: int
    total_graduates: int
    employment_rate: float
    average_salary: int
    data_source: DataSource
    city_distribution: List[EmploymentCityDistribution] = []
    industry_distribution: List[EmploymentIndustryDistribution] = []
    position_distribution: List[EmploymentPositionDistribution] = []
    note: Optional[str] = None


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
    employment_data: Optional[EmploymentDataDetail] = None


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


class DisciplineCategory(str, Enum):
    SCIENCE = "理学"
    ENGINEERING = "工学"
    AGRICULTURE = "农学"
    MEDICINE = "医学"
    LITERATURE = "文学"
    LAW = "法学"
    ECONOMICS = "经济学"
    MANAGEMENT = "管理学"
    ART = "艺术学"
    EDUCATION = "教育学"
    HISTORY = "历史学"
    PHILOSOPHY = "哲学"


class StudyDifficulty(str, Enum):
    EASY = "轻松"
    MODERATE = "适中"
    HARD = "较难"
    VERY_HARD = "非常难"


class EmploymentProspect(str, Enum):
    EXCELLENT = "极好"
    GOOD = "良好"
    NORMAL = "一般"
    POOR = "较差"


class SalaryRange(BaseModel):
    fresh: int
    three_years: int
    five_years_plus: int


class MajorDetail(BaseModel):
    id: str
    name: str
    category: DisciplineCategory
    major_type: str
    brief_intro: str
    introduction: str
    core_courses: List[str]
    employment_direction: List[str]
    typical_positions: List[str]
    salary_range: SalaryRange
    employment_rate: float
    postgraduate_ratio: float
    suitable_traits: List[str]
    unsuitable_people: List[str]
    study_difficulty: StudyDifficulty
    course_load: str
    gender_ratio: str
    employment_prospect: EmploymentProspect
    subject_requirements: List[str] = []


class SubjectRequirementRule(BaseModel):
    major_id: str
    major_name: str
    province: str
    required_subjects: List[str] = []
    optional_subjects: List[str] = []
    requirement_note: Optional[str] = None


class SubjectAnalysisRequest(BaseModel):
    subjects: List[str]
    province: Optional[str] = None
    college_ids: List[str] = []


class MajorEligibility(BaseModel):
    major: Major
    eligible: bool
    reason: Optional[str] = None
    college_id: Optional[str] = None
    college_name: Optional[str] = None


class DisciplineGroup(BaseModel):
    category: str
    majors: List[MajorEligibility] = []
    eligible_count: int = 0
    total_count: int = 0


class SubjectAnalysisResult(BaseModel):
    subjects: List[str]
    total_majors: int = 0
    eligible_majors: int = 0
    ineligible_majors: int = 0
    eligible_rate: float = 0.0
    discipline_groups: List[DisciplineGroup] = []
    college_stats: List[Dict] = []


class CombinationCompareRequest(BaseModel):
    combinations: List[List[str]]
    province: Optional[str] = None
    college_ids: List[str] = []


class CombinationCompareItem(BaseModel):
    combination: List[str]
    combination_label: str
    total_majors: int = 0
    eligible_majors: int = 0
    ineligible_majors: int = 0
    eligible_rate: float = 0.0
    by_college: List[Dict] = []


class CombinationCompareResult(BaseModel):
    items: List[CombinationCompareItem] = []


class MonteCarloHistogramBin(BaseModel):
    bin_start: float
    bin_end: float
    count: int
    probability: float


class MonteCarloCollegeResult(BaseModel):
    college_id: str
    college_name: str
    base_probability: float
    simulated_probability_mean: float
    simulated_probability_std: float
    simulated_probability_median: float
    ci_lower_95: float
    ci_upper_95: float
    ci_lower_90: float
    ci_upper_90: float
    min_simulated_probability: float
    max_simulated_probability: float
    histogram_bins: List[MonteCarloHistogramBin]
    stability_score: float
    volatility_rating: str


class MonteCarloRequest(BaseModel):
    college_ids: List[str]
    user_score: int
    user_rank: int
    province: str
    subject_combination: Optional[str] = None
    num_simulations: int = Field(default=1000, ge=100, le=10000)
    num_bins: int = Field(default=20, ge=5, le=50)


class MonteCarloResponse(BaseModel):
    results: List[MonteCarloCollegeResult]
    num_simulations: int
    common_bins: List[float]


class SimulationStepType(str, Enum):
    RETRIEVE = "检索志愿"
    THRESHOLD_CHECK = "投档线判断"
    MAJOR_CHECK = "专业分数线判断"
    ADJUSTMENT = "调剂判断"
    ADMITTED = "录取成功"
    WITHDRAW = "退档"
    NEXT_VOLUNTEER = "进入下一志愿"


class SimulationStep(BaseModel):
    step_index: int
    step_type: SimulationStepType
    volunteer_order: int
    college_name: str
    major_name: Optional[str] = None
    title: str
    description: str
    user_score: Optional[int] = None
    user_rank: Optional[int] = None
    threshold_score: Optional[int] = None
    threshold_rank: Optional[int] = None
    passed: Optional[bool] = None
    is_final: bool = False


class SimulationResult(BaseModel):
    success: bool
    admitted_college: Optional[str] = None
    admitted_major: Optional[str] = None
    admitted_order: Optional[int] = None
    steps: List[SimulationStep]
    summary: str


class SimulationVolunteerItem(BaseModel):
    order: int
    college_id: str
    college_name: str
    major_id: Optional[str] = None
    major_name: Optional[str] = None
    accept_adjustment: bool = True


class SimulationRequest(BaseModel):
    province: str
    score: int
    rank: int
    subject_combination: Optional[str] = None
    volunteers: List[SimulationVolunteerItem]
    reference_year: Optional[int] = 2025
