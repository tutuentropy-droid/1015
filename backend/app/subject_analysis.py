from typing import List, Dict, Optional, Tuple
from .schemas import (
    Major, MajorEligibility, DisciplineGroup, SubjectAnalysisResult,
    CombinationCompareItem, CombinationCompareResult, SubjectRequirementRule,
    DisciplineCategory
)


NEW_GAO_KAO_PROVINCES = [
    "北京", "上海", "浙江", "山东", "天津", "海南",
    "河北", "辽宁", "江苏", "福建", "湖北", "湖南",
    "广东", "重庆", "黑龙江", "吉林", "安徽", "江西",
    "广西", "贵州", "甘肃",
]


PROVINCE_POLICY: Dict[str, str] = {
    "北京": "3+3",
    "上海": "3+3",
    "浙江": "3+3",
    "山东": "3+3",
    "天津": "3+3",
    "海南": "3+3",
    "河北": "3+1+2",
    "辽宁": "3+1+2",
    "江苏": "3+1+2",
    "福建": "3+1+2",
    "湖北": "3+1+2",
    "湖南": "3+1+2",
    "广东": "3+1+2",
    "重庆": "3+1+2",
    "黑龙江": "3+1+2",
    "吉林": "3+1+2",
    "安徽": "3+1+2",
    "江西": "3+1+2",
    "广西": "3+1+2",
    "贵州": "3+1+2",
    "甘肃": "3+1+2",
}


MAJOR_CATEGORY_MAP: Dict[str, str] = {
    "计算机科学与技术": "工学",
    "软件工程": "工学",
    "人工智能": "工学",
    "数据科学与大数据技术": "工学",
    "电子信息工程": "工学",
    "通信工程": "工学",
    "自动化": "工学",
    "机器人工程": "工学",
    "机械工程": "工学",
    "车辆工程": "工学",
    "航空航天工程": "工学",
    "材料科学与工程": "工学",
    "新能源材料与器件": "工学",
    "化学工程与工艺": "工学",
    "药学": "医学",
    "临床医学": "医学",
    "口腔医学": "医学",
    "中医学": "医学",
    "金融学": "经济学",
    "经济学": "经济学",
    "会计学": "管理学",
    "法学": "法学",
    "汉语言文学": "文学",
    "英语": "文学",
    "新闻学": "文学",
    "数学与应用数学": "理学",
    "物理学": "理学",
    "生物科学": "理学",
    "心理学": "理学",
    "建筑学": "工学",
    "土木工程": "工学",
    "工商管理": "管理学",
    "市场营销": "管理学",
    "人力资源管理": "管理学",
    "电子商务": "管理学",
    "统计学": "理学",
    "地理信息科学": "理学",
    "环境工程": "工学",
    "农业工程": "工学",
    "林学": "农学",
    "水产养殖学": "农学",
    "海洋科学": "理学",
    "大气科学": "理学",
    "历史学": "历史学",
    "哲学": "哲学",
    "社会学": "法学",
    "政治学与行政学": "法学",
    "国际经济与贸易": "经济学",
    "物流管理": "管理学",
    "旅游管理": "管理学",
    "播音与主持艺术": "艺术学",
    "视觉传达设计": "艺术学",
    "环境设计": "艺术学",
    "音乐表演": "艺术学",
    "美术学": "艺术学",
    "运动训练": "教育学",
    "社会体育指导与管理": "教育学",
    "侦查学": "法学",
    "治安学": "法学",
}


