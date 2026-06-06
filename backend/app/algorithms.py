import math
from typing import List, Optional, Tuple
from sklearn.linear_model import LinearRegression
import numpy as np
from .schemas import (
    College, UserInput, CollegePrediction, VolunteerItem,
    VolunteerPlan, AdmissionData, Category, Major
)


def _linear_regression_predict(years: List[int], values: List[int], target_year: int) -> Tuple[float, float]:
    if len(years) < 2:
        return values[-1] if values else 0, 0.0
    X = np.array(years).reshape(-1, 1)
    y = np.array(values)
    model = LinearRegression()
    model.fit(X, y)
    predicted = model.predict(np.array([[target_year]]))[0]
    slope = model.coef_[0] if hasattr(model, 'coef_') else 0
    return float(predicted), float(slope)


def _analyze_size_year_pattern(ranks: List[int], years: List[int]) -> str:
    if len(ranks) < 2:
        return "数据不足"
    diffs = []
    for i in range(1, len(ranks)):
        diffs.append(ranks[i] - ranks[i - 1])
    if not diffs:
        return "数据不足"
    alternating = all(diffs[i] * diffs[i - 1] < 0 for i in range(1, len(diffs)))
    if alternating and len(diffs) >= 2:
        return "明显大小年（建议结合趋势参考）"
    avg_change = sum(abs(d) for d in diffs) / len(diffs)
    avg_rank = sum(ranks) / len(ranks)
    volatility = avg_change / avg_rank if avg_rank > 0 else 0
    if volatility > 0.15:
        return "波动较大（报考需谨慎）"
    elif volatility > 0.08:
        return "存在一定波动"
    else:
        return "录取位次稳定"


def _compute_adjustment_impact(level: str, accept: bool) -> str:
    bonus_map = {
        "C9联盟": "+3~5%",
        "985工程": "+5~8%",
        "211工程": "+8~12%",
        "双一流": "+8~15%",
        "普通本科": "+10~20%",
    }
    bonus = bonus_map.get(level, "+5~10%")
    if accept:
        return f"服从调剂可提高录取概率约{bonus}"
    else:
        return f"不服从调剂可能降低录取概率约{bonus}，建议勾选"


def _get_college_province_data(college: College, province: str) -> List[AdmissionData]:
    return [d for d in college.admission_data if d.province == province]


def _match_majors(college: College, target_directions: List[str]) -> List[Major]:
    if not target_directions:
        return college.majors[:3]
    matched = []
    target_lower = [d.lower() for d in target_directions]
    for major in college.majors:
        dir_field = major.employment_direction + major.typical_positions
        for d in dir_field:
            if any(t in d.lower() for t in target_lower):
                matched.append(major)
                break
    if not matched:
        return college.majors[:3]
    return matched


def _calculate_probability(user_rank: int, predicted_rank: int, recent_ranks: List[int]) -> float:
    if predicted_rank <= 0:
        return 0.0
    if user_rank <= predicted_rank:
        ratio = predicted_rank / user_rank
        prob = 0.5 + 0.5 * (1 - math.exp(-(ratio - 1) * 2))
        return min(0.99, prob)
    else:
        ratio = user_rank / predicted_rank
        prob = 0.5 * math.exp(-(ratio - 1) * 1.5)
        return max(0.01, prob)


def _categorize(probability: float) -> Category:
    if probability >= 0.8:
        return Category.SAFE
    elif probability >= 0.45:
        return Category.STABLE
    else:
        return Category.REACH


