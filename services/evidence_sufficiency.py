"""Transparent, rule-based evidence sufficiency checks for WorkInsight AI."""


def assess_evidence_sufficiency(evidence_result, evidence_dimensions):
    """Evaluate whether extracted evidence covers enough competency dimensions.

    Prototype rules:
    - At least 75% of the configured dimensions must be covered.
    - At least two evidence items must have an explicit status and a verifiable
      supporting quote.

    These are transparent prototype thresholds, not a scientifically validated
    or employment decision rule.
    """
    dimensions = list(evidence_dimensions or [])
    covered = set(evidence_result.get("covered_dimensions", []))
    missing = [dimension for dimension in dimensions if dimension not in covered]

    items = evidence_result.get("evidence_items", [])
    verified_items = [
        item for item in items
        if isinstance(item, dict)
        and item.get("status") == "explicit"
        and isinstance(item.get("supporting_text"), str)
        and item.get("supporting_text", "").strip()
        and "did not provide a verifiable exact quote" not in item.get("supporting_text", "")
        and item.get("dimension") in dimensions
    ]

    total_dimensions = len(dimensions)
    covered_count = sum(1 for dimension in dimensions if dimension in covered)
    coverage_percent = round((covered_count / total_dimensions) * 100) if total_dimensions else 0

    coverage_requirement = 75
    evidence_item_requirement = 2
    is_sufficient = (
        total_dimensions > 0
        and coverage_percent >= coverage_requirement
        and len(verified_items) >= evidence_item_requirement
    )

    reasons = []
    if total_dimensions == 0:
        reasons.append("No competency dimensions were configured for this assessment.")
    else:
        reasons.append(
            f"{covered_count} of {total_dimensions} competency dimensions are covered "
            f"({coverage_percent}%; target: at least {coverage_requirement}%)."
        )
    reasons.append(
        f"{len(verified_items)} explicit evidence item(s) have a verifiable quote "
        f"(target: at least {evidence_item_requirement})."
    )
    if missing:
        reasons.append("Some competency dimensions still have no verified supporting evidence.")
    if evidence_result.get("ambiguities"):
        reasons.append(
            f"The extractor flagged {len(evidence_result['ambiguities'])} item(s) for clarification."
        )

    follow_up_targets = list(missing)
    for ambiguity in evidence_result.get("ambiguities", []):
        if isinstance(ambiguity, str) and ambiguity.strip() and ambiguity not in follow_up_targets:
            follow_up_targets.append(ambiguity)

    return {
        "is_sufficient": is_sufficient,
        "status": "Evidence appears sufficient for the next stage" if is_sufficient
                  else "More evidence may be needed",
        "coverage_percent": coverage_percent,
        "verified_evidence_count": len(verified_items),
        "missing_dimension_count": len(missing),
        "reasons": reasons,
        "follow_up_targets": follow_up_targets,
    }
