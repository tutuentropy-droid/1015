import io
from typing import Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .schemas import VolunteerPlan, Category


def _try_register_cn_font():
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/Library/Fonts/Songti.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/arphic/uming.ttc",
    ]
    for p in font_paths:
        try:
            pdfmetrics.registerFont(TTFont("CNFont", p))
            return "CNFont"
        except Exception:
            continue
    return "Helvetica"


CN_FONT = _try_register_cn_font()


def _category_color(cat: Category) -> str:
    mapping = {
        Category.REACH: "#e74c3c",
        Category.STABLE: "#f39c12",
        Category.SAFE: "#27ae60",
    }
    return mapping.get(cat, "#333333")


def generate_plan_pdf(plan: VolunteerPlan) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleCN", parent=styles["Title"], fontName=CN_FONT, fontSize=22, leading=28, alignment=1, spaceAfter=20
    )
    h2_style = ParagraphStyle(
        "H2CN", parent=styles["Heading2"], fontName=CN_FONT, fontSize=16, leading=22, spaceBefore=12, spaceAfter=8
    )
    h3_style = ParagraphStyle(
        "H3CN", parent=styles["Heading3"], fontName=CN_FONT, fontSize=13, leading=18, spaceBefore=8, spaceAfter=6
    )
    body_style = ParagraphStyle(
        "BodyCN", parent=styles["BodyText"], fontName=CN_FONT, fontSize=10, leading=16
    )
    small_style = ParagraphStyle(
        "SmallCN", parent=styles["BodyText"], fontName=CN_FONT, fontSize=9, leading=14, textColor=colors.grey
    )
    bold_style = ParagraphStyle(
        "BoldCN", parent=styles["BodyText"], fontName=CN_FONT, fontSize=11, leading=16, spaceAfter=4
    )

    story = []
    ui = plan.user_input

    story.append(Paragraph("高考志愿填报方案", title_style))
    story.append(Spacer(1, 0.3 * cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#2c3e50")))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("一、考生信息", h2_style))
    info_data = [
        ["省份", ui.province, "高考分数", str(ui.score)],
        ["全省位次", str(ui.rank), "选科组合", ui.subject_combination],
        ["意向城市", "、".join(ui.acceptable_cities) if ui.acceptable_cities else "不限",
         "意向专业方向", "、".join(ui.target_major_directions) if ui.target_major_directions else "不限"],
        ["是否服从调剂", "是" if ui.accept_adjustment else "否",
         "志愿数量", str(ui.volunteer_count)],
    ]
    info_table = Table(info_data, colWidths=[2.5 * cm, 4 * cm, 2.5 * cm, 5 * cm])
    info_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), CN_FONT),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#ecf0f1")),
        ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#ecf0f1")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.6 * cm))

    story.append(Paragraph("二、方案总览", h2_style))
    story.append(Paragraph(
        f"共生成 <b>{len(plan.volunteers)}</b> 个志愿，其中：冲 <b>{plan.reach_count}</b> 所、"
        f"稳 <b>{plan.stable_count}</b> 所、保 <b>{plan.safe_count}</b> 所。",
        body_style
    ))
    story.append(Paragraph(
        f"综合录取成功率预估：<b>{plan.overall_success_probability * 100:.1f}%</b>",
        body_style
    ))
    story.append(Spacer(1, 0.3 * cm))

    legend_data = [
        [
            Paragraph("<font color='#e74c3c'><b>冲</b></font>", body_style),
            Paragraph("录取概率 10% ~ 45%，可冲刺更好的院校", small_style),
            Paragraph("<font color='#f39c12'><b>稳</b></font>", body_style),
            Paragraph("录取概率 45% ~ 80%，与考生水平匹配", small_style),
            Paragraph("<font color='#27ae60'><b>保</b></font>", body_style),
            Paragraph("录取概率 80% 以上，用于保底", small_style),
        ],
    ]
    legend_table = Table(legend_data, colWidths=[1 * cm, 4.5 * cm, 1 * cm, 4.5 * cm, 1 * cm, 4.5 * cm])
    legend_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(legend_table)
    story.append(Spacer(1, 0.6 * cm))

    story.append(Paragraph("三、志愿推荐列表", h2_style))

    for item in plan.volunteers:
        color = _category_color(item.category)
        story.append(Paragraph(
            f"<font color='{color}'><b>志愿 {item.order} [{item.category.value}]</b></font>　{item.college.name}",
            h3_style
        ))
        meta_data = [
            ["所在省市", f"{item.college.province} {item.college.city}",
             "院校层次", item.college.level.value],
            ["院校类型", item.college.college_type.value,
             "录取概率", f"{item.probability * 100:.1f}%"],
            ["预估录取位次", str(item.predicted_rank),
             "预估录取分数", str(item.predicted_score)],
        ]
        meta_table = Table(meta_data, colWidths=[2.5 * cm, 5 * cm, 2.5 * cm, 5 * cm])
        meta_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), CN_FONT),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f8f9fa")),
            ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#f8f9fa")),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#dee2e6")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 0.2 * cm))

        story.append(Paragraph(f"<b>推荐专业：</b>{item.recommended_major.name}", bold_style))
        story.append(Paragraph(
            f"就业方向：{'、'.join(item.recommended_major.employment_direction)}",
            body_style
        ))
        story.append(Paragraph(
            f"典型岗位：{'、'.join(item.recommended_major.typical_positions)}",
            small_style
        ))
        story.append(Spacer(1, 0.15 * cm))

        admission_headers = ["年份", "省份", "最低分", "最低位次", "批次"]
        admission_rows = [admission_headers]
        recent = item.college.admission_data[:6]
        for d in recent:
            admission_rows.append([
                str(d.year), d.province, str(d.score), str(d.rank), d.batch
            ])
        if len(admission_rows) > 1:
            story.append(Paragraph("<b>近年录取数据（节选）：</b>", body_style))
            a_table = Table(admission_rows, colWidths=[1.5 * cm, 2.2 * cm, 1.8 * cm, 2.2 * cm, 2.2 * cm])
            a_table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), CN_FONT),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#34495e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#bdc3c7")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(a_table)
            story.append(Spacer(1, 0.15 * cm))

        story.append(Paragraph(f"<b>大小年规律：</b>{item.size_year_pattern}", body_style))
        story.append(Paragraph(f"<b>调剂影响：</b>{item.adjustment_impact}", body_style))
        story.append(Spacer(1, 0.3 * cm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#bdc3c7")))
        story.append(Spacer(1, 0.3 * cm))

    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph("四、报考建议", h2_style))
    story.append(Paragraph("1. 本方案基于近年录取数据通过线性回归模型预测，仅供参考，实际录取结果受当年报考人数、招生计划等多种因素影响。", body_style))
    story.append(Paragraph("2. 建议遵循\"冲-稳-保\"的梯度原则，志愿之间保持合理分差。", body_style))
    story.append(Paragraph("3. 建议勾选\"服从调剂\"以降低退档风险，特别是对于冲刺类院校。", body_style))
    story.append(Paragraph("4. 注意目标院校的选科要求、身体条件、外语语种等特殊限制。", body_style))
    story.append(Paragraph("5. 最终填报前请务必查阅各院校官方招生简章和本省考试院发布的最新信息。", body_style))

    doc.build(story)
    return buffer.getvalue()