def predict_college(college: College, user_input: UserInput, current_year: int = 2026) -> Optional[CollegePrediction]:
    province_data = _get_college_province_data(college, user_input.province)
    if not province_data:
        province_data = college.admission_data[:10]

    years = sorted(list(set(d.year for d in province_data)))
    if len(years) < 2:
        return None

    rank_by_year = {}
    score_by_year = {}
    for y in years:
        year_data = [d for d in province_data if d.year == y]
        if year_data:
            rank_by_year[y] = int(sum(d.rank for d in year_data) / len(year_data))
            score_by_year[y] = int(sum(d.score for d in year_data) / len(year_data))

    sorted_years = sorted(rank_by_year.keys())
    ranks = [rank_by_year[y] for y in sorted_years]
    scores = [score_by_year[y] for y in sorted_years]

    predicted_rank, rank_slope = _linear_regression_predict(sorted_years, ranks, current_year)
    predicted_score, _ = _linear_regression_predict(sorted_years, scores, current_year)

    predicted_rank = int(max(50, predicted_rank))
    predicted_score = int(max(400, min(750, predicted_score)))

    probability = _calculate_probability(user_input.rank, predicted_rank, ranks)
    category = _categorize(probability)

    size_year_pattern = _analyze_size_year_pattern(ranks, sorted_years)
    adjustment_impact = _compute_adjustment_impact(college.level.value, user_input.accept_adjustment)

    recent_data = []
    for y in sorted_years[-3:]:
        for d in province_data:
            if d.year == y:
                recent_data.append(d)
                break

    matching_majors = _match_majors(college, user_input.target_major_directions)

    return CollegePrediction(
        college=college,
        predicted_rank=predicted_rank,
        predicted_score=predicted_score,
        probability=round(probability, 4),
        category=category,
        size_year_pattern=size_year_pattern,
        adjustment_impact=adjustment_impact,
        recent_admission_data=recent_data,
        matching_majors=matching_majors,
    )


def filter_and_predict(
    colleges: List[College],
    user_input: UserInput,
) -> List[CollegePrediction]:
    predictions = []
    for college in colleges:
        if user_input.acceptable_cities and college.city not in user_input.acceptable_cities:
            continue
        pred = predict_college(college, user_input)
        if pred is not None:
            predictions.append(pred)
    return predictions


def generate_volunteer_plan(
    colleges: List[College],
    user_input: UserInput,
) -> VolunteerPlan:
    predictions = filter_and_predict(colleges, user_input)
    if not predictions:
        predictions = [predict_college(c, user_input) for c in colleges[:5]]
        predictions = [p for p in predictions if p is not None]

    predictions.sort(key=lambda p: (
        0 if p.category == Category.REACH else (1 if p.category == Category.STABLE else 2),
        -p.probability,
    ))

    reaches = [p for p in predictions if p.category == Category.REACH]
    stables = [p for p in predictions if p.category == Category.STABLE]
    safes = [p for p in predictions if p.category == Category.SAFE]

    total = user_input.volunteer_count
    n_reach = max(2, min(len(reaches), int(total * 0.3)))
    n_safe = max(2, min(len(safes), int(total * 0.3)))
    n_stable = total - n_reach - n_safe
    n_stable = max(1, min(len(stables), n_stable))

    selected = reaches[:n_reach] + stables[:n_stable] + safes[:n_safe]
    while len(selected) < total and len(predictions) > len(selected):
        remaining = [p for p in predictions if p not in selected]
        if remaining:
            selected.append(remaining[0])
        else:
            break

    selected = selected[:total]

    volunteers = []
    for idx, pred in enumerate(selected):
        major = pred.matching_majors[0] if pred.matching_majors else pred.college.majors[0]
        volunteers.append(VolunteerItem(
            order=idx + 1,
            college=pred.college,
            probability=pred.probability,
            category=pred.category,
            predicted_rank=pred.predicted_rank,
            predicted_score=pred.predicted_score,
            recommended_major=major,
            size_year_pattern=pred.size_year_pattern,
            adjustment_impact=pred.adjustment_impact,
        ))

    reach_count = sum(1 for v in volunteers if v.category == Category.REACH)
    stable_count = sum(1 for v in volunteers if v.category == Category.STABLE)
    safe_count = sum(1 for v in volunteers if v.category == Category.SAFE)

    if volunteers:
        fail_probs = [1 - v.probability for v in volunteers]
        overall_fail = 1.0
        for p in fail_probs:
            overall_fail *= p
        overall_success = 1 - overall_fail
    else:
        overall_success = 0.0

    return VolunteerPlan(
        user_input=user_input,
        volunteers=volunteers,
        reach_count=reach_count,
        stable_count=stable_count,
        safe_count=safe_count,
        overall_success_probability=round(overall_success, 4),
    )