SUBJECT_REQUIREMENT_OVERRIDES: Dict[str, Dict[str, Dict]] = {
    "临床医学": {
        "3+3": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
        "3+1+2": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
    },
    "口腔医学": {
        "3+3": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
        "3+1+2": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
    },
    "中医学": {
        "3+3": {"required_subjects": ["化学"], "optional_subjects": ["生物", "物理"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学", "生物"]},
    },
    "药学": {
        "3+3": {"required_subjects": ["化学"], "optional_subjects": ["生物", "物理"]},
        "3+1+2": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
    },
    "人工智能": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学", "数学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "计算机科学与技术": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "软件工程": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "数据科学与大数据技术": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学", "数学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "机械工程": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "航空航天工程": {
        "3+3": {"required_subjects": ["物理", "化学"], "optional_subjects": []},
        "3+1+2": {"required_subjects": ["物理", "化学"], "optional_subjects": []},
    },
    "材料科学与工程": {
        "3+3": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
        "3+1+2": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
    },
    "化学工程与工艺": {
        "3+3": {"required_subjects": ["化学"], "optional_subjects": ["物理"]},
        "3+1+2": {"required_subjects": ["物理", "化学"], "optional_subjects": []},
    },
    "环境工程": {
        "3+3": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
        "3+1+2": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
    },
    "土木工程": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "建筑学": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学", "历史"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "数学与应用数学": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "物理学": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学", "数学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "生物科学": {
        "3+3": {"required_subjects": ["化学", "生物"], "optional_subjects": ["物理"]},
        "3+1+2": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
    },
    "电子信息工程": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "通信工程": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "自动化": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "机器人工程": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "车辆工程": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "新能源材料与器件": {
        "3+3": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
        "3+1+2": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
    },
    "统计学": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "地理信息科学": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学", "地理"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学", "地理"]},
    },
    "大气科学": {
        "3+3": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["化学"]},
    },
    "海洋科学": {
        "3+3": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
        "3+1+2": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
    },
    "农业工程": {
        "3+3": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
        "3+1+2": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
    },
    "林学": {
        "3+3": {"required_subjects": ["化学", "生物"], "optional_subjects": ["物理"]},
        "3+1+2": {"required_subjects": ["物理", "化学"], "optional_subjects": ["生物"]},
    },
    "水产养殖学": {
        "3+3": {"required_subjects": ["化学", "生物"], "optional_subjects": ["物理"]},
        "3+1+2": {"required_subjects": ["化学", "生物"], "optional_subjects": ["物理"]},
    },
    "心理学": {
        "3+3": {"required_subjects": [], "optional_subjects": ["物理", "生物", "化学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["生物", "化学"]},
    },
    "侦查学": {
        "3+3": {"required_subjects": ["政治"], "optional_subjects": ["物理", "化学"]},
        "3+1+2": {"required_subjects": ["物理"], "optional_subjects": ["政治", "化学"]},
    },
}


def _get_province_policy(province: Optional[str]) -> str:
    if province and province in PROVINCE_POLICY:
        return PROVINCE_POLICY[province]
    return "3+1+2"


def _get_requirement_for_major(major_name: str, province: Optional[str]) -> Tuple[List[str], List[str]]:
    policy = _get_province_policy(province)
    if major_name in SUBJECT_REQUIREMENT_OVERRIDES:
        rule = SUBJECT_REQUIREMENT_OVERRIDES[major_name]
        if policy in rule:
            return rule[policy]["required_subjects"], rule[policy]["optional_subjects"]
    return [], []


def _check_eligibility(
    major: Major,
    user_subjects: List[str],
    province: Optional[str],
) -> Tuple[bool, Optional[str]]:
    required, optional = _get_requirement_for_major(major.name, province)

    if not required:
        if major.subject_requirements:
            required = list(major.subject_requirements)

    if not required:
        return True, None

    user_subject_set = set(user_subjects)
    missing = [s for s in required if s not in user_subject_set]

    if missing:
        reason = f"该专业要求必选{missing[0]}"
        if len(missing) > 1:
            reason = f"该专业要求必选{'、'.join(missing)}"
        if optional:
            reason += f"，可选{'、'.join(optional)}"
        return False, reason

    return True, None


def analyze_subjects(
    colleges,
    user_subjects: List[str],
    province: Optional[str] = None,
    college_ids: Optional[List[str]] = None,
) -> SubjectAnalysisResult:
    target_colleges = colleges
    if college_ids:
        id_set = set(college_ids)
        target_colleges = [c for c in colleges if c.id in id_set]

    all_eligibilities: List[MajorEligibility] = []
    college_stats = []

    for college in target_colleges:
        eligible_in_college = 0
        total_in_college = 0
        for major in college.majors:
            eligible, reason = _check_eligibility(major, user_subjects, province)
            total_in_college += 1
            if eligible:
                eligible_in_college += 1
            all_eligibilities.append(MajorEligibility(
                major=major,
                eligible=eligible,
                reason=reason,
                college_id=college.id,
                college_name=college.name,
            ))
        college_stats.append({
            "college_id": college.id,
            "college_name": college.name,
            "total_majors": total_in_college,
            "eligible_majors": eligible_in_college,
            "ineligible_majors": total_in_college - eligible_in_college,
            "eligible_rate": round(eligible_in_college / total_in_college, 4) if total_in_college > 0 else 0,
        })

    seen_majors: Dict[str, MajorEligibility] = {}
    for e in all_eligibilities:
        key = e.major.name
        if key not in seen_majors:
            seen_majors[key] = e
        else:
            if e.eligible and not seen_majors[key].eligible:
                seen_majors[key] = e

    unique_eligibilities = list(seen_majors.values())

    groups_map: Dict[str, List[MajorEligibility]] = {}
    for e in unique_eligibilities:
        category = MAJOR_CATEGORY_MAP.get(e.major.name, "其他")
        if category not in groups_map:
            groups_map[category] = []
        groups_map[category].append(e)

    discipline_groups: List[DisciplineGroup] = []
    category_order = [
        "工学", "理学", "医学", "经济学", "管理学",
        "法学", "文学", "历史学", "哲学", "农学",
        "教育学", "艺术学", "其他",
    ]
    for cat in category_order:
        if cat in groups_map:
            majors = groups_map[cat]
            eligible_count = sum(1 for m in majors if m.eligible)
            discipline_groups.append(DisciplineGroup(
                category=cat,
                majors=majors,
                eligible_count=eligible_count,
                total_count=len(majors),
            ))

    total = len(unique_eligibilities)
    eligible = sum(1 for e in unique_eligibilities if e.eligible)

    return SubjectAnalysisResult(
        subjects=user_subjects,
        total_majors=total,
        eligible_majors=eligible,
        ineligible_majors=total - eligible,
        eligible_rate=round(eligible / total, 4) if total > 0 else 0,
        discipline_groups=discipline_groups,
        college_stats=college_stats,
    )


def compare_combinations(
    colleges,
    combinations: List[List[str]],
    province: Optional[str] = None,
    college_ids: Optional[List[str]] = None,
) -> CombinationCompareResult:
    items: List[CombinationCompareItem] = []

    for combo in combinations:
        analysis = analyze_subjects(colleges, combo, province, college_ids)
        combo_label = "+".join(combo) if combo else "不限"
        items.append(CombinationCompareItem(
            combination=combo,
            combination_label=combo_label,
            total_majors=analysis.total_majors,
            eligible_majors=analysis.eligible_majors,
            ineligible_majors=analysis.ineligible_majors,
            eligible_rate=analysis.eligible_rate,
            by_college=analysis.college_stats,
        ))

    return CombinationCompareResult(items=items)


def get_subject_requirements(
    major_name: str,
    province: Optional[str] = None,
) -> SubjectRequirementRule:
    required, optional = _get_requirement_for_major(major_name, province)
    note = None
    if province and province in PROVINCE_POLICY:
        policy = PROVINCE_POLICY[province]
        note = f"{province}采用{policy}模式"
    return SubjectRequirementRule(
        major_id=major_name,
        major_name=major_name,
        province=province or "通用",
        required_subjects=required,
        optional_subjects=optional,
        requirement_note=note,
    )
