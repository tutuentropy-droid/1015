from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List, Optional
from io import BytesIO
from .schemas import (
    College, UserInput, CollegePrediction, VolunteerPlan, Category,
    SubjectAnalysisRequest, SubjectAnalysisResult,
    CombinationCompareRequest, CombinationCompareResult,
    SubjectRequirementRule
)
from .data_generator import (
    get_all_provinces, get_all_subject_combinations, get_all_cities, get_all_major_directions,
    get_all_majors, get_major_detail, compare_majors
)
from .algorithms import filter_and_predict, generate_volunteer_plan
from .pdf_export import generate_plan_pdf
from .database import COLLEGES
from .subject_analysis import (
    analyze_subjects, compare_combinations, get_subject_requirements,
    NEW_GAO_KAO_PROVINCES, PROVINCE_POLICY
)

app = FastAPI(
    title="高考志愿填报决策系统",
    description="基于数据驱动的智能志愿填报辅助工具",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/meta/provinces", response_model=List[str], summary="获取所有省份列表")
def list_provinces():
    return get_all_provinces()


@app.get("/api/meta/subject-combinations", response_model=List[str], summary="获取选科组合列表")
def list_subject_combinations():
    return get_all_subject_combinations()


@app.get("/api/meta/cities", response_model=List[str], summary="获取所有可选城市列表")
def list_cities():
    return get_all_cities()


@app.get("/api/meta/major-directions", response_model=List[str], summary="获取专业方向列表")
def list_major_directions():
    return get_all_major_directions()


@app.get("/api/meta/categories", response_model=List[str], summary="获取冲稳保分组类别")
def list_categories():
    return [c.value for c in Category]


@app.get("/api/colleges", response_model=List[College], summary="查询院校列表")
def list_colleges(
    province: Optional[str] = None,
    city: Optional[str] = None,
    keyword: Optional[str] = None,
    level: Optional[str] = None,
    college_type: Optional[str] = None,
    limit: int = 50,
):
    result = COLLEGES
    if province:
        result = [c for c in result if c.province == province]
    if city:
        result = [c for c in result if c.city == city]
    if keyword:
        result = [c for c in result if keyword in c.name or any(keyword in t for t in c.tags)]
    if level:
        result = [c for c in result if c.level.value == level]
    if college_type:
        result = [c for c in result if c.college_type.value == college_type]
    return result[:limit]


@app.get("/api/colleges/{college_id}", response_model=College, summary="获取单个院校详情")
def get_college(college_id: str):
    for c in COLLEGES:
        if c.id == college_id:
            return c
    raise HTTPException(status_code=404, detail="院校不存在")


@app.post("/api/predict/colleges", response_model=List[CollegePrediction], summary="根据用户条件预测院校录取概率")
def predict_colleges(user_input: UserInput):
    predictions = filter_and_predict(COLLEGES, user_input)
    predictions.sort(key=lambda p: -p.probability)
    return predictions


@app.post("/api/plan/generate", response_model=VolunteerPlan, summary="生成完整志愿填报方案")
def generate_plan(user_input: UserInput):
    plan = generate_volunteer_plan(COLLEGES, user_input)
    return plan


@app.post("/api/plan/export-pdf", summary="导出生成的志愿方案为 PDF")
def export_plan_pdf(plan: VolunteerPlan):
    pdf_bytes = generate_plan_pdf(plan)
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=volunteer_plan.pdf"},
    )


@app.get("/api/meta/new-gaokao-provinces", response_model=List[dict], summary="获取新高考省份列表及模式")
def list_new_gaokao_provinces():
    return [
        {"province": p, "policy": PROVINCE_POLICY.get(p, "3+1+2")}
        for p in NEW_GAO_KAO_PROVINCES
    ]


@app.get("/api/meta/all-subjects", response_model=List[str], summary="获取所有可选科目")
def list_all_subjects():
    return ["物理", "化学", "生物", "历史", "政治", "地理"]


@app.post("/api/subject/analyze", response_model=SubjectAnalysisResult, summary="分析选科组合可报专业")
def analyze_subject_combination(req: SubjectAnalysisRequest):
    result = analyze_subjects(
        COLLEGES,
        req.subjects,
        req.province,
        req.college_ids if req.college_ids else None,
    )
    return result


@app.post("/api/subject/compare", response_model=CombinationCompareResult, summary="对比多个选科组合")
def compare_subject_combinations(req: CombinationCompareRequest):
    result = compare_combinations(
        COLLEGES,
        req.combinations,
        req.province,
        req.college_ids if req.college_ids else None,
    )
    return result


@app.get("/api/subject/requirement/{major_name}", response_model=SubjectRequirementRule, summary="查询某个专业的选科要求")
def get_major_subject_requirement(major_name: str, province: Optional[str] = None):
    return get_subject_requirements(major_name, province)


@app.get("/api/majors", summary="获取所有专业列表（带基本信息）")
def list_majors(category: Optional[str] = None, keyword: Optional[str] = None):
    majors = get_all_majors()
    if category:
        majors = [m for m in majors if m["category"] == category]
    if keyword:
        majors = [m for m in majors if keyword in m["name"] or keyword in m.get("brief_intro", "")]
    return majors


@app.get("/api/majors/{major_name}", summary="获取专业详情（含对比维度数据）")
def get_major(major_name: str):
    detail = get_major_detail(major_name)
    if not detail:
        raise HTTPException(status_code=404, detail="专业不存在")
    return detail


@app.post("/api/majors/compare", summary="对比多个专业")
def compare_majors_endpoint(major_names: List[str] = Body(...)):
    if len(major_names) < 2:
        raise HTTPException(status_code=400, detail="至少选择 2 个专业进行对比")
    if len(major_names) > 3:
        raise HTTPException(status_code=400, detail="最多对比 3 个专业")
    result = compare_majors(major_names)
    if len(result) < 2:
        raise HTTPException(status_code=400, detail="找到的有效专业不足 2 个")
    return result
