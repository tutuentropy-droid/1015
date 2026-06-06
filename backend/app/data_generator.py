import random
from typing import List, Dict
from .schemas import (
    College, Major, AdmissionData, CollegeLevel, CollegeType, DisciplineLevel
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
        colleges.append(College(
            id=f"C{idx + 1:04d}",
            name=tpl["name"],
            province=tpl["province"],
            city=tpl["city"],
            level=tpl["level"],
            college_type=tpl["college_type"],
            description=f"{tpl['name']}是一所位于{tpl['city']}的知名高等院校。",
            majors=majors,
            admission_data=admission_data,
            tags=tpl["tags"],
            employment_rate=round(random.uniform(er_range[0], er_range[1]), 4),
            average_salary=random.randint(sal_range[0], sal_range[1]),
        ))
    return colleges


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
