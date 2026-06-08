import random
from typing import List, Dict, Optional
from .schemas import (
    College, Major, AdmissionData, CollegeLevel, CollegeType, DisciplineLevel,
    MajorDetail, DisciplineCategory, StudyDifficulty, EmploymentProspect, SalaryRange
)

random.seed(42)


MAJOR_DATABASE: Dict[str, Dict] = {
    "计算机科学与技术": {
        "subject_requirements": ["物理"],
        "employment_direction": ["互联网/IT行业", "人工智能", "软件开发", "数据分析", "信息安全"],
        "typical_positions": ["软件工程师", "算法工程师", "数据分析师", "产品经理", "系统架构师"],
        "description": "研究计算机系统与软件应用的核心学科",
        "directions": ["计算机", "IT", "软件", "人工智能", "互联网"],
    },
    "软件工程": {
        "subject_requirements": ["物理"],
        "employment_direction": ["软件开发", "互联网", "金融科技", "企业信息化"],
        "typical_positions": ["后端开发工程师", "前端开发工程师", "全栈工程师", "测试工程师", "运维工程师"],
        "description": "系统学习软件开发与工程化方法",
        "directions": ["计算机", "IT", "软件", "互联网"],
    },
    "人工智能": {
        "subject_requirements": ["物理", "化学"],
        "employment_direction": ["人工智能", "机器学习", "计算机视觉", "自然语言处理", "自动驾驶"],
        "typical_positions": ["AI算法工程师", "机器学习工程师", "CV工程师", "NLP工程师", "深度学习研究员"],
        "description": "前沿的AI交叉学科",
        "directions": ["计算机", "IT", "人工智能", "互联网"],
    },
    "数据科学与大数据技术": {
        "subject_requirements": ["物理"],
        "employment_direction": ["数据分析", "大数据", "商业智能", "数据挖掘", "云计算"],
        "typical_positions": ["数据科学家", "大数据工程师", "BI分析师", "数据产品经理", "数据挖掘工程师"],
        "description": "聚焦海量数据处理与分析",
        "directions": ["计算机", "IT", "数据", "互联网"],
    },
    "电子信息工程": {
        "subject_requirements": ["物理"],
        "employment_direction": ["通信", "半导体", "消费电子", "物联网", "航空航天"],
        "typical_positions": ["硬件工程师", "嵌入式工程师", "通信工程师", "IC设计工程师", "FPGA工程师"],
        "description": "信息技术与电子系统的基础学科",
        "directions": ["电子", "通信", "IT"],
    },
    "通信工程": {
        "subject_requirements": ["物理"],
        "employment_direction": ["5G/6G通信", "互联网", "运营商", "通信设备", "卫星通信"],
        "typical_positions": ["通信工程师", "射频工程师", "网络优化工程师", "5G算法工程师", "传输工程师"],
        "description": "通信系统与网络技术",
        "directions": ["电子", "通信", "IT"],
    },
    "自动化": {
        "subject_requirements": ["物理"],
        "employment_direction": ["智能制造", "机器人", "工业控制", "自动驾驶", "物联网"],
        "typical_positions": ["自动化工程师", "机器人工程师", "控制算法工程师", "PLC工程师", "工业互联网工程师"],
        "description": "自动控制与智能系统",
        "directions": ["自动化", "智能制造", "机器人"],
    },
    "机器人工程": {
        "subject_requirements": ["物理"],
        "employment_direction": ["机器人", "智能制造", "自动驾驶", "服务机器人", "工业机器人"],
        "typical_positions": ["机器人算法工程师", "机械设计工程师", "SLAM工程师", "运动控制工程师", "机器人应用工程师"],
        "description": "机器人系统设计与开发",
        "directions": ["自动化", "机器人", "智能制造"],
    },
    "机械工程": {
        "subject_requirements": ["物理", "化学"],
        "employment_direction": ["装备制造", "汽车", "航空航天", "新能源", "轨道交通"],
        "typical_positions": ["机械设计工程师", "工艺工程师", "结构工程师", "CAE工程师", "生产工程师"],
        "description": "机械装备设计与制造",
        "directions": ["机械", "制造", "汽车", "航空"],
    },
    "车辆工程": {
        "subject_requirements": ["物理"],
        "employment_direction": ["新能源汽车", "传统汽车", "智能网联", "汽车零部件", "轨道交通"],
        "typical_positions": ["汽车设计工程师", "新能源工程师", "智能驾驶工程师", "底盘工程师", "汽车电子工程师"],
        "description": "汽车设计与制造",
        "directions": ["机械", "汽车", "新能源"],
    },
    "航空航天工程": {
        "subject_requirements": ["物理", "化学"],
        "employment_direction": ["航空航天", "国防军工", "卫星", "民航", "航天科工"],
        "typical_positions": ["飞行器设计工程师", "航空发动机工程师", "结构强度工程师", "航电工程师", "发射场工程师"],
        "description": "航空与航天飞行器设计",
        "directions": ["航空", "航天", "军工"],
    },
    "材料科学与工程": {
        "subject_requirements": ["物理", "化学"],
        "employment_direction": ["新材料", "半导体", "新能源", "冶金", "高端制造"],
        "typical_positions": ["材料工程师", "半导体工艺工程师", "新能源材料研究员", "材料测试工程师", "金相工程师"],
        "description": "材料研发与应用",
        "directions": ["材料", "新能源", "半导体"],
    },
    "新能源材料与器件": {
        "subject_requirements": ["物理", "化学"],
        "employment_direction": ["新能源", "动力电池", "光伏", "储能", "半导体"],
        "typical_positions": ["电池研发工程师", "光伏工程师", "储能工程师", "材料研究员", "器件工程师"],
        "description": "新能源材料与储能器件",
        "directions": ["材料", "新能源"],
    },
    "化学工程与工艺": {
        "subject_requirements": ["物理", "化学"],
        "employment_direction": ["石油化工", "精细化工", "医药", "新材料", "环境保护"],
        "typical_positions": ["化工工程师", "工艺工程师", "研发工程师", "生产管理", "EHS工程师"],
        "description": "化学工艺与工业生产",
        "directions": ["化工", "石油", "医药"],
    },
    "药学": {
        "subject_requirements": ["物理", "化学", "生物"],
        "employment_direction": ["医药研发", "制药", "药品监管", "临床药学", "医药代表"],
        "typical_positions": ["药物研发工程师", "制剂工程师", "分析研究员", "临床药师", "药政注册"],
        "description": "药物发现与开发",
        "directions": ["医药", "生物", "化学"],
    },
    "临床医学": {
        "subject_requirements": ["物理", "化学", "生物"],
        "employment_direction": ["医院临床", "医学科研", "医药企业", "医疗器械", "医疗AI"],
        "typical_positions": ["临床医生", "医学研究员", "医药研发", "医学影像医师", "医疗AI专家"],
        "description": "临床诊断与治疗",
        "directions": ["医学", "医药", "生物"],
    },
    "口腔医学": {
        "subject_requirements": ["物理", "化学", "生物"],
        "employment_direction": ["口腔医院", "牙科诊所", "医疗器械", "种植牙", "口腔材料"],
        "typical_positions": ["口腔科医生", "正畸医生", "种植医生", "口腔修复医师", "口腔产品经理"],
        "description": "口腔疾病诊疗",
        "directions": ["医学", "医药"],
    },
    "中医学": {
        "subject_requirements": ["物理", "化学", "生物"],
        "employment_direction": ["中医院", "中药研发", "中医养生", "针灸推拿", "中西医结合"],
        "typical_positions": ["中医师", "针灸师", "中药师", "养生顾问", "中医科研"],
        "description": "传统中医诊疗",
        "directions": ["医学", "中医", "医药"],
    },
    "金融学": {
        "subject_requirements": [],
        "employment_direction": ["银行", "证券", "基金", "保险", "金融科技"],
        "typical_positions": ["投资分析师", "银行客户经理", "基金经理", "风控专员", "量化研究员"],
        "description": "金融市场与投融资",
        "directions": ["金融", "经济", "商科"],
    },
    "经济学": {
        "subject_requirements": [],
        "employment_direction": ["宏观经济研究", "金融", "咨询", "政府机关", "企业战略"],
        "typical_positions": ["经济分析师", "政策研究员", "咨询顾问", "投资研究员", "数据分析师"],
        "description": "经济理论与应用",
        "directions": ["金融", "经济", "商科"],
    },
    "会计学": {
        "subject_requirements": [],
        "employment_direction": ["四大会计师事务所", "企业财务", "审计", "税务", "投资银行"],
        "typical_positions": ["会计师", "审计师", "财务分析师", "税务专员", "CFO"],
        "description": "会计、审计与财务管理",
        "directions": ["金融", "商科", "财务"],
    },
    "法学": {
        "subject_requirements": [],
        "employment_direction": ["律师事务所", "公司法务", "法院检察院", "政府法制", "合规"],
        "typical_positions": ["律师", "法官", "检察官", "公司法务", "合规专员"],
        "description": "法律理论与实务",
        "directions": ["法律", "法学"],
    },
    "汉语言文学": {
        "subject_requirements": [],
        "employment_direction": ["教育", "新媒体", "出版", "公务员", "品牌策划"],
        "typical_positions": ["语文教师", "新媒体编辑", "文案策划", "出版社编辑", "行政文秘"],
        "description": "中文语言文学",
        "directions": ["文学", "教育", "传媒"],
    },
    "英语": {
        "subject_requirements": [],
        "employment_direction": ["翻译", "外贸", "教育", "跨境电商", "跨国企业"],
        "typical_positions": ["翻译", "外贸业务员", "英语教师", "跨境运营", "国际商务"],
        "description": "英语语言与文化",
        "directions": ["语言", "外语", "教育", "外贸"],
    },
    "新闻学": {
        "subject_requirements": [],
        "employment_direction": ["传统媒体", "新媒体", "公关", "广告", "企业传播"],
        "typical_positions": ["记者", "编辑", "新媒体运营", "公关专员", "广告策划"],
        "description": "新闻传播与媒介",
        "directions": ["传媒", "新闻", "新媒体"],
    },
    "数学与应用数学": {
        "subject_requirements": ["物理"],
        "employment_direction": ["金融量化", "教育", "数据分析", "科研", "算法"],
        "typical_positions": ["量化分析师", "数学教师", "数据科学家", "算法研究员", "精算师"],
        "description": "数学理论与应用",
        "directions": ["数学", "教育", "金融"],
    },
    "物理学": {
        "subject_requirements": ["物理"],
        "employment_direction": ["科研", "半导体", "光学", "教育", "新能源"],
        "typical_positions": ["物理研究员", "半导体工程师", "光学工程师", "物理教师", "量子计算研究员"],
        "description": "物理理论与实验",
        "directions": ["物理", "教育", "科研", "半导体"],
    },
    "生物科学": {
        "subject_requirements": ["物理", "化学", "生物"],
        "employment_direction": ["生物医药", "基因检测", "农业", "科研", "食品"],
        "typical_positions": ["生物研究员", "测序分析师", "发酵工程师", "生物信息工程师", "生物教师"],
        "description": "生命科学研究",
        "directions": ["生物", "医药", "科研"],
    },
    "心理学": {
        "subject_requirements": [],
        "employment_direction": ["心理咨询", "教育", "人力资源", "用户研究", "精神卫生"],
        "typical_positions": ["心理咨询师", "心理教师", "HRBP", "用户研究员", "临床心理学家"],
        "description": "心理科学与应用",
        "directions": ["心理", "教育", "HR"],
    },
    "建筑学": {
        "subject_requirements": ["物理"],
        "employment_direction": ["建筑设计", "城市规划", "房地产", "景观设计", "室内设计"],
        "typical_positions": ["建筑设计师", "规划师", "景观设计师", "房地产策划", "BIM工程师"],
        "description": "建筑设计与城市规划",
        "directions": ["建筑", "设计", "房地产"],
    },
    "土木工程": {
        "subject_requirements": ["物理"],
        "employment_direction": ["建筑施工", "房地产", "基础设施", "市政工程", "工程咨询"],
        "typical_positions": ["土建工程师", "项目经理", "结构设计师", "造价工程师", "监理工程师"],
        "description": "土木工程设计与施工",
        "directions": ["建筑", "土木", "房地产"],
    },
    "工商管理": {
        "subject_requirements": [],
        "employment_direction": ["企业管理", "咨询", "人力资源", "市场营销", "创业"],
        "typical_positions": ["管理培训生", "咨询顾问", "HR经理", "市场经理", "运营经理"],
        "description": "企业经营管理",
        "directions": ["商科", "管理", "HR"],
    },
    "市场营销": {
        "subject_requirements": [],
        "employment_direction": ["互联网运营", "广告", "品牌", "快消", "数字营销"],
        "typical_positions": ["市场经理", "品牌经理", "运营专员", "广告策划", "增长黑客"],
        "description": "市场营销与品牌管理",
        "directions": ["商科", "市场", "互联网"],
    },
    "人力资源管理": {
        "subject_requirements": [],
        "employment_direction": ["企业HR", "猎头", "咨询", "劳务派遣", "组织发展"],
        "typical_positions": ["HRBP", "招聘经理", "薪酬专员", "培训专员", "猎头顾问"],
        "description": "人力资源开发与管理",
        "directions": ["商科", "HR", "管理"],
    },
    "电子商务": {
        "subject_requirements": [],
        "employment_direction": ["电商运营", "跨境电商", "直播电商", "互联网产品", "供应链"],
        "typical_positions": ["电商运营", "直播运营", "跨境运营", "产品经理", "供应链专员"],
        "description": "电子商务与数字商务",
        "directions": ["商科", "互联网", "电商"],
    },
    "统计学": {
        "subject_requirements": ["物理"],
        "employment_direction": ["金融", "数据科学", "生物统计", "市场研究", "政府统计"],
        "typical_positions": ["数据分析师", "统计学家", "精算师", "数据科学家", "BI工程师"],
        "description": "统计理论与数据分析",
        "directions": ["数学", "数据", "金融"],
    },
    "地理信息科学": {
        "subject_requirements": ["物理"],
        "employment_direction": ["GIS开发", "地图导航", "智慧城市", "自然资源", "遥感"],
        "typical_positions": ["GIS开发工程师", "遥感数据分析师", "地图产品经理", "智慧城市工程师", "测绘工程师"],
        "description": "地理信息与空间技术",
        "directions": ["计算机", "GIS", "地理"],
    },
    "环境工程": {
        "subject_requirements": ["物理", "化学", "生物"],
        "employment_direction": ["环保", "水务", "固废处理", "大气治理", "ESG咨询"],
        "typical_positions": ["环保工程师", "水处理工程师", "环评工程师", "ESG顾问", "环境监测"],
        "description": "环境污染治理与生态保护",
        "directions": ["环保", "环境", "化工"],
    },
    "农业工程": {
        "subject_requirements": ["物理", "化学", "生物"],
        "employment_direction": ["智慧农业", "农业科技", "农机装备", "食品加工", "乡村振兴"],
        "typical_positions": ["农业工程师", "智慧农业产品经理", "农机设计工程师", "食品工程师", "农业技术员"],
        "description": "农业工程与现代农业",
        "directions": ["农业", "机械"],
    },
    "林学": {
        "subject_requirements": ["物理", "化学", "生物"],
        "employment_direction": ["林业", "生态保护", "园林", "自然保护", "碳汇"],
        "typical_positions": ["林业工程师", "园林设计师", "生态保护员", "碳汇项目经理", "自然保护区管理"],
        "description": "森林培育与生态保护",
        "directions": ["农业", "林业", "环保"],
    },
    "水产养殖学": {
        "subject_requirements": ["物理", "化学", "生物"],
        "employment_direction": ["水产养殖", "海洋科技", "渔业", "水产品加工", "海洋保护"],
        "typical_positions": ["水产养殖技术员", "水产营养师", "海洋生物研究员", "水产品质检", "渔业管理"],
        "description": "水产养殖与海洋生物",
        "directions": ["农业", "水产", "海洋"],
    },
    "海洋科学": {
        "subject_requirements": ["物理", "化学", "生物"],
        "employment_direction": ["海洋科研", "海洋油气", "海洋保护", "港口", "极地研究"],
        "typical_positions": ["海洋科学家", "海洋工程师", "海洋生物研究员", "海油工程师", "港口工程师"],
        "description": "海洋科学与技术",
        "directions": ["海洋", "科研"],
    },
    "大气科学": {
        "subject_requirements": ["物理"],
        "employment_direction": ["气象", "民航", "环保", "气候研究", "新能源"],
        "typical_positions": ["气象预报员", "气候研究员", "航空气象工程师", "大气环境工程师", "新能源气象评估"],
        "description": "大气与气象科学",
        "directions": ["气象", "环保", "科研"],
    },
    "历史学": {
        "subject_requirements": [],
        "employment_direction": ["教育", "文博", "文化遗产", "新媒体", "公务员"],
        "typical_positions": ["历史教师", "博物馆馆员", "文化遗产研究员", "历史自媒体", "文旅策划"],
        "description": "历史研究与文化传承",
        "directions": ["历史", "教育", "文博"],
    },
    "哲学": {
        "subject_requirements": [],
        "employment_direction": ["科研", "教育", "公务员", "出版", "咨询"],
        "typical_positions": ["哲学研究员", "大学教师", "公务员", "出版社编辑", "战略咨询"],
        "description": "哲学思维与思辨",
        "directions": ["哲学", "教育", "科研"],
    },
    "社会学": {
        "subject_requirements": [],
        "employment_direction": ["社会工作", "民政", "NGO", "市场研究", "用户研究"],
        "typical_positions": ["社会工作者", "社区工作者", "用户研究员", "政策研究员", "民政公务员"],
        "description": "社会研究与公共服务",
        "directions": ["社会", "公共服务", "HR"],
    },
    "政治学与行政学": {
        "subject_requirements": [],
        "employment_direction": ["公务员", "政策研究", "行政管理", "新闻", "高校"],
        "typical_positions": ["公务员", "政策研究员", "行政专员", "党政干部", "高校辅导员"],
        "description": "政治与公共行政",
        "directions": ["政治", "公务员", "管理"],
    },
    "国际经济与贸易": {
        "subject_requirements": [],
        "employment_direction": ["外贸", "跨境电商", "跨国公司", "海关", "国际金融"],
        "typical_positions": ["外贸业务员", "跨境运营", "报关员", "国际采购", "涉外律师"],
        "description": "国际贸易与商务",
        "directions": ["经济", "外贸", "金融"],
    },
    "物流管理": {
        "subject_requirements": [],
        "employment_direction": ["物流", "供应链", "电商", "快递", "航运"],
        "typical_positions": ["供应链经理", "物流专员", "仓储经理", "采购经理", "航运操作"],
        "description": "现代物流与供应链管理",
        "directions": ["商科", "物流", "供应链"],
    },
    "旅游管理": {
        "subject_requirements": [],
        "employment_direction": ["旅游景区", "酒店", "OTA", "文旅策划", "会展"],
        "typical_positions": ["景区运营", "酒店经理", "旅游产品经理", "文旅策划师", "会展策划"],
        "description": "旅游与酒店管理",
        "directions": ["商科", "旅游", "酒店"],
    },
    "播音与主持艺术": {
        "subject_requirements": [],
        "employment_direction": ["广播电视", "新媒体", "商业主持", "配音", "公关"],
        "typical_positions": ["主持人", "主播", "配音演员", "商业主持人", "视频博主"],
        "description": "播音主持与有声语言",
        "directions": ["传媒", "艺术", "新媒体"],
    },
    "视觉传达设计": {
        "subject_requirements": [],
        "employment_direction": ["广告", "互联网", "品牌", "出版", "UI设计"],
        "typical_positions": ["平面设计师", "UI设计师", "品牌设计师", "插画师", "动效设计师"],
        "description": "视觉设计与品牌传播",
        "directions": ["艺术", "设计", "互联网"],
    },
    "环境设计": {
        "subject_requirements": [],
        "employment_direction": ["室内设计", "景观设计", "建筑设计", "软装", "展览展示"],
        "typical_positions": ["室内设计师", "景观设计师", "软装设计师", "展览设计师", "建筑效果图"],
        "description": "空间与环境艺术设计",
        "directions": ["艺术", "设计", "建筑"],
    },
    "音乐表演": {
        "subject_requirements": [],
        "employment_direction": ["演出团体", "音乐教育", "音乐制作", "新媒体", "文化传播"],
        "typical_positions": ["职业演奏家", "音乐教师", "音乐制作人", "声乐指导", "音乐博主"],
        "description": "音乐表演与创作",
        "directions": ["艺术", "音乐", "教育"],
    },
    "美术学": {
        "subject_requirements": [],
        "employment_direction": ["美术教育", "美术创作", "艺术策展", "文化遗产", "新媒体艺术"],
        "typical_positions": ["美术教师", "职业艺术家", "美术馆策展人", "文创设计师", "美术评论家"],
        "description": "美术理论与创作",
        "directions": ["艺术", "美术", "教育"],
    },
    "运动训练": {
        "subject_requirements": [],
        "employment_direction": ["职业体育", "体育教育", "健身", "运动康复", "赛事运营"],
        "typical_positions": ["职业运动员", "体育教师", "健身教练", "康复师", "赛事运营"],
        "description": "竞技体育与训练",
        "directions": ["体育", "教育", "健身"],
    },
    "社会体育指导与管理": {
        "subject_requirements": [],
        "employment_direction": ["全民健身", "健身俱乐部", "社区体育", "体育培训", "体育产业"],
        "typical_positions": ["健身教练", "体育培训师", "社区体育指导员", "俱乐部运营", "体育赛事策划"],
        "description": "社会体育与全民健身",
        "directions": ["体育", "健身"],
    },
    "侦查学": {
        "subject_requirements": ["物理", "化学", "生物"],
        "employment_direction": ["公安机关", "国家安全", "检察系统", "司法鉴定", "企业合规"],
        "typical_positions": ["刑事警察", "经侦民警", "司法鉴定人", "反舞弊专员", "国家安全干部"],
        "description": "刑事侦查与司法鉴定",
        "directions": ["公安", "政法", "法律"],
    },
    "治安学": {
        "subject_requirements": [],
        "employment_direction": ["公安机关", "保安管理", "企业安保", "应急管理", "城市管理"],
        "typical_positions": ["治安民警", "派出所民警", "安保总监", "应急管理专员", "城市管理执法"],
        "description": "社会治安管理",
        "directions": ["公安", "政法", "管理"],
    },
}


