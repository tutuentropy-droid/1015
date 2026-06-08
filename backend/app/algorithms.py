import math
from typing import List, Optional, Tuple
from sklearn.linear_model import LinearRegression
import numpy as np
from .schemas import (
    College, UserInput, CollegePrediction, VolunteerItem,
    VolunteerPlan, AdmissionData, Category, Major,
    MonteCarloCollegeResult, MonteCarloHistogramBin
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


def _compute_histogram_bins(simulated_probs: List[float], num_bins: int) -> List[MonteCarloHistogramBin]:
    if not simulated_probs:
        return []
    min_p = min(simulated_probs)
    max_p = max(simulated_probs)
    if min_p == max_p:
        min_p = max(0.0, min_p - 0.05)
        max_p = min(1.0, max_p + 0.05)
    bin_width = (max_p - min_p) / num_bins
    bins = []
    for i in range(num_bins):
        bin_start = min_p + i * bin_width
        bin_end = bin_start + bin_width
        if i == num_bins - 1:
            count = sum(1 for p in simulated_probs if bin_start <= p <= bin_end)
        else:
            count = sum(1 for p in simulated_probs if bin_start <= p < bin_end)
        probability = count / len(simulated_probs) if simulated_probs else 0
        bins.append(MonteCarloHistogramBin(
            bin_start=round(bin_start, 4),
            bin_end=round(bin_end, 4),
            count=count,
            probability=round(probability, 4),
        ))
    return bins


def _compute_stability_score(simulated_probs: List[float], std: float) -> float:
    if not simulated_probs:
        return 0.0
    mean_p = sum(simulated_probs) / len(simulated_probs)
    if mean_p == 0:
        return 0.0
    cv = std / mean_p
    stability = max(0.0, 1.0 - cv)
    return round(stability, 4)


def _get_volatility_rating(std: float, stability: float) -> str:
    if std < 0.03 or stability >= 0.85:
        return "录取概率极为稳定"
    elif std < 0.06 or stability >= 0.7:
        return "录取概率较为稳定"
    elif std < 0.10 or stability >= 0.55:
        return "存在一定波动"
    elif std < 0.15 or stability >= 0.4:
        return "波动较大，报考需谨慎"
    else:
        return "波动极大，不确定性高"


def monte_carlo_simulation(
    college: College,
    user_score: int,
    user_rank: int,
    province: str,
    subject_combination: Optional[str] = None,
    num_simulations: int = 1000,
    num_bins: int = 20,
    current_year: int = 2026,
) -> Optional[MonteCarloCollegeResult]:
    province_data = _get_college_province_data(college, province)
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

    predicted_rank = max(50, predicted_rank)
    predicted_score = max(400, min(750, predicted_score))

    base_probability = _calculate_probability(user_rank, int(predicted_rank), ranks)

    rank_residuals = []
    score_residuals = []
    X = np.array(sorted_years).reshape(-1, 1)
    y_rank = np.array(ranks)
    y_score = np.array(scores)

    if len(sorted_years) >= 2:
        rank_model = LinearRegression()
        rank_model.fit(X, y_rank)
        rank_pred_all = rank_model.predict(X)
        rank_residuals = list(y_rank - rank_pred_all)

        score_model = LinearRegression()
        score_model.fit(X, y_score)
        score_pred_all = score_model.predict(X)
        score_residuals = list(y_score - score_pred_all)

    if len(rank_residuals) < 2:
        rank_std = max(abs(predicted_rank * 0.05), 200)
    else:
        rank_std = float(np.std(rank_residuals, ddof=1))
        if rank_std < 50:
            rank_std = 50

    if len(score_residuals) < 2:
        score_std = max(predicted_score * 0.02, 5)
    else:
        score_std = float(np.std(score_residuals, ddof=1))
        if score_std < 3:
            score_std = 3

    np.random.seed(42 + hash(college.id) % 1000)

    simulated_probs = []
    for _ in range(num_simulations):
        noise_rank = np.random.normal(0, rank_std)
        noise_score = np.random.normal(0, score_std)

        sim_predicted_rank = max(50, predicted_rank + noise_rank)
        sim_predicted_score = max(400, min(750, predicted_score + noise_score))

        score_factor = 1.0
        if predicted_score > 0:
            score_factor = user_score / sim_predicted_score

        combined_rank = sim_predicted_rank
        if score_factor < 1.0:
            combined_rank = sim_predicted_rank / max(0.5, score_factor)
        elif score_factor > 1.0:
            combined_rank = sim_predicted_rank * max(0.7, 1 / score_factor)

        sim_prob = _calculate_probability(user_rank, int(combined_rank), ranks)
        sim_prob = max(0.0, min(1.0, sim_prob))
        simulated_probs.append(sim_prob)

    simulated_probs_arr = np.array(simulated_probs)
    mean_prob = float(np.mean(simulated_probs_arr))
    std_prob = float(np.std(simulated_probs_arr, ddof=1))
    median_prob = float(np.median(simulated_probs_arr))
    min_prob = float(np.min(simulated_probs_arr))
    max_prob = float(np.max(simulated_probs_arr))

    ci_lower_95 = float(np.percentile(simulated_probs_arr, 2.5))
    ci_upper_95 = float(np.percentile(simulated_probs_arr, 97.5))
    ci_lower_90 = float(np.percentile(simulated_probs_arr, 5))
    ci_upper_90 = float(np.percentile(simulated_probs_arr, 95))

    histogram_bins = _compute_histogram_bins(simulated_probs, num_bins)

    stability_score = _compute_stability_score(simulated_probs, std_prob)
    volatility_rating = _get_volatility_rating(std_prob, stability_score)

    return MonteCarloCollegeResult(
        college_id=college.id,
        college_name=college.name,
        base_probability=round(base_probability, 4),
        simulated_probability_mean=round(mean_prob, 4),
        simulated_probability_std=round(std_prob, 4),
        simulated_probability_median=round(median_prob, 4),
        ci_lower_95=round(ci_lower_95, 4),
        ci_upper_95=round(ci_upper_95, 4),
        ci_lower_90=round(ci_lower_90, 4),
        ci_upper_90=round(ci_upper_90, 4),
        min_simulated_probability=round(min_prob, 4),
        max_simulated_probability=round(max_prob, 4),
        histogram_bins=histogram_bins,
        stability_score=stability_score,
        volatility_rating=volatility_rating,
    )


def batch_monte_carlo_simulation(
    colleges: List[College],
    user_score: int,
    user_rank: int,
    province: str,
    subject_combination: Optional[str] = None,
    num_simulations: int = 1000,
    num_bins: int = 20,
) -> Tuple[List[MonteCarloCollegeResult], List[float]]:
    results = []
    all_min = 1.0
    all_max = 0.0
    for college in colleges:
        result = monte_carlo_simulation(
            college, user_score, user_rank, province,
            subject_combination, num_simulations, num_bins,
        )
        if result:
            results.append(result)
            all_min = min(all_min, result.ci_lower_95)
            all_max = max(all_max, result.ci_upper_95)

    all_min = max(0.0, all_min - 0.05)
    all_max = min(1.0, all_max + 0.05)
    if all_max - all_min < 0.1:
        all_max = all_min + 0.1

    bin_width = (all_max - all_min) / num_bins
    common_bins = [round(all_min + i * bin_width, 4) for i in range(num_bins + 1)]

    return results, common_bins
