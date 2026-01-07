from __future__ import annotations
from typing import Optional, Dict, Any, List


def build_business_custom_prompt(
    query: str,
    user_inputs: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Build a business-analysis-focused custom prompt for write_report().
    This prompt does not change the output template - it only constrains style and content.

    Args:
        query: The original research task from the user.
        user_inputs: Optional dict for future extensibility (e.g. target_region, target_customer, competitors).

    Returns:
        A string to be passed as `custom_prompt` to ReportGenerator.write_report().
    """
    user_inputs = user_inputs or {}
    target_region = user_inputs.get("region", "")
    target_customer = user_inputs.get("customer", "")
    competitors: List[str] = user_inputs.get("competitors", []) or []
    competitors_hint = ""
    if competitors:
        competitors_hint = f"- 已知竞争对手（可选）：{', '.join(competitors)}\n"

    region_hint = f"- 目标地域（可选）：{target_region}\n" if target_region else ""
    customer_hint = f"- 目标客户（可选）：{target_customer}\n" if target_customer else ""

    # Three-part prompt: role + chapter rules + citation policy.
    role_block = (
        "你是一名资深商业分析师，请基于已检索与已汇总的上下文，输出一份严谨的行业分析报告。\n"
        "仅输出 Markdown 章节内容，不要加入任何多余解释或前后缀。\n"
        "任何关键结论尽量包含“时间/地域/数字/来源占位符[n]”。若数据缺失，请标注“数据缺口：……（待补充）”，不得臆测。\n"
    )

    input_block = (
        f"研究任务：{query}\n"
        f"{region_hint}{customer_hint}{competitors_hint}".strip()
    )

    chapter_rules = (
        "- 行业与市场：TAM/SAM/SOM（写明单位与年份）、CAGR（范围+年份）、关键驱动/制约（3–5 条）。\n"
        "- 客户与需求：细分画像、JTBD、典型使用场景（尽量量化）。\n"
        "- 竞争格局：列出 Top 3–5 对手，清晰差异点；给出文字化 SWOT（简洁要点）。\n"
        "- 商业模式与单元经济：收入结构、关键成本项、至少 1 个敏感性变量及其影响路径。\n"
        "- 合规与风险：监管要点、行业特有合规清单（如数据/牌照）。\n"
        "- Go-To-Market：获客渠道与转化路径、冷启动方法、前 3 个可落地动作。\n"
        "- 路线图：30/60/90 天里程碑（含可交付物/KPI）。\n"
        "- 每节 700–900 字，少形容词与重复，用要点/短段表达。\n"
    )

    citation_rules = (
        "引用规范：\n"
        "- 正文中使用 [n] 作为来源占位；\n"
        "- 文末统一列出 [n] 域名 | 标题/报告 | 年份；\n"
        "- 若不同来源冲突，择最新且权威者，并在文中以“（冲突说明）”标注；\n"
        "- 严禁编造链接；付费墙源以“（付费墙，保留摘要）”说明。\n"
    )

    content = (
        f"{role_block}\n"
        f"{input_block}\n\n"
        "写作要求（保持与你现有模板章节对应）：\n"
        f"{chapter_rules}\n"
        f"{citation_rules}\n"
        "请严格遵循以上要求完成写作。"
    )

    return content