COLLEGE_TEMPLATES = [
    {"name": "清华大学", "province": "北京", "city": "北京", "level": CollegeLevel.C9, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 100, "base_score": 680, "tags": ["顶尖名校", "C9", "985", "211", "双一流A类"]},
    {"name": "北京大学", "province": "北京", "city": "北京", "level": CollegeLevel.C9, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 150, "base_score": 678, "tags": ["顶尖名校", "C9", "985", "211", "双一流A类"]},
    {"name": "浙江大学", "province": "浙江", "city": "杭州", "level": CollegeLevel.C9, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 800, "base_score": 660, "tags": ["顶尖名校", "C9", "985", "211", "双一流A类"]},
    {"name": "上海交通大学", "province": "上海", "city": "上海", "level": CollegeLevel.C9, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 600, "base_score": 665, "tags": ["顶尖名校", "C9", "985", "211", "双一流A类"]},
    {"name": "复旦大学", "province": "上海", "city": "上海", "level": CollegeLevel.C9, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 700, "base_score": 663, "tags": ["顶尖名校", "C9", "985", "211", "双一流A类"]},
    {"name": "南京大学", "province": "江苏", "city": "南京", "level": CollegeLevel.C9, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 1200, "base_score": 652, "tags": ["顶尖名校", "C9", "985", "211", "双一流A类"]},
    {"name": "中国科学技术大学", "province": "安徽", "city": "合肥", "level": CollegeLevel.C9, "college_type": CollegeType.SCIENCE, "base_rank": 1000, "base_score": 655, "tags": ["顶尖名校", "C9", "985", "211", "双一流A类"]},
    {"name": "哈尔滨工业大学", "province": "黑龙江", "city": "哈尔滨", "level": CollegeLevel.C9, "college_type": CollegeType.SCIENCE, "base_rank": 2500, "base_score": 635, "tags": ["顶尖名校", "C9", "985", "211", "双一流A类"]},
    {"name": "西安交通大学", "province": "陕西", "city": "西安", "level": CollegeLevel.C9, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 2800, "base_score": 630, "tags": ["顶尖名校", "C9", "985", "211", "双一流A类"]},
    {"name": "中国人民大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 1500, "base_score": 648, "tags": ["名校", "985", "211", "双一流A类", "人文社科强"]},
    {"name": "北京航空航天大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.SCIENCE, "base_rank": 1800, "base_score": 645, "tags": ["名校", "985", "211", "双一流A类", "航空航天强"]},
    {"name": "同济大学", "province": "上海", "city": "上海", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 2000, "base_score": 642, "tags": ["名校", "985", "211", "双一流A类", "建筑强"]},
    {"name": "武汉大学", "province": "湖北", "city": "武汉", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 3000, "base_score": 628, "tags": ["名校", "985", "211", "双一流A类"]},
    {"name": "华中科技大学", "province": "湖北", "city": "武汉", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.SCIENCE, "base_rank": 3200, "base_score": 626, "tags": ["名校", "985", "211", "双一流A类"]},
    {"name": "中山大学", "province": "广东", "city": "广州", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 3500, "base_score": 623, "tags": ["名校", "985", "211", "双一流A类"]},
    {"name": "四川大学", "province": "四川", "city": "成都", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 4500, "base_score": 615, "tags": ["名校", "985", "211", "双一流A类"]},
    {"name": "山东大学", "province": "山东", "city": "济南", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 4200, "base_score": 618, "tags": ["名校", "985", "211", "双一流A类"]},
    {"name": "吉林大学", "province": "吉林", "city": "长春", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 5500, "base_score": 605, "tags": ["名校", "985", "211", "双一流A类"]},
    {"name": "东南大学", "province": "江苏", "city": "南京", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.SCIENCE, "base_rank": 2800, "base_score": 630, "tags": ["名校", "985", "211", "双一流A类", "建筑强"]},
    {"name": "厦门大学", "province": "福建", "city": "厦门", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 3800, "base_score": 620, "tags": ["名校", "985", "211", "双一流A类", "校园美丽"]},
    {"name": "北京师范大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.NORMAL, "base_rank": 2200, "base_score": 640, "tags": ["名校", "985", "211", "双一流A类", "师范强"]},
    {"name": "华东师范大学", "province": "上海", "city": "上海", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.NORMAL, "base_rank": 3000, "base_score": 628, "tags": ["名校", "985", "211", "双一流A类", "师范强"]},
    {"name": "南开大学", "province": "天津", "city": "天津", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 2500, "base_score": 635, "tags": ["名校", "985", "211", "双一流A类"]},
    {"name": "天津大学", "province": "天津", "city": "天津", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.SCIENCE, "base_rank": 3200, "base_score": 626, "tags": ["名校", "985", "211", "双一流A类"]},
    {"name": "中南大学", "province": "湖南", "city": "长沙", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.SCIENCE, "base_rank": 4800, "base_score": 612, "tags": ["名校", "985", "211", "双一流A类"]},
    {"name": "湖南大学", "province": "湖南", "city": "长沙", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 4000, "base_score": 619, "tags": ["名校", "985", "211", "双一流A类"]},
    {"name": "重庆大学", "province": "重庆", "city": "重庆", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.SCIENCE, "base_rank": 4200, "base_score": 618, "tags": ["名校", "985", "211", "双一流A类"]},
    {"name": "电子科技大学", "province": "四川", "city": "成都", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.SCIENCE, "base_rank": 3600, "base_score": 622, "tags": ["名校", "985", "211", "双一流A类", "IT强"]},
    {"name": "大连理工大学", "province": "辽宁", "city": "大连", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.SCIENCE, "base_rank": 4500, "base_score": 615, "tags": ["名校", "985", "211", "双一流A类"]},
    {"name": "东北大学", "province": "辽宁", "city": "沈阳", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.SCIENCE, "base_rank": 5800, "base_score": 603, "tags": ["名校", "985", "211", "双一流B类"]},
    {"name": "兰州大学", "province": "甘肃", "city": "兰州", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 6500, "base_score": 598, "tags": ["名校", "985", "211", "双一流A类"]},
    {"name": "西北工业大学", "province": "陕西", "city": "西安", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.SCIENCE, "base_rank": 3500, "base_score": 623, "tags": ["名校", "985", "211", "双一流A类", "航空航天强"]},
    {"name": "西北农林科技大学", "province": "陕西", "city": "咸阳", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.AGRICULTURAL, "base_rank": 7500, "base_score": 590, "tags": ["985", "211", "双一流B类", "农林强"]},
    {"name": "中国农业大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.AGRICULTURAL, "base_rank": 4000, "base_score": 619, "tags": ["名校", "985", "211", "双一流A类", "农林强"]},
    {"name": "中国海洋大学", "province": "山东", "city": "青岛", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 5500, "base_score": 605, "tags": ["985", "211", "双一流A类", "海洋强"]},
    {"name": "中央民族大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 7000, "base_score": 593, "tags": ["985", "211", "双一流A类", "民族类"]},
    {"name": "北京理工大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.SCIENCE, "base_rank": 2600, "base_score": 633, "tags": ["名校", "985", "211", "双一流A类"]},
    {"name": "华南理工大学", "province": "广东", "city": "广州", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.SCIENCE, "base_rank": 3800, "base_score": 620, "tags": ["名校", "985", "211", "双一流A类"]},
    {"name": "北京协和医学院", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_985, "college_type": CollegeType.MEDICAL, "base_rank": 2000, "base_score": 642, "tags": ["名校", "双一流", "医学顶尖"]},
    {"name": "上海财经大学", "province": "上海", "city": "上海", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.FINANCE, "base_rank": 2200, "base_score": 640, "tags": ["名校", "211", "双一流", "财经强"]},
    {"name": "中央财经大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.FINANCE, "base_rank": 2800, "base_score": 630, "tags": ["名校", "211", "双一流", "财经强"]},
    {"name": "对外经济贸易大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.FINANCE, "base_rank": 3200, "base_score": 626, "tags": ["名校", "211", "双一流", "经贸强"]},
    {"name": "北京邮电大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 2500, "base_score": 635, "tags": ["名校", "211", "双一流", "信息通信强"]},
    {"name": "上海外国语大学", "province": "上海", "city": "上海", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.LANGUAGE, "base_rank": 3500, "base_score": 623, "tags": ["名校", "211", "双一流", "外语强"]},
    {"name": "北京外国语大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.LANGUAGE, "base_rank": 3200, "base_score": 626, "tags": ["名校", "211", "双一流", "外语强"]},
    {"name": "中国政法大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.POLITICAL, "base_rank": 3000, "base_score": 628, "tags": ["名校", "211", "双一流", "政法强"]},
    {"name": "华北电力大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 5500, "base_score": 605, "tags": ["211", "双一流", "电力强"]},
    {"name": "北京交通大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 4200, "base_score": 618, "tags": ["211", "双一流", "交通强"]},
    {"name": "北京科技大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 4000, "base_score": 619, "tags": ["211", "双一流", "材料冶金强"]},
    {"name": "南京航空航天大学", "province": "江苏", "city": "南京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 4500, "base_score": 615, "tags": ["211", "双一流", "航空航天强"]},
    {"name": "南京理工大学", "province": "江苏", "city": "南京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 4800, "base_score": 612, "tags": ["211", "双一流", "军工强"]},
    {"name": "西安电子科技大学", "province": "陕西", "city": "西安", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 4200, "base_score": 618, "tags": ["211", "双一流", "电子信息强"]},
    {"name": "华东理工大学", "province": "上海", "city": "上海", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 5000, "base_score": 610, "tags": ["211", "双一流", "化工强"]},
    {"name": "东华大学", "province": "上海", "city": "上海", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 6000, "base_score": 602, "tags": ["211", "双一流", "纺织服装强"]},
    {"name": "上海大学", "province": "上海", "city": "上海", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 5500, "base_score": 605, "tags": ["211", "双一流", "地方强校"]},
    {"name": "苏州大学", "province": "江苏", "city": "苏州", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 5200, "base_score": 608, "tags": ["211", "双一流", "地方强校"]},
    {"name": "暨南大学", "province": "广东", "city": "广州", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 5000, "base_score": 610, "tags": ["211", "双一流", "华侨第一校"]},
    {"name": "西南财经大学", "province": "四川", "city": "成都", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.FINANCE, "base_rank": 4800, "base_score": 612, "tags": ["211", "双一流", "财经强"]},
    {"name": "中南财经政法大学", "province": "湖北", "city": "武汉", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.FINANCE, "base_rank": 5000, "base_score": 610, "tags": ["211", "双一流", "财经政法强"]},
    {"name": "武汉理工大学", "province": "湖北", "city": "武汉", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 5200, "base_score": 608, "tags": ["211", "双一流", "材料交通强"]},
    {"name": "中国地质大学", "province": "湖北", "city": "武汉", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 6000, "base_score": 602, "tags": ["211", "双一流", "地学强"]},
    {"name": "华中师范大学", "province": "湖北", "city": "武汉", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.NORMAL, "base_rank": 5500, "base_score": 605, "tags": ["211", "双一流", "师范强"]},
    {"name": "华中农业大学", "province": "湖北", "city": "武汉", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.AGRICULTURAL, "base_rank": 6500, "base_score": 598, "tags": ["211", "双一流", "农林强"]},
    {"name": "东北师范大学", "province": "吉林", "city": "长春", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.NORMAL, "base_rank": 6000, "base_score": 602, "tags": ["211", "双一流", "师范强"]},
    {"name": "哈尔滨工程大学", "province": "黑龙江", "city": "哈尔滨", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 5800, "base_score": 603, "tags": ["211", "双一流", "船舶军工强"]},
    {"name": "西南交通大学", "province": "四川", "city": "成都", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 5500, "base_score": 605, "tags": ["211", "双一流", "交通强"]},
    {"name": "西南大学", "province": "重庆", "city": "重庆", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.NORMAL, "base_rank": 6000, "base_score": 602, "tags": ["211", "双一流", "师范农业"]},
    {"name": "陕西师范大学", "province": "陕西", "city": "西安", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.NORMAL, "base_rank": 6800, "base_score": 596, "tags": ["211", "双一流", "师范强"]},
    {"name": "西北大学", "province": "陕西", "city": "西安", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 5800, "base_score": 603, "tags": ["211", "双一流", "地方强校"]},
    {"name": "郑州大学", "province": "河南", "city": "郑州", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 6500, "base_score": 598, "tags": ["双一流B类", "211", "地方强校"]},
    {"name": "云南大学", "province": "云南", "city": "昆明", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 7500, "base_score": 590, "tags": ["双一流B类", "211", "地方强校"]},
    {"name": "新疆大学", "province": "新疆", "city": "乌鲁木齐", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 10000, "base_score": 570, "tags": ["双一流B类", "211", "西部高校"]},
    {"name": "北京化工大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 5500, "base_score": 605, "tags": ["211", "双一流", "化工强"]},
    {"name": "北京林业大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.AGRICULTURAL, "base_rank": 6000, "base_score": 602, "tags": ["211", "双一流", "林业强"]},
    {"name": "北京中医药大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.MEDICAL, "base_rank": 5000, "base_score": 610, "tags": ["211", "双一流", "中医强"]},
    {"name": "中国传媒大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.LANGUAGE, "base_rank": 4500, "base_score": 615, "tags": ["211", "双一流", "传媒强"]},
    {"name": "中国矿业大学", "province": "江苏", "city": "徐州", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 6500, "base_score": 598, "tags": ["211", "双一流", "矿业强"]},
    {"name": "河海大学", "province": "江苏", "city": "南京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 5500, "base_score": 605, "tags": ["211", "双一流", "水利强"]},
    {"name": "江南大学", "province": "江苏", "city": "无锡", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 6200, "base_score": 600, "tags": ["211", "双一流", "食品轻工强"]},
    {"name": "南京农业大学", "province": "江苏", "city": "南京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.AGRICULTURAL, "base_rank": 6000, "base_score": 602, "tags": ["211", "双一流", "农林强"]},
    {"name": "中国药科大学", "province": "江苏", "city": "南京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.MEDICAL, "base_rank": 5500, "base_score": 605, "tags": ["211", "双一流", "药学强"]},
    {"name": "南京师范大学", "province": "江苏", "city": "南京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.NORMAL, "base_rank": 5200, "base_score": 608, "tags": ["211", "双一流", "师范强"]},
    {"name": "安徽大学", "province": "安徽", "city": "合肥", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 7000, "base_score": 593, "tags": ["211", "双一流", "地方强校"]},
    {"name": "合肥工业大学", "province": "安徽", "city": "合肥", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 6000, "base_score": 602, "tags": ["211", "双一流", "工科强"]},
    {"name": "福州大学", "province": "福建", "city": "福州", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 6500, "base_score": 598, "tags": ["211", "双一流", "地方强校"]},
    {"name": "南昌大学", "province": "江西", "city": "南昌", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 7000, "base_score": 593, "tags": ["211", "双一流", "地方强校"]},
    {"name": "中国石油大学", "province": "山东", "city": "青岛", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 6200, "base_score": 600, "tags": ["211", "双一流", "石油强"]},
    {"name": "太原理工大学", "province": "山西", "city": "太原", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 7500, "base_score": 590, "tags": ["211", "双一流", "地方强校"]},
    {"name": "河北工业大学", "province": "天津", "city": "天津", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 7000, "base_score": 593, "tags": ["211", "双一流", "地方强校"]},
    {"name": "广西大学", "province": "广西", "city": "南宁", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 8000, "base_score": 585, "tags": ["211", "双一流", "地方强校"]},
    {"name": "贵州大学", "province": "贵州", "city": "贵阳", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 8500, "base_score": 580, "tags": ["211", "双一流", "地方强校"]},
    {"name": "海南大学", "province": "海南", "city": "海口", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 9000, "base_score": 575, "tags": ["双一流B类", "211", "地方强校"]},
    {"name": "内蒙古大学", "province": "内蒙古", "city": "呼和浩特", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 9000, "base_score": 575, "tags": ["211", "双一流", "地方强校"]},
    {"name": "辽宁大学", "province": "辽宁", "city": "沈阳", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 7000, "base_score": 593, "tags": ["211", "双一流", "地方强校"]},
    {"name": "大连海事大学", "province": "辽宁", "city": "大连", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 7500, "base_score": 590, "tags": ["211", "双一流", "海事强"]},
    {"name": "延边大学", "province": "吉林", "city": "延吉", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 9500, "base_score": 572, "tags": ["211", "双一流", "民族地区"]},
    {"name": "东北林业大学", "province": "黑龙江", "city": "哈尔滨", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.AGRICULTURAL, "base_rank": 8000, "base_score": 585, "tags": ["211", "双一流", "林业强"]},
    {"name": "东北农业大学", "province": "黑龙江", "city": "哈尔滨", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.AGRICULTURAL, "base_rank": 8500, "base_score": 580, "tags": ["211", "双一流", "农业强"]},
    {"name": "宁夏大学", "province": "宁夏", "city": "银川", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 9500, "base_score": 572, "tags": ["211", "双一流", "地方强校"]},
    {"name": "青海大学", "province": "青海", "city": "西宁", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 10000, "base_score": 570, "tags": ["211", "双一流", "地方强校"]},
    {"name": "石河子大学", "province": "新疆", "city": "石河子", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 10500, "base_score": 565, "tags": ["211", "双一流", "兵团高校"]},
    {"name": "西藏大学", "province": "西藏", "city": "拉萨", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 11000, "base_score": 560, "tags": ["211", "双一流", "高原高校"]},
    {"name": "天津医科大学", "province": "天津", "city": "天津", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.MEDICAL, "base_rank": 5000, "base_score": 610, "tags": ["211", "双一流", "医学强"]},
    {"name": "中国人民公安大学", "province": "北京", "city": "北京", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.MILITARY, "base_rank": 7000, "base_score": 593, "tags": ["双一流", "警校顶尖"]},
    {"name": "北京工业大学", "province": "北京", "city": "北京", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.SCIENCE, "base_rank": 5500, "base_score": 605, "tags": ["211", "双一流", "地方强校"]},
    {"name": "首都师范大学", "province": "北京", "city": "北京", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.NORMAL, "base_rank": 6500, "base_score": 598, "tags": ["双一流", "师范强"]},
    {"name": "深圳大学", "province": "广东", "city": "深圳", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 5000, "base_score": 610, "tags": ["双一流", "地方强校", "特区"]},
    {"name": "华南师范大学", "province": "广东", "city": "广州", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.NORMAL, "base_rank": 5500, "base_score": 605, "tags": ["211", "双一流", "师范强"]},
    {"name": "广州中医药大学", "province": "广东", "city": "广州", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.MEDICAL, "base_rank": 7000, "base_score": 593, "tags": ["双一流", "中医强"]},
    {"name": "南京邮电大学", "province": "江苏", "city": "南京", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.SCIENCE, "base_rank": 5000, "base_score": 610, "tags": ["双一流", "信息通信强"]},
    {"name": "南京信息工程大学", "province": "江苏", "city": "南京", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.SCIENCE, "base_rank": 6000, "base_score": 602, "tags": ["双一流", "气象强"]},
    {"name": "南京中医药大学", "province": "江苏", "city": "南京", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.MEDICAL, "base_rank": 6500, "base_score": 598, "tags": ["双一流", "中医强"]},
    {"name": "杭州电子科技大学", "province": "浙江", "city": "杭州", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.SCIENCE, "base_rank": 6000, "base_score": 602, "tags": ["地方强校", "电子信息"]},
    {"name": "浙江工业大学", "province": "浙江", "city": "杭州", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.SCIENCE, "base_rank": 6500, "base_score": 598, "tags": ["地方强校"]},
    {"name": "浙江师范大学", "province": "浙江", "city": "金华", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.NORMAL, "base_rank": 7500, "base_score": 590, "tags": ["地方强校", "师范"]},
    {"name": "宁波大学", "province": "浙江", "city": "宁波", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 6500, "base_score": 598, "tags": ["双一流", "地方强校"]},
    {"name": "上海中医药大学", "province": "上海", "city": "上海", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.MEDICAL, "base_rank": 6000, "base_score": 602, "tags": ["双一流", "中医强"]},
    {"name": "上海海洋大学", "province": "上海", "city": "上海", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.AGRICULTURAL, "base_rank": 8500, "base_score": 580, "tags": ["双一流", "水产强"]},
    {"name": "成都理工大学", "province": "四川", "city": "成都", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.SCIENCE, "base_rank": 7000, "base_score": 593, "tags": ["双一流", "地学强"]},
    {"name": "成都中医药大学", "province": "四川", "city": "成都", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.MEDICAL, "base_rank": 7500, "base_score": 590, "tags": ["双一流", "中医强"]},
    {"name": "四川农业大学", "province": "四川", "city": "雅安", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.AGRICULTURAL, "base_rank": 7000, "base_score": 593, "tags": ["211", "双一流", "农业强"]},
    {"name": "西南石油大学", "province": "四川", "city": "南充", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.SCIENCE, "base_rank": 7500, "base_score": 590, "tags": ["双一流", "石油强"]},
    {"name": "南方科技大学", "province": "广东", "city": "深圳", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.SCIENCE, "base_rank": 4500, "base_score": 615, "tags": ["双一流", "新型大学", "特区"]},
    {"name": "广州大学", "province": "广东", "city": "广州", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 7000, "base_score": 593, "tags": ["地方强校"]},
    {"name": "广东工业大学", "province": "广东", "city": "广州", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.SCIENCE, "base_rank": 6500, "base_score": 598, "tags": ["双一流", "地方强校"]},
    {"name": "南方医科大学", "province": "广东", "city": "广州", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.MEDICAL, "base_rank": 6000, "base_score": 602, "tags": ["地方强校", "医学"]},
    {"name": "武汉科技大学", "province": "湖北", "city": "武汉", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.SCIENCE, "base_rank": 7500, "base_score": 590, "tags": ["地方强校"]},
    {"name": "湖北大学", "province": "湖北", "city": "武汉", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 8000, "base_score": 585, "tags": ["地方强校"]},
    {"name": "湘潭大学", "province": "湖南", "city": "湘潭", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 7000, "base_score": 593, "tags": ["双一流", "地方强校"]},
    {"name": "湖南师范大学", "province": "湖南", "city": "长沙", "level": CollegeLevel.PROJECT_211, "college_type": CollegeType.NORMAL, "base_rank": 6500, "base_score": 598, "tags": ["211", "双一流", "师范强"]},
    {"name": "长沙理工大学", "province": "湖南", "city": "长沙", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.SCIENCE, "base_rank": 7500, "base_score": 590, "tags": ["地方强校"]},
    {"name": "山东师范大学", "province": "山东", "city": "济南", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.NORMAL, "base_rank": 7500, "base_score": 590, "tags": ["地方强校", "师范"]},
    {"name": "青岛大学", "province": "山东", "city": "青岛", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 7000, "base_score": 593, "tags": ["地方强校"]},
    {"name": "燕山大学", "province": "河北", "city": "秦皇岛", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.SCIENCE, "base_rank": 7000, "base_score": 593, "tags": ["地方强校", "机械强"]},
    {"name": "河南大学", "province": "河南", "city": "开封", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 7000, "base_score": 593, "tags": ["双一流", "百年名校"]},
    {"name": "西安建筑科技大学", "province": "陕西", "city": "西安", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.SCIENCE, "base_rank": 7000, "base_score": 593, "tags": ["地方强校", "建筑老八校"]},
    {"name": "西安理工大学", "province": "陕西", "city": "西安", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.SCIENCE, "base_rank": 7500, "base_score": 590, "tags": ["地方强校"]},
    {"name": "重庆邮电大学", "province": "重庆", "city": "重庆", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.SCIENCE, "base_rank": 6500, "base_score": 598, "tags": ["地方强校", "信息通信"]},
    {"name": "重庆医科大学", "province": "重庆", "city": "重庆", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.MEDICAL, "base_rank": 6500, "base_score": 598, "tags": ["地方强校", "医学"]},
    {"name": "江西财经大学", "province": "江西", "city": "南昌", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.FINANCE, "base_rank": 7500, "base_score": 590, "tags": ["地方强校", "财经"]},
    {"name": "昆明理工大学", "province": "云南", "city": "昆明", "level": CollegeLevel.ORDINARY, "college_type": CollegeType.SCIENCE, "base_rank": 8500, "base_score": 580, "tags": ["地方强校"]},
    {"name": "山西大学", "province": "山西", "city": "太原", "level": CollegeLevel.DOUBLE_FIRST_CLASS, "college_type": CollegeType.COMPREHENSIVE, "base_rank": 7500, "base_score": 590, "tags": ["双一流", "百年名校"]},
]

PROVINCES = [
    "北京", "上海", "广东", "江苏", "浙江", "山东", "河南", "四川", "湖北", "湖南",
    "河北", "安徽", "福建", "陕西", "辽宁", "重庆", "天津", "江西", "广西", "云南",
    "贵州", "山西", "黑龙江", "吉林", "内蒙古", "新疆", "甘肃", "海南", "宁夏", "青海", "西藏"
]

SUBJECT_COMBINATIONS = [
    "物理+化学+生物", "物理+化学+地理", "物理+化学+政治",
    "物理+生物+地理", "物理+生物+政治", "物理+地理+政治",
    "历史+地理+政治", "历史+生物+政治", "历史+生物+地理",
    "历史+化学+政治", "历史+化学+生物", "历史+化学+地理"
]


def _generate_majors(college_type: CollegeType, level: CollegeLevel, count: int = 8) -> List[Major]:
    type_priority = {
        CollegeType.COMPREHENSIVE: ["计算机科学与技术", "金融学", "法学", "汉语言文学", "数学与应用数学", "英语", "工商管理", "软件工程", "经济学", "统计学", "心理学", "新闻学"],
        CollegeType.SCIENCE: ["计算机科学与技术", "软件工程", "电子信息工程", "通信工程", "自动化", "机械工程", "材料科学与工程", "人工智能", "数据科学与大数据技术", "电气工程及其自动化", "土木工程", "机器人工程", "车辆工程", "航空航天工程", "新能源材料与器件"],
        CollegeType.NORMAL: ["汉语言文学", "英语", "数学与应用数学", "物理学", "历史学", "心理学", "化学", "生物科学", "思想政治教育", "地理科学", "教育学", "小学教育"],
        CollegeType.AGRICULTURAL: ["农业工程", "林学", "生物科学", "食品科学与工程", "水产养殖学", "园艺", "植物保护", "动物科学", "草业科学", "环境科学", "农业资源与环境"],
        CollegeType.MEDICAL: ["临床医学", "口腔医学", "药学", "中医学", "护理学", "预防医学", "医学检验技术", "医学影像技术", "生物医学工程", "基础医学", "中药学"],
        CollegeType.FINANCE: ["金融学", "经济学", "会计学", "国际经济与贸易", "财务管理", "统计学", "保险学", "投资学", "金融工程", "财政学", "税收学", "工商管理"],
        CollegeType.POLITICAL: ["法学", "政治学与行政学", "侦查学", "治安学", "社会学", "行政管理", "公共事业管理", "国际政治", "知识产权", "监狱学"],
        CollegeType.LANGUAGE: ["英语", "翻译", "日语", "法语", "德语", "西班牙语", "俄语", "阿拉伯语", "新闻学", "传播学", "汉语国际教育"],
        CollegeType.ART: ["视觉传达设计", "环境设计", "美术学", "音乐表演", "播音与主持艺术", "广播电视编导", "动画", "数字媒体艺术", "产品设计", "服装与服饰设计"],
        CollegeType.SPORT: ["运动训练", "社会体育指导与管理", "体育教育", "休闲体育", "运动人体科学", "运动康复"],
        CollegeType.MILITARY: ["侦查学", "治安学", "法学", "刑事科学技术", "网络安全与执法", "公安管理学", "涉外警务", "警务指挥与战术"],
    }

    level_distribution = {
        CollegeLevel.C9: [DisciplineLevel.A_PLUS, DisciplineLevel.A, DisciplineLevel.A, DisciplineLevel.A_MINUS, DisciplineLevel.A_MINUS, DisciplineLevel.B_PLUS, DisciplineLevel.B_PLUS, DisciplineLevel.B],
        CollegeLevel.PROJECT_985: [DisciplineLevel.A, DisciplineLevel.A_MINUS, DisciplineLevel.A_MINUS, DisciplineLevel.B_PLUS, DisciplineLevel.B_PLUS, DisciplineLevel.B, DisciplineLevel.B, DisciplineLevel.B_MINUS],
        CollegeLevel.PROJECT_211: [DisciplineLevel.A_MINUS, DisciplineLevel.B_PLUS, DisciplineLevel.B_PLUS, DisciplineLevel.B, DisciplineLevel.B, DisciplineLevel.B_MINUS, DisciplineLevel.B_MINUS, DisciplineLevel.C_PLUS],
        CollegeLevel.DOUBLE_FIRST_CLASS: [DisciplineLevel.B_PLUS, DisciplineLevel.B, DisciplineLevel.B, DisciplineLevel.B_MINUS, DisciplineLevel.B_MINUS, DisciplineLevel.C_PLUS, DisciplineLevel.C_PLUS, DisciplineLevel.C],
        CollegeLevel.ORDINARY: [DisciplineLevel.B, DisciplineLevel.B_MINUS, DisciplineLevel.B_MINUS, DisciplineLevel.C_PLUS, DisciplineLevel.C_PLUS, DisciplineLevel.C, DisciplineLevel.C, DisciplineLevel.C_MINUS],
    }

    majors_list = []
    available = type_priority.get(college_type, type_priority[CollegeType.COMPREHENSIVE])
    selected = available[:count]
    dist = level_distribution.get(level, level_distribution[CollegeLevel.ORDINARY])
    for idx, name in enumerate(selected):
        if name in MAJOR_DATABASE:
            m = MAJOR_DATABASE[name]
            majors_list.append(Major(
                id=f"M{hash(name) % 100000:05d}_{idx}",
                name=name,
                subject_requirements=m["subject_requirements"],
                employment_direction=m["employment_direction"],
                typical_positions=m["typical_positions"],
                description=m["description"],
                discipline_level=dist[idx % len(dist)] if idx < len(dist) else random.choice(dist),
            ))
    return majors_list


def _generate_admission_data(base_rank: int, base_score: int) -> List[AdmissionData]:
    result = []
    years = [2025, 2024, 2023]
    for year_idx, year in enumerate(years):
        for province in PROVINCES[:15]:
            rank_noise = random.randint(-int(base_rank * 0.15), int(base_rank * 0.15))
            score_noise = random.randint(-8, 8)
            rank_variation = int(base_rank * (1 + year_idx * 0.02)) + rank_noise
            score_variation = base_score - year_idx * 2 + score_noise
            result.append(AdmissionData(
                year=year,
                province=province,
                score=max(400, min(750, score_variation)),
                rank=max(100, rank_variation),
                batch="本科一批",
                subject_combination=random.choice(SUBJECT_COMBINATIONS[:6]),
            ))
    return result


def generate_colleges() -> List[College]:
    colleges = []
    employment_rate_by_level = {
        CollegeLevel.C9: (0.95, 0.98),
        CollegeLevel.PROJECT_985: (0.92, 0.97),
        CollegeLevel.PROJECT_211: (0.88, 0.94),
        CollegeLevel.DOUBLE_FIRST_CLASS: (0.85, 0.92),
        CollegeLevel.ORDINARY: (0.78, 0.88),
    }
    salary_by_level = {
        CollegeLevel.C9: (180000, 280000),
        CollegeLevel.PROJECT_985: (150000, 240000),
        CollegeLevel.PROJECT_211: (120000, 190000),
        CollegeLevel.DOUBLE_FIRST_CLASS: (100000, 160000),
        CollegeLevel.ORDINARY: (70000, 130000),
    }
    for idx, tpl in enumerate(COLLEGE_TEMPLATES):
        majors = _generate_majors(tpl["college_type"], tpl["level"], count=random.randint(6, 12))
        admission_data = _generate_admission_data(tpl["base_rank"], tpl["base_score"])
        er_range = employment_rate_by_level.get(tpl["level"], employment_rate_by_level[CollegeLevel.ORDINARY])
        sal_range = salary_by_level.get(tpl["level"], salary_by_level[CollegeLevel.ORDINARY])
        employment_rate = round(random.uniform(er_range[0], er_range[1]), 4)
        average_salary = random.randint(sal_range[0], sal_range[1])
        college_id = f"C{idx + 1:04d}"
        employment_data = generate_employment_data(
            college_id=college_id,
            college_name=tpl["name"],
            college_province=tpl["province"],
            college_city=tpl["city"],
            level=tpl["level"],
            college_type=tpl["college_type"],
            base_employment_rate=employment_rate,
            base_average_salary=average_salary,
        )
        colleges.append(College(
            id=college_id,
            name=tpl["name"],
            province=tpl["province"],
            city=tpl["city"],
            level=tpl["level"],
            college_type=tpl["college_type"],
            description=f"{tpl['name']}是一所位于{tpl['city']}的知名高等院校。",
            majors=majors,
            admission_data=admission_data,
            tags=tpl["tags"],
            employment_rate=employment_rate,
            average_salary=average_salary,
            employment_data=employment_data,
        ))
    return colleges


MAJOR_DETAIL_DATABASE: Dict[str, Dict] = {
    "计算机科学与技术": {
        "category": "工学",
        "major_type": "电气信息类",
        "brief_intro": "研究计算机系统与软件应用的核心学科，就业面广，市场需求大。",
        "introduction": "计算机科学与技术是研究信息获取、处理、存储、传输和利用的理论与实践相结合的学科。",
        "core_courses": ["数据结构", "算法设计", "操作系统", "计算机网络", "数据库原理", "编译原理"],
        "employment_directions": ["互联网/IT行业", "人工智能", "软件开发", "数据分析", "信息安全"],
        "typical_positions": ["软件工程师", "算法工程师", "数据分析师", "产品经理", "系统架构师"],
        "salary_range": {"fresh": 180000, "three_years": 300000, "five_years_plus": 500000},
        "postgraduate_ratio": 0.45,
        "suitable_traits": ["逻辑思维强", "喜欢编程", "数学基础好", "持续学习能力"],
        "unsuitable_people": ["不喜欢久坐", "对代码无兴趣", "逻辑思维较弱"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男7:女3",
        "employment_prospect": "极好",
        "employment_rate": 0.96,
    },
    "软件工程": {
        "category": "工学",
        "major_type": "电气信息类",
        "brief_intro": "系统学习软件开发与工程化方法，注重实践能力。",
        "introduction": "软件工程是研究和应用如何以系统性的、规范化的、可定量的过程化方法去开发和维护软件。",
        "core_courses": ["软件工程导论", "软件设计", "软件测试", "软件项目管理", "敏捷开发"],
        "employment_directions": ["软件开发", "互联网", "金融科技", "企业信息化"],
        "typical_positions": ["后端开发工程师", "前端开发工程师", "全栈工程师", "测试工程师", "运维工程师"],
        "salary_range": {"fresh": 170000, "three_years": 280000, "five_years_plus": 450000},
        "postgraduate_ratio": 0.30,
        "suitable_traits": ["动手能力强", "喜欢工程实践", "团队协作好"],
        "unsuitable_people": ["不喜欢编程", "缺乏耐心", "不善于团队合作"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男7.5:女2.5",
        "employment_prospect": "极好",
        "employment_rate": 0.95,
    },
    "人工智能": {
        "category": "工学",
        "major_type": "电气信息类",
        "brief_intro": "前沿的AI交叉学科，发展前景广阔但门槛高。",
        "introduction": "人工智能是研究使计算机来模拟人的某些思维过程和智能行为的学科。",
        "core_courses": ["机器学习", "深度学习", "计算机视觉", "自然语言处理", "神经网络"],
        "employment_directions": ["人工智能", "机器学习", "计算机视觉", "自然语言处理", "自动驾驶"],
        "typical_positions": ["AI算法工程师", "机器学习工程师", "CV工程师", "NLP工程师", "深度学习研究员"],
        "salary_range": {"fresh": 250000, "three_years": 400000, "five_years_plus": 650000},
        "postgraduate_ratio": 0.70,
        "suitable_traits": ["数学优秀", "科研能力强", "对AI有热情", "英文阅读能力强"],
        "unsuitable_people": ["数学基础薄弱", "不喜欢科研", "期望快速就业"],
        "study_difficulty": "非常难",
        "course_load": "很重",
        "gender_ratio": "男8:女2",
        "employment_prospect": "极好",
        "employment_rate": 0.94,
    },
    "数据科学与大数据技术": {
        "category": "工学",
        "major_type": "电气信息类",
        "brief_intro": "聚焦海量数据处理与分析，数据驱动决策。",
        "introduction": "数据科学与大数据技术是利用数学、统计、编程等方法从海量数据中提取价值的交叉学科。",
        "core_courses": ["数据结构", "数据库", "数据挖掘", "机器学习", "大数据平台"],
        "employment_directions": ["数据分析", "大数据", "商业智能", "数据挖掘", "云计算"],
        "typical_positions": ["数据科学家", "大数据工程师", "BI分析师", "数据产品经理", "数据挖掘工程师"],
        "salary_range": {"fresh": 190000, "three_years": 320000, "five_years_plus": 500000},
        "postgraduate_ratio": 0.50,
        "suitable_traits": ["数学统计好", "编程能力强", "对数据敏感"],
        "unsuitable_people": ["不喜欢数字", "编程能力差", "缺乏耐心"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男7:女3",
        "employment_prospect": "极好",
        "employment_rate": 0.95,
    },
    "电子信息工程": {
        "category": "工学",
        "major_type": "电气信息类",
        "brief_intro": "信息技术与电子系统的基础学科，软硬结合。",
        "introduction": "电子信息工程是应用计算机等现代化技术进行电子信息控制和信息处理的学科。",
        "core_courses": ["电路分析", "模拟电子", "数字电子", "信号与系统", "通信原理"],
        "employment_directions": ["通信", "半导体", "消费电子", "物联网", "航空航天"],
        "typical_positions": ["硬件工程师", "嵌入式工程师", "通信工程师", "IC设计工程师", "FPGA工程师"],
        "salary_range": {"fresh": 140000, "three_years": 220000, "five_years_plus": 350000},
        "postgraduate_ratio": 0.45,
        "suitable_traits": ["物理好", "动手能力强", "软硬兼修"],
        "unsuitable_people": ["物理差", "不喜欢焊接电路"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男7.5:女2.5",
        "employment_prospect": "良好",
        "employment_rate": 0.90,
    },
    "通信工程": {
        "category": "工学",
        "major_type": "电气信息类",
        "brief_intro": "通信系统与网络技术，5G/6G前沿领域。",
        "introduction": "通信工程主要研究通信过程中的信息传输和信号处理的原理和应用。",
        "core_courses": ["通信原理", "信号与系统", "数字信号处理", "无线通信", "光纤通信"],
        "employment_directions": ["5G/6G通信", "互联网", "运营商", "通信设备", "卫星通信"],
        "typical_positions": ["通信工程师", "射频工程师", "网络优化工程师", "5G算法工程师", "传输工程师"],
        "salary_range": {"fresh": 140000, "three_years": 230000, "five_years_plus": 360000},
        "postgraduate_ratio": 0.48,
        "suitable_traits": ["数学好", "物理好", "对通信技术感兴趣"],
        "unsuitable_people": ["数学差", "不喜欢理论推导"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男7:女3",
        "employment_prospect": "良好",
        "employment_rate": 0.89,
    },
    "自动化": {
        "category": "工学",
        "major_type": "电气信息类",
        "brief_intro": "自动控制与智能系统，工业4.0核心。",
        "introduction": "自动化是指机器设备、系统或生产、管理过程在没有人或较少人的直接参与下，按照人的要求，经过自动检测、信息处理、分析判断、操纵控制，实现预期的目标的过程。",
        "core_courses": ["自动控制原理", "现代控制理论", "过程控制", "PLC原理", "机器人学"],
        "employment_directions": ["智能制造", "机器人", "工业控制", "自动驾驶", "物联网"],
        "typical_positions": ["自动化工程师", "机器人工程师", "控制算法工程师", "PLC工程师", "工业互联网工程师"],
        "salary_range": {"fresh": 120000, "three_years": 200000, "five_years_plus": 320000},
        "postgraduate_ratio": 0.40,
        "suitable_traits": ["动手能力强", "喜欢控制", "软硬结合"],
        "unsuitable_people": ["不喜欢编程", "不喜欢硬件"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男8:女2",
        "employment_prospect": "良好",
        "employment_rate": 0.91,
    },
    "机械工程": {
        "category": "工学",
        "major_type": "机械类",
        "brief_intro": "机械装备设计与制造，工业基础学科。",
        "introduction": "机械工程是一门涉及利用物理定律为机械系统作分析、设计、生产及维修的工程学科。",
        "core_courses": ["理论力学", "材料力学", "机械设计", "机械原理", "工程制图"],
        "employment_directions": ["装备制造", "汽车", "航空航天", "新能源", "轨道交通"],
        "typical_positions": ["机械设计工程师", "工艺工程师", "结构工程师", "CAE工程师", "生产工程师"],
        "salary_range": {"fresh": 90000, "three_years": 140000, "five_years_plus": 220000},
        "postgraduate_ratio": 0.35,
        "suitable_traits": ["动手能力强", "空间想象力好", "物理好"],
        "unsuitable_people": ["空间想象力差", "不喜欢画图"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男9:女1",
        "employment_prospect": "良好",
        "employment_rate": 0.88,
    },
    "临床医学": {
        "category": "医学",
        "major_type": "临床医学类",
        "brief_intro": "临床诊断与治疗，学制长但职业稳定。",
        "introduction": "临床医学是研究疾病的病因、诊断、治疗和预后，提高临床治疗水平，促进人体健康的科学。",
        "core_courses": ["人体解剖学", "生理学", "病理学", "药理学", "内科学", "外科学"],
        "employment_directions": ["医院临床", "医学科研", "医药企业", "医疗器械", "医疗AI"],
        "typical_positions": ["临床医生", "医学研究员", "医药研发", "医学影像医师", "医疗AI专家"],
        "salary_range": {"fresh": 80000, "three_years": 180000, "five_years_plus": 350000},
        "postgraduate_ratio": 0.80,
        "suitable_traits": ["责任心强", "抗压能力强", "动手能力好", "生物化学好"],
        "unsuitable_people": ["晕血", "心理素质差", "害怕夜班"],
        "study_difficulty": "非常难",
        "course_load": "极重",
        "gender_ratio": "男5:女5",
        "employment_prospect": "良好",
        "employment_rate": 0.92,
    },
    "口腔医学": {
        "category": "医学",
        "major_type": "口腔医学类",
        "brief_intro": "口腔疾病诊疗，收入高且工作环境好。",
        "introduction": "口腔医学是研究口腔器官、面部软组织、颌面诸骨、颞下颌关节、唾液腺以及颈部某些疾病的防治为主要内容的学科。",
        "core_courses": ["口腔解剖学", "口腔生理学", "口腔病理学", "口腔内科学", "口腔外科学"],
        "employment_directions": ["口腔医院", "牙科诊所", "医疗器械", "种植牙", "口腔材料"],
        "typical_positions": ["口腔科医生", "正畸医生", "种植医生", "口腔修复医师", "口腔产品经理"],
        "salary_range": {"fresh": 100000, "three_years": 220000, "five_years_plus": 400000},
        "postgraduate_ratio": 0.60,
        "suitable_traits": ["心灵手巧", "动手能力强", "沟通能力好"],
        "unsuitable_people": ["动手能力差", "沟通能力弱"],
        "study_difficulty": "非常难",
        "course_load": "极重",
        "gender_ratio": "男4:女6",
        "employment_prospect": "极好",
        "employment_rate": 0.95,
    },
    "金融学": {
        "category": "经济学",
        "major_type": "金融学类",
        "brief_intro": "金融市场与投融资，高薪但竞争激烈。",
        "introduction": "金融学是研究价值判断和价值规律的学科，主要包括金融市场、投资、融资、风险管理等内容。",
        "core_courses": ["货币银行学", "投资学", "公司金融", "金融工程", "计量经济学"],
        "employment_directions": ["银行", "证券", "基金", "保险", "金融科技"],
        "typical_positions": ["投资分析师", "银行客户经理", "基金经理", "风控专员", "量化研究员"],
        "salary_range": {"fresh": 120000, "three_years": 250000, "five_years_plus": 500000},
        "postgraduate_ratio": 0.55,
        "suitable_traits": ["数学好", "数字敏感", "沟通能力强", "名校背景"],
        "unsuitable_people": ["数学差", "对数字不敏感", "不喜欢高压环境"],
        "study_difficulty": "适中",
        "course_load": "适中",
        "gender_ratio": "男4:女6",
        "employment_prospect": "良好",
        "employment_rate": 0.88,
    },
    "会计学": {
        "category": "管理学",
        "major_type": "工商管理类",
        "brief_intro": "会计、审计与财务管理，就业稳定。",
        "introduction": "会计学是以研究财务活动和成本资料的收集、分类、综合、分析和解释的基础上形成协助决策的信息系统。",
        "core_courses": ["基础会计", "中级财务会计", "成本会计", "审计学", "财务管理"],
        "employment_directions": ["四大会计师事务所", "企业财务", "审计", "税务", "投资银行"],
        "typical_positions": ["会计师", "审计师", "财务分析师", "税务专员", "CFO"],
        "salary_range": {"fresh": 80000, "three_years": 140000, "five_years_plus": 250000},
        "postgraduate_ratio": 0.30,
        "suitable_traits": ["细心", "数字敏感", "逻辑清晰", "耐心"],
        "unsuitable_people": ["粗心大意", "对数字没兴趣", "不喜欢重复性工作"],
        "study_difficulty": "适中",
        "course_load": "适中",
        "gender_ratio": "男3:女7",
        "employment_prospect": "良好",
        "employment_rate": 0.90,
    },
    "法学": {
        "category": "法学",
        "major_type": "法学类",
        "brief_intro": "法律理论与实务，需通过司法考试。",
        "introduction": "法学是研究法律现象、法律规范及其发展规律的社会科学。",
        "core_courses": ["法理学", "宪法学", "民法学", "刑法学", "诉讼法学"],
        "employment_directions": ["律师事务所", "公司法务", "法院检察院", "政府法制", "合规"],
        "typical_positions": ["律师", "法官", "检察官", "公司法务", "合规专员"],
        "salary_range": {"fresh": 70000, "three_years": 150000, "five_years_plus": 300000},
        "postgraduate_ratio": 0.35,
        "suitable_traits": ["记忆力好", "逻辑清晰", "口才好", "抗压能力强"],
        "unsuitable_people": ["记忆力差", "不喜欢背诵", "不善言辞"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男4:女6",
        "employment_prospect": "一般",
        "employment_rate": 0.80,
    },
    "汉语言文学": {
        "category": "文学",
        "major_type": "中国语言文学类",
        "brief_intro": "中文语言文学，就业面广但专业壁垒低。",
        "introduction": "汉语言文学专业主要培养掌握汉语和中国文学方面的基本知识，受到有关理论、发展历史、研究现状等方面的系统教育和业务能力的基本训练的人才。",
        "core_courses": ["中国古代文学", "中国现当代文学", "文学概论", "语言学概论", "古代汉语"],
        "employment_directions": ["教育", "新媒体", "出版", "公务员", "品牌策划"],
        "typical_positions": ["语文教师", "新媒体编辑", "文案策划", "出版社编辑", "行政文秘"],
        "salary_range": {"fresh": 60000, "three_years": 100000, "five_years_plus": 160000},
        "postgraduate_ratio": 0.28,
        "suitable_traits": ["文学素养好", "文笔好", "喜欢阅读写作"],
        "unsuitable_people": ["不喜欢阅读", "文笔差"],
        "study_difficulty": "适中",
        "course_load": "适中",
        "gender_ratio": "男2.5:女7.5",
        "employment_prospect": "一般",
        "employment_rate": 0.85,
    },
    "英语": {
        "category": "文学",
        "major_type": "外国语言文学类",
        "brief_intro": "英语语言与文化，国际交流工具。",
        "introduction": "英语专业是培养具有扎实的英语语言基础和比较广泛的科学文化知识，能在外事、经贸、文化、新闻出版、教育、科研、旅游等部门从事翻译、研究、教学、管理工作的英语高级专门人才。",
        "core_courses": ["综合英语", "英语听力", "英语口语", "英语写作", "英美文学", "翻译理论与实践"],
        "employment_directions": ["翻译", "外贸", "教育", "跨境电商", "跨国企业"],
        "typical_positions": ["翻译", "外贸业务员", "英语教师", "跨境运营", "国际商务"],
        "salary_range": {"fresh": 70000, "three_years": 110000, "five_years_plus": 180000},
        "postgraduate_ratio": 0.25,
        "suitable_traits": ["语言天赋好", "听力口语强", "跨文化交流能力"],
        "unsuitable_people": ["英语基础差", "不喜欢语言学习"],
        "study_difficulty": "轻松",
        "course_load": "适中",
        "gender_ratio": "男2:女8",
        "employment_prospect": "一般",
        "employment_rate": 0.84,
    },
    "数学与应用数学": {
        "category": "理学",
        "major_type": "数学类",
        "brief_intro": "数学理论与应用，转行互联网金融容易。",
        "introduction": "数学与应用数学是研究数量、结构、变化以及空间模型等概念的一门学科。",
        "core_courses": ["数学分析", "高等代数", "解析几何", "概率论与数理统计", "运筹学"],
        "employment_directions": ["金融量化", "教育", "数据分析", "科研", "算法"],
        "typical_positions": ["量化分析师", "数学教师", "数据科学家", "算法研究员", "精算师"],
        "salary_range": {"fresh": 100000, "three_years": 180000, "five_years_plus": 300000},
        "postgraduate_ratio": 0.55,
        "suitable_traits": ["数学天赋好", "逻辑思维强", "喜欢研究"],
        "unsuitable_people": ["数学差", "不喜欢理论"],
        "study_difficulty": "非常难",
        "course_load": "极重",
        "gender_ratio": "男6:女4",
        "employment_prospect": "良好",
        "employment_rate": 0.88,
    },
    "建筑学": {
        "category": "工学",
        "major_type": "建筑学类",
        "brief_intro": "建筑设计与城市规划，艺术与工程结合。",
        "introduction": "建筑学是研究建筑及其环境的学科，是一门横跨工程技术和人文艺术的学科。",
        "core_courses": ["建筑设计", "建筑史", "建筑构造", "建筑力学", "城市规划"],
        "employment_directions": ["建筑设计", "城市规划", "房地产", "景观设计", "室内设计"],
        "typical_positions": ["建筑设计师", "规划师", "景观设计师", "房地产策划", "BIM工程师"],
        "salary_range": {"fresh": 100000, "three_years": 160000, "five_years_plus": 250000},
        "postgraduate_ratio": 0.40,
        "suitable_traits": ["空间想象力好", "艺术感强", "手绘能力好", "能熬夜"],
        "unsuitable_people": ["空间想象力差", "不喜欢熬夜", "艺术感弱"],
        "study_difficulty": "较难",
        "course_load": "极重",
        "gender_ratio": "男6:女4",
        "employment_prospect": "一般",
        "employment_rate": 0.82,
    },
    "土木工程": {
        "category": "工学",
        "major_type": "土木类",
        "brief_intro": "土木工程设计与施工，基建行业支柱。",
        "introduction": "土木工程是建造各类土地工程设施的科学技术的统称，既指所应用的材料、设备和所进行的勘测、设计、施工、保养、维修等技术活动。",
        "core_courses": ["理论力学", "材料力学", "结构力学", "混凝土结构", "土力学"],
        "employment_directions": ["建筑施工", "房地产", "基础设施", "市政工程", "工程咨询"],
        "typical_positions": ["土建工程师", "项目经理", "结构设计师", "造价工程师", "监理工程师"],
        "salary_range": {"fresh": 80000, "three_years": 130000, "five_years_plus": 200000},
        "postgraduate_ratio": 0.30,
        "suitable_traits": ["吃苦耐劳", "动手能力强", "物理好"],
        "unsuitable_people": ["吃不了苦", "不喜欢下工地"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男9:女1",
        "employment_prospect": "一般",
        "employment_rate": 0.85,
    },
    "工商管理": {
        "category": "管理学",
        "major_type": "工商管理类",
        "brief_intro": "企业经营管理，综合类管理专业。",
        "introduction": "工商管理是研究工商企业经济管理基本理论和一般方法的学科，主要包括企业的经营战略制定和内部行为管理两个方面。",
        "core_courses": ["管理学", "经济学", "市场营销", "财务管理", "人力资源管理"],
        "employment_directions": ["企业管理", "咨询", "人力资源", "市场营销", "创业"],
        "typical_positions": ["管理培训生", "咨询顾问", "HR经理", "市场经理", "运营经理"],
        "salary_range": {"fresh": 70000, "three_years": 120000, "five_years_plus": 200000},
        "postgraduate_ratio": 0.30,
        "suitable_traits": ["沟通能力强", "组织协调好", "综合能力强"],
        "unsuitable_people": ["内向", "不喜欢管理", "缺乏领导力"],
        "study_difficulty": "轻松",
        "course_load": "适中",
        "gender_ratio": "男4.5:女5.5",
        "employment_prospect": "一般",
        "employment_rate": 0.86,
    },
    "心理学": {
        "category": "理学",
        "major_type": "心理学类",
        "brief_intro": "心理科学与应用，社会需求增长中。",
        "introduction": "心理学是一门研究人类及动物的心理现象、精神功能和行为的科学，既是一门理论学科，也是一门应用学科。",
        "core_courses": ["普通心理学", "发展心理学", "实验心理学", "心理统计学", "心理咨询"],
        "employment_directions": ["心理咨询", "教育", "人力资源", "用户研究", "精神卫生"],
        "typical_positions": ["心理咨询师", "心理教师", "HRBP", "用户研究员", "临床心理学家"],
        "salary_range": {"fresh": 60000, "three_years": 90000, "five_years_plus": 150000},
        "postgraduate_ratio": 0.50,
        "suitable_traits": ["共情能力强", "善于倾听", "观察力敏锐", "自我情绪稳定"],
        "unsuitable_people": ["情绪容易受影响", "不善于倾听"],
        "study_difficulty": "适中",
        "course_load": "适中",
        "gender_ratio": "男3:女7",
        "employment_prospect": "一般",
        "employment_rate": 0.80,
    },
    "药学": {
        "category": "医学",
        "major_type": "药学类",
        "brief_intro": "药物发现与开发，医药行业核心。",
        "introduction": "药学是研究药物的来源、炮制、性状、作用、分析、鉴定、调配、生产、保管和寻找（包括合成）新药等的学科。",
        "core_courses": ["有机化学", "分析化学", "药物化学", "药剂学", "药理学"],
        "employment_directions": ["医药研发", "制药", "药品监管", "临床药学", "医药代表"],
        "typical_positions": ["药物研发工程师", "制剂工程师", "分析研究员", "临床药师", "药政注册"],
        "salary_range": {"fresh": 80000, "three_years": 130000, "five_years_plus": 220000},
        "postgraduate_ratio": 0.55,
        "suitable_traits": ["化学好", "生物好", "耐心细致", "科研能力强"],
        "unsuitable_people": ["化学差", "不喜欢做实验"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男4:女6",
        "employment_prospect": "良好",
        "employment_rate": 0.88,
    },
    "新闻学": {
        "category": "文学",
        "major_type": "新闻传播学类",
        "brief_intro": "新闻传播与媒介，新媒体时代转型中。",
        "introduction": "新闻学是研究新闻事业和新闻工作规律的科学。",
        "core_courses": ["新闻学概论", "新闻采访与写作", "新闻编辑", "传播学概论", "新闻评论"],
        "employment_directions": ["传统媒体", "新媒体", "公关", "广告", "企业传播"],
        "typical_positions": ["记者", "编辑", "新媒体运营", "公关专员", "广告策划"],
        "salary_range": {"fresh": 70000, "three_years": 110000, "five_years_plus": 180000},
        "postgraduate_ratio": 0.25,
        "suitable_traits": ["文字功底好", "社会责任感强", "好奇心强", "沟通能力好"],
        "unsuitable_people": ["文笔差", "内向不善交际"],
        "study_difficulty": "轻松",
        "course_load": "适中",
        "gender_ratio": "男3:女7",
        "employment_prospect": "一般",
        "employment_rate": 0.82,
    },
    "经济学": {
        "category": "经济学",
        "major_type": "经济学类",
        "brief_intro": "经济理论与应用，考研和考公热门。",
        "introduction": "经济学是研究人类经济活动的规律即价值的创造、转化、实现的规律——经济发展规律的理论。",
        "core_courses": ["微观经济学", "宏观经济学", "计量经济学", "政治经济学", "财政学"],
        "employment_directions": ["宏观经济研究", "金融", "咨询", "政府机关", "企业战略"],
        "typical_positions": ["经济分析师", "政策研究员", "咨询顾问", "投资研究员", "数据分析师"],
        "salary_range": {"fresh": 90000, "three_years": 160000, "five_years_plus": 280000},
        "postgraduate_ratio": 0.55,
        "suitable_traits": ["数学好", "逻辑思维强", "关注社会经济"],
        "unsuitable_people": ["数学差", "对经济不感兴趣"],
        "study_difficulty": "适中",
        "course_load": "适中",
        "gender_ratio": "男5:女5",
        "employment_prospect": "良好",
        "employment_rate": 0.86,
    },
    "物理学": {
        "category": "理学",
        "major_type": "物理学类",
        "brief_intro": "物理理论与实验，基础研究重镇。",
        "introduction": "物理学是研究物质运动最一般规律和物质基本结构的学科。",
        "core_courses": ["理论力学", "电动力学", "量子力学", "热力学与统计物理", "固体物理"],
        "employment_directions": ["科研", "半导体", "光学", "教育", "新能源"],
        "typical_positions": ["物理研究员", "半导体工程师", "光学工程师", "物理教师", "量子计算研究员"],
        "salary_range": {"fresh": 90000, "three_years": 150000, "five_years_plus": 260000},
        "postgraduate_ratio": 0.65,
        "suitable_traits": ["物理天赋好", "数学好", "喜欢理论研究"],
        "unsuitable_people": ["物理差", "数学差", "不喜欢理论"],
        "study_difficulty": "非常难",
        "course_load": "极重",
        "gender_ratio": "男7.5:女2.5",
        "employment_prospect": "良好",
        "employment_rate": 0.85,
    },
    "生物科学": {
        "category": "理学",
        "major_type": "生物科学类",
        "brief_intro": "生命科学研究，生物医药前沿。",
        "introduction": "生物科学是研究生命现象和生命活动规律的科学，是自然科学中的基础学科之一。",
        "core_courses": ["分子生物学", "细胞生物学", "遗传学", "生物化学", "微生物学"],
        "employment_directions": ["生物医药", "基因检测", "农业", "科研", "食品"],
        "typical_positions": ["生物研究员", "测序分析师", "发酵工程师", "生物信息工程师", "生物教师"],
        "salary_range": {"fresh": 70000, "three_years": 110000, "five_years_plus": 180000},
        "postgraduate_ratio": 0.65,
        "suitable_traits": ["生物好", "化学好", "喜欢做实验", "科研能力强"],
        "unsuitable_people": ["不喜欢实验", "生物化学差"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男5:女5",
        "employment_prospect": "一般",
        "employment_rate": 0.78,
    },
    "车辆工程": {
        "category": "工学",
        "major_type": "机械类",
        "brief_intro": "汽车设计与制造，新能源汽车热潮。",
        "introduction": "车辆工程是研究汽车、拖拉机、机车车辆、军用车辆及其他工程车辆等陆上移动机械的理论、设计及制造技术的工程技术学科。",
        "core_courses": ["汽车构造", "汽车理论", "汽车设计", "发动机原理", "汽车电子"],
        "employment_directions": ["新能源汽车", "传统汽车", "智能网联", "汽车零部件", "轨道交通"],
        "typical_positions": ["汽车设计工程师", "新能源工程师", "智能驾驶工程师", "底盘工程师", "汽车电子工程师"],
        "salary_range": {"fresh": 110000, "three_years": 170000, "five_years_plus": 260000},
        "postgraduate_ratio": 0.35,
        "suitable_traits": ["喜欢汽车", "物理好", "动手能力强"],
        "unsuitable_people": ["对汽车不感兴趣", "物理差"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男9:女1",
        "employment_prospect": "良好",
        "employment_rate": 0.90,
    },
    "航空航天工程": {
        "category": "工学",
        "major_type": "航空航天类",
        "brief_intro": "航空与航天飞行器设计，高精尖领域。",
        "introduction": "航空航天工程是涉及航空与航天两大技术领域的综合性学科，培养飞行器设计、制造和研发人才。",
        "core_courses": ["空气动力学", "飞行器结构力学", "飞行力学", "航空航天材料", "航天器设计"],
        "employment_directions": ["航空航天", "国防军工", "卫星", "民航", "航天科工"],
        "typical_positions": ["飞行器设计工程师", "航空发动机工程师", "结构强度工程师", "航电工程师", "发射场工程师"],
        "salary_range": {"fresh": 120000, "three_years": 180000, "five_years_plus": 280000},
        "postgraduate_ratio": 0.55,
        "suitable_traits": ["物理好", "数学好", "爱国敬业", "动手能力强"],
        "unsuitable_people": ["物理数学差", "不能接受地域限制"],
        "study_difficulty": "非常难",
        "course_load": "极重",
        "gender_ratio": "男8.5:女1.5",
        "employment_prospect": "良好",
        "employment_rate": 0.92,
    },
    "材料科学与工程": {
        "category": "工学",
        "major_type": "材料类",
        "brief_intro": "材料研发与应用，制造业基础。",
        "introduction": "材料科学与工程是研究材料的组成、结构、工艺、性能和应用的学科。",
        "core_courses": ["材料力学", "材料物理", "材料化学", "材料科学基础", "材料加工工程"],
        "employment_directions": ["新材料", "半导体", "新能源", "冶金", "高端制造"],
        "typical_positions": ["材料工程师", "半导体工艺工程师", "新能源材料研究员", "材料测试工程师", "金相工程师"],
        "salary_range": {"fresh": 80000, "three_years": 130000, "five_years_plus": 210000},
        "postgraduate_ratio": 0.50,
        "suitable_traits": ["化学好", "物理好", "喜欢实验", "科研能力强"],
        "unsuitable_people": ["不喜欢化学物理", "不喜欢实验"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男7:女3",
        "employment_prospect": "良好",
        "employment_rate": 0.86,
    },
    "市场营销": {
        "category": "管理学",
        "major_type": "工商管理类",
        "brief_intro": "市场营销与品牌管理，数字营销时代。",
        "introduction": "市场营销是在创造、沟通、传播和交换产品中，为顾客、客户、合作伙伴以及整个社会带来经济价值的活动、过程和体系。",
        "core_courses": ["市场营销学", "消费者行为学", "市场调研", "品牌管理", "数字营销"],
        "employment_directions": ["互联网运营", "广告", "品牌", "快消", "数字营销"],
        "typical_positions": ["市场经理", "品牌经理", "运营专员", "广告策划", "增长黑客"],
        "salary_range": {"fresh": 70000, "three_years": 120000, "five_years_plus": 200000},
        "postgraduate_ratio": 0.20,
        "suitable_traits": ["创意好", "沟通能力强", "数据敏感", "对用户心理敏感"],
        "unsuitable_people": ["内向", "缺乏创意", "不喜欢和人打交道"],
        "study_difficulty": "轻松",
        "course_load": "较轻",
        "gender_ratio": "男4:女6",
        "employment_prospect": "良好",
        "employment_rate": 0.88,
    },
    "人力资源管理": {
        "category": "管理学",
        "major_type": "工商管理类",
        "brief_intro": "人力资源开发与管理，企业战略伙伴。",
        "introduction": "人力资源管理是指在经济学与人本思想指导下，通过招聘、甄选、培训、报酬等管理形式对组织内外相关人力资源进行有效运用。",
        "core_courses": ["人力资源管理", "组织行为学", "薪酬管理", "招聘与配置", "绩效管理"],
        "employment_directions": ["企业HR", "猎头", "咨询", "劳务派遣", "组织发展"],
        "typical_positions": ["HRBP", "招聘经理", "薪酬专员", "培训专员", "猎头顾问"],
        "salary_range": {"fresh": 60000, "three_years": 100000, "five_years_plus": 170000},
        "postgraduate_ratio": 0.20,
        "suitable_traits": ["沟通能力强", "察言观色", "耐心细致", "同理心强"],
        "unsuitable_people": ["不喜欢和人打交道", "缺乏耐心"],
        "study_difficulty": "轻松",
        "course_load": "较轻",
        "gender_ratio": "男2.5:女7.5",
        "employment_prospect": "良好",
        "employment_rate": 0.87,
    },
    "统计学": {
        "category": "理学",
        "major_type": "统计学类",
        "brief_intro": "统计理论与数据分析，数据时代热门。",
        "introduction": "统计学是通过搜索、整理、分析、描述数据等手段，以达到推断所测对象的本质，甚至预测对象未来的一门综合性科学。",
        "core_courses": ["概率论", "数理统计", "应用回归分析", "多元统计分析", "抽样调查"],
        "employment_directions": ["金融", "数据科学", "生物统计", "市场研究", "政府统计"],
        "typical_positions": ["数据分析师", "统计学家", "精算师", "数据科学家", "BI工程师"],
        "salary_range": {"fresh": 100000, "three_years": 170000, "five_years_plus": 280000},
        "postgraduate_ratio": 0.50,
        "suitable_traits": ["数学好", "对数据敏感", "编程能力强"],
        "unsuitable_people": ["数学差", "不喜欢数字"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男5:女5",
        "employment_prospect": "极好",
        "employment_rate": 0.92,
    },
    "国际经济与贸易": {
        "category": "经济学",
        "major_type": "经济与贸易类",
        "brief_intro": "国际贸易与商务，全球化专业。",
        "introduction": "国际经济与贸易是研究国际贸易发生的原因、国际贸易政策、国际贸易实务、跨国投资以及国际贸易与经济发展关系的一门学科。",
        "core_courses": ["国际贸易", "国际贸易实务", "国际金融", "外贸函电", "跨境电商"],
        "employment_directions": ["外贸", "跨境电商", "跨国公司", "海关", "国际金融"],
        "typical_positions": ["外贸业务员", "跨境运营", "报关员", "国际采购", "涉外律师"],
        "salary_range": {"fresh": 70000, "three_years": 120000, "five_years_plus": 200000},
        "postgraduate_ratio": 0.25,
        "suitable_traits": ["英语好", "沟通能力强", "外向", "对国际贸易感兴趣"],
        "unsuitable_people": ["英语差", "内向"],
        "study_difficulty": "轻松",
        "course_load": "适中",
        "gender_ratio": "男4:女6",
        "employment_prospect": "一般",
        "employment_rate": 0.83,
    },
    "电子商务": {
        "category": "管理学",
        "major_type": "电子商务类",
        "brief_intro": "电子商务与数字商务，互联网+时代。",
        "introduction": "电子商务是指以信息网络技术为手段，以商品交换为中心的商务活动。",
        "core_courses": ["电子商务概论", "网络营销", "供应链管理", "电商运营", "数据分析"],
        "employment_directions": ["电商运营", "跨境电商", "直播电商", "互联网产品", "供应链"],
        "typical_positions": ["电商运营", "直播运营", "跨境运营", "产品经理", "供应链专员"],
        "salary_range": {"fresh": 80000, "three_years": 130000, "five_years_plus": 200000},
        "postgraduate_ratio": 0.15,
        "suitable_traits": ["互联网思维", "数据敏感", "执行能力强"],
        "unsuitable_people": ["不熟悉互联网", "执行能力弱"],
        "study_difficulty": "轻松",
        "course_load": "适中",
        "gender_ratio": "男4:女6",
        "employment_prospect": "良好",
        "employment_rate": 0.89,
    },
    "物流管理": {
        "category": "管理学",
        "major_type": "物流管理与工程类",
        "brief_intro": "现代物流与供应链管理。",
        "introduction": "物流管理是指在社会再生产过程中，根据物质资料实体流动的规律，应用管理的基本原理和科学方法，对物流活动进行计划、组织、指挥、协调、控制和监督。",
        "core_courses": ["物流管理", "供应链管理", "仓储管理", "运输管理", "采购管理"],
        "employment_directions": ["物流", "供应链", "电商", "快递", "航运"],
        "typical_positions": ["供应链经理", "物流专员", "仓储经理", "采购经理", "航运操作"],
        "salary_range": {"fresh": 60000, "three_years": 100000, "five_years_plus": 160000},
        "postgraduate_ratio": 0.15,
        "suitable_traits": ["组织协调好", "细心", "吃苦耐劳"],
        "unsuitable_people": ["吃不了苦", "粗心大意"],
        "study_difficulty": "轻松",
        "course_load": "适中",
        "gender_ratio": "男5.5:女4.5",
        "employment_prospect": "一般",
        "employment_rate": 0.86,
    },
    "旅游管理": {
        "category": "管理学",
        "major_type": "旅游管理类",
        "brief_intro": "旅游与酒店管理。",
        "introduction": "旅游管理是随着经济的发展而兴起的一门新兴学科，与工商管理并列管理学下的一级学科。",
        "core_courses": ["旅游学概论", "旅游经济学", "酒店管理", "旅游规划", "会展管理"],
        "employment_directions": ["旅游景区", "酒店", "OTA", "文旅策划", "会展"],
        "typical_positions": ["景区运营", "酒店经理", "旅游产品经理", "文旅策划师", "会展策划"],
        "salary_range": {"fresh": 50000, "three_years": 80000, "five_years_plus": 130000},
        "postgraduate_ratio": 0.15,
        "suitable_traits": ["外向开朗", "服务意识强", "兴趣广泛"],
        "unsuitable_people": ["内向", "不喜欢服务行业"],
        "study_difficulty": "轻松",
        "course_load": "较轻",
        "gender_ratio": "男3:女7",
        "employment_prospect": "一般",
        "employment_rate": 0.80,
    },
    "历史学": {
        "category": "历史学",
        "major_type": "历史学类",
        "brief_intro": "历史研究与文化传承。",
        "introduction": "历史学是人类对自己的历史材料进行筛选和组合的知识形式。",
        "core_courses": ["中国古代史", "中国近代史", "世界古代史", "世界近代史", "史学概论"],
        "employment_directions": ["教育", "文博", "文化遗产", "新媒体", "公务员"],
        "typical_positions": ["历史教师", "博物馆馆员", "文化遗产研究员", "历史自媒体", "文旅策划"],
        "salary_range": {"fresh": 55000, "three_years": 90000, "five_years_plus": 150000},
        "postgraduate_ratio": 0.40,
        "suitable_traits": ["喜欢阅读", "记忆力好", "文字功底好"],
        "unsuitable_people": ["不喜欢历史", "记忆力差"],
        "study_difficulty": "适中",
        "course_load": "适中",
        "gender_ratio": "男5:女5",
        "employment_prospect": "一般",
        "employment_rate": 0.80,
    },
    "哲学": {
        "category": "哲学",
        "major_type": "哲学类",
        "brief_intro": "哲学思维与思辨，小众但深刻。",
        "introduction": "哲学是有严密逻辑系统的宇宙观，它研究宇宙的性质、宇宙内万事万物演化的总规律、人在宇宙中的位置等一些很基本的问题。",
        "core_courses": ["马克思主义哲学", "中国哲学史", "西方哲学史", "逻辑学", "伦理学"],
        "employment_directions": ["科研", "教育", "公务员", "出版", "咨询"],
        "typical_positions": ["哲学研究员", "大学教师", "公务员", "出版社编辑", "战略咨询"],
        "salary_range": {"fresh": 55000, "three_years": 90000, "five_years_plus": 150000},
        "postgraduate_ratio": 0.50,
        "suitable_traits": ["喜欢思考", "逻辑思维强", "阅读广泛"],
        "unsuitable_people": ["不喜欢思考抽象问题"],
        "study_difficulty": "适中",
        "course_load": "适中",
        "gender_ratio": "男6:女4",
        "employment_prospect": "一般",
        "employment_rate": 0.78,
    },
    "社会学": {
        "category": "法学",
        "major_type": "社会学类",
        "brief_intro": "社会研究与公共服务。",
        "introduction": "社会学是一门研究社会结构、社会运行、社会群体及社会变迁的社会科学。",
        "core_courses": ["社会学概论", "社会调查研究方法", "社会统计学", "组织社会学", "发展社会学"],
        "employment_directions": ["社会工作", "民政", "NGO", "市场研究", "用户研究"],
        "typical_positions": ["社会工作者", "社区工作者", "用户研究员", "政策研究员", "民政公务员"],
        "salary_range": {"fresh": 55000, "three_years": 90000, "five_years_plus": 140000},
        "postgraduate_ratio": 0.35,
        "suitable_traits": ["关注社会", "同理心强", "研究能力强"],
        "unsuitable_people": ["不关心社会", "缺乏同理心"],
        "study_difficulty": "适中",
        "course_load": "适中",
        "gender_ratio": "男4:女6",
        "employment_prospect": "一般",
        "employment_rate": 0.79,
    },
    "中医学": {
        "category": "医学",
        "major_type": "中医学类",
        "brief_intro": "传统中医诊疗，国粹传承。",
        "introduction": "中医学是研究人体生理、病理以及疾病的诊断和防治等的一门学科。",
        "core_courses": ["中医基础理论", "中医诊断学", "中药学", "方剂学", "中医内科学"],
        "employment_directions": ["中医院", "中药研发", "中医养生", "针灸推拿", "中西医结合"],
        "typical_positions": ["中医师", "针灸师", "中药师", "养生顾问", "中医科研"],
        "salary_range": {"fresh": 60000, "three_years": 120000, "five_years_plus": 220000},
        "postgraduate_ratio": 0.55,
        "suitable_traits": ["对中医有兴趣", "记忆力好", "耐心", "动手能力强"],
        "unsuitable_people": ["不相信中医", "记忆力差"],
        "study_difficulty": "较难",
        "course_load": "极重",
        "gender_ratio": "男5:女5",
        "employment_prospect": "良好",
        "employment_rate": 0.87,
    },
    "机器人工程": {
        "category": "工学",
        "major_type": "自动化类",
        "brief_intro": "机器人系统设计与开发，新兴热门专业。",
        "introduction": "机器人工程是集机械工程、电子工程、自动控制、计算机科学等多学科交叉融合的新兴专业。",
        "core_courses": ["机器人学", "运动控制", "机器视觉", "SLAM技术", "嵌入式系统"],
        "employment_directions": ["机器人", "智能制造", "自动驾驶", "服务机器人", "工业机器人"],
        "typical_positions": ["机器人算法工程师", "机械设计工程师", "SLAM工程师", "运动控制工程师", "机器人应用工程师"],
        "salary_range": {"fresh": 160000, "three_years": 260000, "five_years_plus": 420000},
        "postgraduate_ratio": 0.55,
        "suitable_traits": ["动手能力强", "喜欢机器人", "软硬件能力均衡"],
        "unsuitable_people": ["动手能力差", "不喜欢编程硬件"],
        "study_difficulty": "非常难",
        "course_load": "极重",
        "gender_ratio": "男8.5:女1.5",
        "employment_prospect": "极好",
        "employment_rate": 0.95,
    },
    "新能源材料与器件": {
        "category": "工学",
        "major_type": "材料类",
        "brief_intro": "新能源材料与储能器件，双碳时代热门。",
        "introduction": "新能源材料与器件专业是研究新能源材料的制备、结构、性能及器件应用的新兴专业。",
        "core_courses": ["新能源材料", "电化学原理", "电池技术", "光伏材料", "储能技术"],
        "employment_directions": ["新能源", "动力电池", "光伏", "储能", "半导体"],
        "typical_positions": ["电池研发工程师", "光伏工程师", "储能工程师", "材料研究员", "器件工程师"],
        "salary_range": {"fresh": 130000, "three_years": 200000, "five_years_plus": 320000},
        "postgraduate_ratio": 0.55,
        "suitable_traits": ["化学好", "物理好", "对新能源感兴趣", "科研能力强"],
        "unsuitable_people": ["化学差", "不喜欢做实验"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男7.5:女2.5",
        "employment_prospect": "极好",
        "employment_rate": 0.93,
    },
    "化学工程与工艺": {
        "category": "工学",
        "major_type": "化工与制药类",
        "brief_intro": "化学工艺与工业生产。",
        "introduction": "化学工程与工艺是研究化学工业生产过程中的共同规律，并用化学方法改变物质组成或性质来生产化学产品的一门工程学科。",
        "core_courses": ["化工原理", "化学反应工程", "化工热力学", "分离工程", "工艺设计"],
        "employment_directions": ["石油化工", "精细化工", "医药", "新材料", "环境保护"],
        "typical_positions": ["化工工程师", "工艺工程师", "研发工程师", "生产管理", "EHS工程师"],
        "salary_range": {"fresh": 80000, "three_years": 130000, "five_years_plus": 200000},
        "postgraduate_ratio": 0.40,
        "suitable_traits": ["化学好", "动手能力强", "耐心细致"],
        "unsuitable_people": ["化学差", "不喜欢实验"],
        "study_difficulty": "较难",
        "course_load": "较重",
        "gender_ratio": "男7:女3",
        "employment_prospect": "一般",
        "employment_rate": 0.85,
    },
    "环境工程": {
        "category": "工学",
        "major_type": "环境科学与工程类",
        "brief_intro": "环境污染治理与生态保护，政策利好。",
        "introduction": "环境工程是研究和从事防治环境污染和提高环境质量的科学技术。",
        "core_courses": ["环境工程原理", "水污染控制", "大气污染控制", "固体废弃物处理", "环境监测"],
        "employment_directions": ["环保", "水务", "固废处理", "大气治理", "ESG咨询"],
        "typical_positions": ["环保工程师", "水处理工程师", "环评工程师", "ESG顾问", "环境监测"],
        "salary_range": {"fresh": 70000, "three_years": 110000, "five_years_plus": 180000},
        "postgraduate_ratio": 0.45,
        "suitable_traits": ["关注环保", "化学好", "生物好"],
        "unsuitable_people": ["不关心环保", "化学差"],
        "study_difficulty": "适中",
        "course_load": "适中",
        "gender_ratio": "男6:女4",
        "employment_prospect": "良好",
        "employment_rate": 0.85,
    },
    "播音与主持艺术": {
        "category": "艺术学",
        "major_type": "戏剧与影视学类",
        "brief_intro": "播音主持与有声语言，需要艺考。",
        "introduction": "播音与主持艺术培养具备广播电视新闻传播、语言文学、播音学以及艺术、美学等多学科知识与能力的人才。",
        "core_courses": ["播音发声", "播音创作", "即兴口语表达", "节目主持", "配音艺术"],
        "employment_directions": ["广播电视", "新媒体", "商业主持", "配音", "公关"],
        "typical_positions": ["主持人", "主播", "配音演员", "商业主持人", "视频博主"],
        "salary_range": {"fresh": 60000, "three_years": 120000, "five_years_plus": 250000},
        "postgraduate_ratio": 0.10,
        "suitable_traits": ["口才好", "形象气质佳", "反应快", "表现欲强"],
        "unsuitable_people": ["口才差", "内向", "形象气质普通"],
        "study_difficulty": "轻松",
        "course_load": "较轻",
        "gender_ratio": "男4:女6",
        "employment_prospect": "一般",
        "employment_rate": 0.78,
    },
    "视觉传达设计": {
        "category": "艺术学",
        "major_type": "设计学类",
        "brief_intro": "视觉设计与品牌传播，需要艺考。",
        "introduction": "视觉传达设计是通过视觉媒介表现并传达给观众的设计，包括平面设计、UI设计、品牌设计等。",
        "core_courses": ["平面构成", "色彩构成", "图形设计", "排版设计", "品牌设计"],
        "employment_directions": ["广告", "互联网", "品牌", "出版", "UI设计"],
        "typical_positions": ["平面设计师", "UI设计师", "品牌设计师", "插画师", "动效设计师"],
        "salary_range": {"fresh": 70000, "three_years": 120000, "five_years_plus": 200000},
        "postgraduate_ratio": 0.15,
        "suitable_traits": ["审美能力强", "创意思维", "手绘/软件能力强"],
        "unsuitable_people": ["审美一般", "缺乏创意"],
        "study_difficulty": "轻松",
        "course_load": "适中",
        "gender_ratio": "男3:女7",
        "employment_prospect": "良好",
        "employment_rate": 0.85,
    },
    "政治学与行政学": {
        "category": "法学",
        "major_type": "政治学类",
        "brief_intro": "政治与公共行政，考公热门。",
        "introduction": "政治学与行政学是研究政治现象、政治制度以及行政管理的学科。",
        "core_courses": ["政治学原理", "行政学原理", "中国政府与政治", "公共政策", "比较政治"],
        "employment_directions": ["公务员", "政策研究", "行政管理", "新闻", "高校"],
        "typical_positions": ["公务员", "政策研究员", "行政专员", "党政干部", "高校辅导员"],
        "salary_range": {"fresh": 60000, "three_years": 100000, "five_years_plus": 150000},
        "postgraduate_ratio": 0.35,
        "suitable_traits": ["关注时政", "文字功底好", "综合能力强"],
        "unsuitable_people": ["不关心政治", "文字功底差"],
        "study_difficulty": "适中",
        "course_load": "适中",
        "gender_ratio": "男5:女5",
        "employment_prospect": "一般",
        "employment_rate": 0.82,
    },
    "侦查学": {
        "category": "法学",
        "major_type": "公安学类",
        "brief_intro": "刑事侦查与司法鉴定，警校特色。",
        "introduction": "侦查学是研究侦查活动及其规律的一门法学学科，主要研究刑事犯罪侦查的理论和方法。",
        "core_courses": ["侦查学总论", "刑事侦查", "痕迹检验", "刑事技术", "侦查讯问"],
        "employment_directions": ["公安机关", "国家安全", "检察系统", "司法鉴定", "企业合规"],
        "typical_positions": ["刑事警察", "经侦民警", "司法鉴定人", "反舞弊专员", "国家安全干部"],
        "salary_range": {"fresh": 80000, "three_years": 120000, "five_years_plus": 180000},
        "postgraduate_ratio": 0.15,
        "suitable_traits": ["正义感强", "逻辑推理好", "身体素质好", "观察力强"],
        "unsuitable_people": ["身体条件差", "逻辑推理弱"],
        "study_difficulty": "适中",
        "course_load": "适中",
        "gender_ratio": "男8:女2",
        "employment_prospect": "良好",
        "employment_rate": 0.90,
    },
    "治安学": {
        "category": "法学",
        "major_type": "公安学类",
        "brief_intro": "社会治安管理。",
        "introduction": "治安学是研究社会治安管理活动及其规律的一门学科。",
        "core_courses": ["治安学总论", "治安管理学", "治安案件查处", "社区警务", "应急管理"],
        "employment_directions": ["公安机关", "保安管理", "企业安保", "应急管理", "城市管理"],
        "typical_positions": ["治安民警", "派出所民警", "安保总监", "应急管理专员", "城市管理执法"],
        "salary_range": {"fresh": 75000, "three_years": 110000, "five_years_plus": 160000},
        "postgraduate_ratio": 0.10,
        "suitable_traits": ["责任感强", "沟通能力好", "身体素质好"],
        "unsuitable_people": ["身体条件差", "沟通能力弱"],
        "study_difficulty": "轻松",
        "course_load": "适中",
        "gender_ratio": "男8:女2",
        "employment_prospect": "良好",
        "employment_rate": 0.89,
    },
}


def get_all_provinces() -> List[str]:
    return PROVINCES


def get_all_subject_combinations() -> List[str]:
    return SUBJECT_COMBINATIONS


def get_all_cities() -> List[str]:
    return sorted(list(set([t["city"] for t in COLLEGE_TEMPLATES])))


def get_all_major_directions() -> List[str]:
    directions = set()
    for m in MAJOR_DATABASE.values():
        for d in m["directions"]:
            directions.add(d)
    return sorted(list(directions))


def get_all_majors() -> List[Dict]:
    majors = []
    for name, detail in MAJOR_DETAIL_DATABASE.items():
        base = MAJOR_DATABASE.get(name, {})
        majors.append({
            "name": name,
            "category": detail["category"],
            "major_type": detail["major_type"],
            "brief_intro": detail["brief_intro"],
            "subject_requirements": base.get("subject_requirements", []),
            "employment_direction": detail.get("employment_directions", base.get("employment_direction", [])),
            "study_difficulty": detail["study_difficulty"],
            "employment_prospect": detail["employment_prospect"],
        })
    return majors


def get_major_detail(major_name: str) -> Optional[Dict]:
    if major_name not in MAJOR_DETAIL_DATABASE:
        return None
    detail = MAJOR_DETAIL_DATABASE[major_name]
    base = MAJOR_DATABASE.get(major_name, {})
    result = {**detail}
    if "employment_directions" in result and "employment_direction" not in result:
        result["employment_direction"] = result.pop("employment_directions")
    result["name"] = major_name
    result["subject_requirements"] = base.get("subject_requirements", [])
    if not result.get("employment_direction"):
        result["employment_direction"] = base.get("employment_direction", [])
    if not result.get("typical_positions"):
        result["typical_positions"] = base.get("typical_positions", [])
    result["description"] = base.get("description", "")
    return result


def compare_majors(major_names: List[str]) -> List[Dict]:
    result = []
    for name in major_names:
        detail = get_major_detail(name)
        if detail:
            result.append(detail)
    return result


CITY_PROVINCE_MAP = {
    "北京": "北京", "上海": "上海", "广州": "广东", "深圳": "广东",
    "杭州": "浙江", "南京": "江苏", "成都": "四川", "武汉": "湖北",
    "西安": "陕西", "苏州": "江苏", "天津": "天津", "重庆": "重庆",
    "青岛": "山东", "长沙": "湖南", "郑州": "河南", "厦门": "福建",
    "合肥": "安徽", "福州": "福建", "济南": "山东", "大连": "辽宁",
    "沈阳": "辽宁", "哈尔滨": "黑龙江", "长春": "吉林", "南昌": "江西",
    "南宁": "广西", "昆明": "云南", "贵阳": "贵州", "太原": "山西",
    "石家庄": "河北", "兰州": "甘肃", "乌鲁木齐": "新疆", "呼和浩特": "内蒙古",
    "海口": "海南", "银川": "宁夏", "西宁": "青海", "拉萨": "西藏",
    "宁波": "浙江", "无锡": "江苏", "佛山": "广东", "东莞": "广东",
    "珠海": "广东", "中山": "广东", "温州": "浙江", "金华": "浙江",
    "烟台": "山东", "潍坊": "山东", "泉州": "福建", "徐州": "江苏",
    "常州": "江苏", "南通": "江苏", "惠州": "广东", "汕头": "广东",
    "咸阳": "陕西", "绵阳": "四川", "南充": "四川", "宜昌": "湖北",
    "襄阳": "湖北", "湘潭": "湖南", "株洲": "湖南", "洛阳": "河南",
    "开封": "河南", "秦皇岛": "河北", "保定": "河北", "唐山": "河北",
    "延吉": "吉林", "石河子": "新疆", "雅安": "四川", "徐州": "江苏",
    "威海": "山东", "扬州": "江苏", "镇江": "江苏", "桂林": "广西",
    "三亚": "海南", "大理": "云南", "丽江": "云南", "包头": "内蒙古",
}

EMPLOYMENT_INDUSTRIES = [
    "互联网/IT", "金融/银行/证券", "教育/培训", "医疗/医药/健康",
    "政府/事业单位/国企", "制造业/工业", "房地产/建筑", "零售/快消/电商",
    "咨询/专业服务", "文化传媒/广告", "能源/化工/环保", "汽车/交通/物流",
    "通信/运营商", "航空航天/国防军工", "农业/食品", "其他",
]

EMPLOYMENT_POSITION_TYPES = [
    "技术研发类", "产品/运营类", "市场/销售类", "职能管理类",
    "设计/创意类", "金融/投资类", "教育/科研类", "医疗/医药类",
    "生产/制造类", "公务员/事业单位", "服务/支持类", "其他",
]

CITY_SALARY_BASE = {
    "北京": 180000, "上海": 185000, "深圳": 190000, "广州": 150000,
    "杭州": 170000, "南京": 150000, "成都": 130000, "武汉": 130000,
    "西安": 120000, "苏州": 150000, "天津": 135000, "重庆": 120000,
    "青岛": 120000, "长沙": 120000, "郑州": 100000, "厦门": 140000,
    "合肥": 130000, "福州": 120000, "济南": 115000, "大连": 115000,
}

INDUSTRY_SALARY_FACTOR = {
    "互联网/IT": 1.3, "金融/银行/证券": 1.25, "教育/培训": 0.95,
    "医疗/医药/健康": 1.1, "政府/事业单位/国企": 0.9, "制造业/工业": 0.95,
    "房地产/建筑": 1.0, "零售/快消/电商": 0.9, "咨询/专业服务": 1.15,
    "文化传媒/广告": 0.95, "能源/化工/环保": 1.0, "汽车/交通/物流": 0.95,
    "通信/运营商": 1.1, "航空航天/国防军工": 1.05, "农业/食品": 0.8,
    "其他": 0.9,
}

POSITION_SALARY_FACTOR = {
    "技术研发类": 1.3, "产品/运营类": 1.1, "市场/销售类": 0.95,
    "职能管理类": 0.95, "设计/创意类": 1.0, "金融/投资类": 1.25,
    "教育/科研类": 0.9, "医疗/医药类": 1.05, "生产/制造类": 0.85,
    "公务员/事业单位": 0.85, "服务/支持类": 0.8, "其他": 0.85,
}

COLLEGE_TYPE_INDUSTRY_BIAS = {
    CollegeType.SCIENCE: {
        "互联网/IT": 0.35, "通信/运营商": 0.08, "制造业/工业": 0.12,
        "金融/银行/证券": 0.08, "政府/事业单位/国企": 0.08,
        "航空航天/国防军工": 0.05, "能源/化工/环保": 0.05,
        "汽车/交通/物流": 0.05, "咨询/专业服务": 0.04,
    },
    CollegeType.COMPREHENSIVE: {
        "互联网/IT": 0.20, "金融/银行/证券": 0.15, "教育/培训": 0.10,
        "政府/事业单位/国企": 0.10, "咨询/专业服务": 0.08,
        "文化传媒/广告": 0.06, "零售/快消/电商": 0.06,
        "制造业/工业": 0.06, "房地产/建筑": 0.05,
    },
    CollegeType.FINANCE: {
        "金融/银行/证券": 0.45, "咨询/专业服务": 0.12,
        "互联网/IT": 0.10, "零售/快消/电商": 0.08,
        "政府/事业单位/国企": 0.08, "房地产/建筑": 0.05,
    },
    CollegeType.NORMAL: {
        "教育/培训": 0.50, "政府/事业单位/国企": 0.15,
        "文化传媒/广告": 0.08, "互联网/IT": 0.08,
        "金融/银行/证券": 0.05,
    },
    CollegeType.MEDICAL: {
        "医疗/医药/健康": 0.70, "政府/事业单位/国企": 0.10,
        "教育/科研类": 0.08, "互联网/IT": 0.05,
    },
    CollegeType.AGRICULTURAL: {
        "农业/食品": 0.30, "政府/事业单位/国企": 0.15,
        "教育/培训": 0.12, "能源/化工/环保": 0.10,
        "互联网/IT": 0.08, "制造业/工业": 0.08,
    },
    CollegeType.POLITICAL: {
        "公务员/事业单位": 0.55, "政府/事业单位/国企": 0.15,
        "教育/培训": 0.08, "金融/银行/证券": 0.06,
    },
    CollegeType.LANGUAGE: {
        "教育/培训": 0.25, "文化传媒/广告": 0.15,
        "零售/快消/电商": 0.12, "金融/银行/证券": 0.10,
        "互联网/IT": 0.10, "咨询/专业服务": 0.08,
    },
    CollegeType.ART: {
        "设计/创意类": 0.30, "文化传媒/广告": 0.25,
        "教育/培训": 0.15, "互联网/IT": 0.10,
    },
    CollegeType.SPORT: {
        "教育/培训": 0.35, "服务/支持类": 0.20,
        "政府/事业单位/国企": 0.10, "文化传媒/广告": 0.08,
    },
    CollegeType.MILITARY: {
        "公务员/事业单位": 0.60, "政府/事业单位/国企": 0.15,
        "教育/培训": 0.08,
    },
}

COLLEGE_TYPE_POSITION_BIAS = {
    CollegeType.SCIENCE: {
        "技术研发类": 0.45, "产品/运营类": 0.12, "公务员/事业单位": 0.08,
        "金融/投资类": 0.06, "生产/制造类": 0.08, "教育/科研类": 0.07,
    },
    CollegeType.COMPREHENSIVE: {
        "技术研发类": 0.18, "产品/运营类": 0.15, "市场/销售类": 0.12,
        "职能管理类": 0.12, "金融/投资类": 0.10, "公务员/事业单位": 0.08,
        "教育/科研类": 0.08,
    },
    CollegeType.FINANCE: {
        "金融/投资类": 0.50, "职能管理类": 0.12, "市场/销售类": 0.10,
        "咨询/专业服务": 0.08, "产品/运营类": 0.06,
    },
    CollegeType.NORMAL: {
        "教育/科研类": 0.55, "公务员/事业单位": 0.15,
        "职能管理类": 0.08, "市场/销售类": 0.05,
    },
    CollegeType.MEDICAL: {
        "医疗/医药类": 0.65, "教育/科研类": 0.12,
        "公务员/事业单位": 0.08, "技术研发类": 0.05,
    },
    CollegeType.AGRICULTURAL: {
        "生产/制造类": 0.25, "教育/科研类": 0.18,
        "公务员/事业单位": 0.15, "技术研发类": 0.10,
        "市场/销售类": 0.08,
    },
    CollegeType.POLITICAL: {
        "公务员/事业单位": 0.60, "职能管理类": 0.12,
        "教育/科研类": 0.08, "市场/销售类": 0.05,
    },
    CollegeType.LANGUAGE: {
        "教育/科研类": 0.28, "市场/销售类": 0.15,
        "职能管理类": 0.12, "产品/运营类": 0.10,
        "服务/支持类": 0.08,
    },
    CollegeType.ART: {
        "设计/创意类": 0.45, "教育/科研类": 0.15,
        "市场/销售类": 0.10, "产品/运营类": 0.08,
    },
    CollegeType.SPORT: {
        "教育/科研类": 0.35, "服务/支持类": 0.25,
        "市场/销售类": 0.10, "公务员/事业单位": 0.08,
    },
    CollegeType.MILITARY: {
        "公务员/事业单位": 0.65, "教育/科研类": 0.12,
        "职能管理类": 0.08,
    },
}


def _generate_distribution(
    bias: Dict[str, float],
    all_items: List[str],
    total_count: int,
    base_salary: int,
    salary_factor_map: Dict[str, float],
) -> List[Dict]:
    result = []
    remaining = 1.0
    remaining_items = [i for i in all_items if i not in bias]
    for item, pct in bias.items():
        pct = max(0.01, min(pct, remaining - 0.01 * max(0, len(remaining_items))))
        count = int(total_count * pct)
        if count > 0:
            salary_factor = salary_factor_map.get(item, 1.0)
            salary_noise = random.uniform(0.85, 1.15)
            result.append({
                "name": item,
                "count": count,
                "percentage": round(pct, 4),
                "avg_salary": int(base_salary * salary_factor * salary_noise),
            })
        remaining -= pct
    if remaining > 0 and remaining_items:
        extra_pct = remaining / len(remaining_items)
        for item in remaining_items:
            if random.random() < 0.4:
                count = int(total_count * extra_pct)
                if count > 0:
                    salary_factor = salary_factor_map.get(item, 1.0)
                    salary_noise = random.uniform(0.85, 1.15)
                    result.append({
                        "name": item,
                        "count": count,
                        "percentage": round(extra_pct, 4),
                        "avg_salary": int(base_salary * salary_factor * salary_noise),
                    })
    total_pct = sum(r["percentage"] for r in result)
    if total_pct > 0:
        for r in result:
            r["percentage"] = round(r["percentage"] / total_pct, 4)
    result.sort(key=lambda x: -x["percentage"])
    return result


def _generate_city_distribution(
    college_province: str,
    college_city: str,
    level: CollegeLevel,
    total_count: int,
    base_salary: int,
) -> List[Dict]:
    tier1_cities = ["北京", "上海", "深圳", "广州", "杭州", "南京", "成都", "武汉", "西安", "苏州"]
    province_capitals = {
        "广东": ["广州", "深圳", "佛山", "东莞"], "江苏": ["南京", "苏州", "无锡", "常州", "南通"],
        "浙江": ["杭州", "宁波", "温州", "金华"], "山东": ["济南", "青岛", "烟台", "潍坊"],
        "四川": ["成都", "绵阳"], "湖北": ["武汉", "宜昌", "襄阳"],
        "湖南": ["长沙", "湘潭", "株洲"], "河南": ["郑州", "洛阳", "开封"],
        "福建": ["厦门", "福州", "泉州"], "安徽": ["合肥"],
        "陕西": ["西安", "咸阳"], "辽宁": ["大连", "沈阳"],
        "重庆": ["重庆"], "天津": ["天津"], "北京": ["北京"], "上海": ["上海"],
        "黑龙江": ["哈尔滨"], "吉林": ["长春", "延吉"],
        "江西": ["南昌"], "广西": ["南宁", "桂林"], "云南": ["昆明", "大理", "丽江"],
        "贵州": ["贵阳"], "山西": ["太原"], "河北": ["石家庄", "保定", "唐山", "秦皇岛"],
        "甘肃": ["兰州"], "新疆": ["乌鲁木齐", "石河子"], "内蒙古": ["呼和浩特", "包头"],
        "海南": ["海口", "三亚"], "宁夏": ["银川"], "青海": ["西宁"], "西藏": ["拉萨"],
    }
    result = []
    remaining = 1.0
    level_local_pref = {
        CollegeLevel.C9: 0.15, CollegeLevel.PROJECT_985: 0.20,
        CollegeLevel.PROJECT_211: 0.25, CollegeLevel.DOUBLE_FIRST_CLASS: 0.30,
        CollegeLevel.ORDINARY: 0.45,
    }
    local_pref = level_local_pref.get(level, 0.35)
    local_cities = province_capitals.get(college_province, [college_city])
    if college_city not in local_cities:
        local_cities = [college_city] + local_cities
    local_pct_per_city = local_pref / len(local_cities)
    for city in local_cities[:3]:
        pct = local_pct_per_city * (1.2 if city == college_city else 1.0)
        count = int(total_count * pct)
        if count > 0:
            city_base = CITY_SALARY_BASE.get(city, base_salary)
            salary_noise = random.uniform(0.9, 1.1)
            result.append({
                "city": city,
                "province": CITY_PROVINCE_MAP.get(city, college_province),
                "count": count,
                "percentage": round(pct, 4),
                "avg_salary": int(city_base * salary_noise),
            })
        remaining -= pct
    level_tier1_pref = {
        CollegeLevel.C9: 0.55, CollegeLevel.PROJECT_985: 0.45,
        CollegeLevel.PROJECT_211: 0.35, CollegeLevel.DOUBLE_FIRST_CLASS: 0.25,
        CollegeLevel.ORDINARY: 0.15,
    }
    tier1_pref = level_tier1_pref.get(level, 0.25)
    tier1_pct_per_city = tier1_pref / len(tier1_cities)
    for city in tier1_cities:
        if any(r["city"] == city for r in result):
            continue
        if random.random() < 0.7:
            pct = tier1_pct_per_city * random.uniform(0.6, 1.4)
            count = int(total_count * pct)
            if count > 0:
                city_base = CITY_SALARY_BASE.get(city, base_salary)
                salary_noise = random.uniform(0.9, 1.1)
                result.append({
                    "city": city,
                    "province": CITY_PROVINCE_MAP.get(city, college_province),
                    "count": count,
                    "percentage": round(pct, 4),
                    "avg_salary": int(city_base * salary_noise),
                })
                remaining -= pct
    if remaining > 0.05:
        other_province_cities = []
        for prov, cities in province_capitals.items():
            if prov != college_province:
                other_province_cities.extend(cities)
        random.shuffle(other_province_cities)
        num_other = min(8, int(remaining / 0.03))
        other_pct_per_city = remaining / max(1, num_other)
        for city in other_province_cities[:num_other]:
            if any(r["city"] == city for r in result):
                continue
            count = int(total_count * other_pct_per_city)
            if count > 0:
                city_base = CITY_SALARY_BASE.get(city, base_salary)
                salary_noise = random.uniform(0.9, 1.1)
                result.append({
                    "city": city,
                    "province": CITY_PROVINCE_MAP.get(city, college_province),
                    "count": count,
                    "percentage": round(other_pct_per_city, 4),
                    "avg_salary": int(city_base * salary_noise),
                })
    total_pct = sum(r["percentage"] for r in result)
    if total_pct > 0:
        for r in result:
            r["percentage"] = round(r["percentage"] / total_pct, 4)
    result.sort(key=lambda x: -x["percentage"])
    return result[:15]


def generate_employment_data(
    college_id: str,
    college_name: str,
    college_province: str,
    college_city: str,
    level: CollegeLevel,
    college_type: CollegeType,
    base_employment_rate: float,
    base_average_salary: int,
) -> "EmploymentDataDetail":
    from .schemas import (
        EmploymentDataDetail, EmploymentCityDistribution,
        EmploymentIndustryDistribution, EmploymentPositionDistribution,
        DataSource,
    )
    total_graduates_by_level = {
        CollegeLevel.C9: (3500, 5500),
        CollegeLevel.PROJECT_985: (3000, 5000),
        CollegeLevel.PROJECT_211: (2500, 4500),
        CollegeLevel.DOUBLE_FIRST_CLASS: (2000, 4000),
        CollegeLevel.ORDINARY: (1500, 3500),
    }
    grad_range = total_graduates_by_level.get(level, (2000, 3500))
    total_graduates = random.randint(grad_range[0], grad_range[1])
    data_source = DataSource.OFFICIAL if random.random() < 0.6 else DataSource.THIRD_PARTY
    industry_bias = COLLEGE_TYPE_INDUSTRY_BIAS.get(college_type, COLLEGE_TYPE_INDUSTRY_BIAS[CollegeType.COMPREHENSIVE])
    position_bias = COLLEGE_TYPE_POSITION_BIAS.get(college_type, COLLEGE_TYPE_POSITION_BIAS[CollegeType.COMPREHENSIVE])
    industry_dist_raw = _generate_distribution(
        industry_bias, EMPLOYMENT_INDUSTRIES, total_graduates, base_average_salary, INDUSTRY_SALARY_FACTOR
    )
    position_dist_raw = _generate_distribution(
        position_bias, EMPLOYMENT_POSITION_TYPES, total_graduates, base_average_salary, POSITION_SALARY_FACTOR
    )
    city_dist_raw = _generate_city_distribution(
        college_province, college_city, level, total_graduates, base_average_salary
    )
    industry_distribution = [
        EmploymentIndustryDistribution(
            industry=d["name"],
            count=d["count"],
            percentage=d["percentage"],
            avg_salary=d["avg_salary"],
        )
        for d in industry_dist_raw
    ]
    position_distribution = [
        EmploymentPositionDistribution(
            position_type=d["name"],
            count=d["count"],
            percentage=d["percentage"],
            avg_salary=d["avg_salary"],
        )
        for d in position_dist_raw
    ]
    city_distribution = [
        EmploymentCityDistribution(
            city=d["city"],
            province=d["province"],
            count=d["count"],
            percentage=d["percentage"],
            avg_salary=d["avg_salary"],
        )
        for d in city_dist_raw
    ]
    note = None
    if data_source == DataSource.THIRD_PARTY:
        note = "数据来自第三方就业调查机构样本统计，仅供参考"
    return EmploymentDataDetail(
        college_id=college_id,
        college_name=college_name,
        year=2025,
        total_graduates=total_graduates,
        employment_rate=round(base_employment_rate + random.uniform(-0.02, 0.02), 4),
        average_salary=base_average_salary,
        data_source=data_source,
        city_distribution=city_distribution,
        industry_distribution=industry_distribution,
        position_distribution=position_distribution,
        note=note,
    )
