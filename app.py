import streamlit as st
from html import escape

from services.evidence_extractor import extract_evidence
from services.evidence_sufficiency import assess_evidence_sufficiency
from services.followup_generator import generate_followup_questions

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="WorkInsight AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)
if "evidence_result" not in st.session_state:
    st.session_state.evidence_result = None
if "sufficiency_result" not in st.session_state:
    st.session_state.sufficiency_result = None
if "follow_up_questions" not in st.session_state:
    st.session_state.follow_up_questions = []
if "follow_up_submitted" not in st.session_state:
    st.session_state.follow_up_submitted = False
if "assessment_response" not in st.session_state:
    st.session_state.assessment_response = ""


# ==================================================
# 2. COMPETENCY DATA
# ==================================================

COMPETENCIES = {
    "Teamwork": {
        "description": (
            "Collaboration, shared responsibility, "
            "and supporting team members."
        ),
        "scenario": (
            "Your team is working on an important project. "
            "One teammate is falling behind, and the deadline "
            "is approaching. What would you do?"
        ),
        "evidence_dimensions": [
            "Collaboration",
            "Support for teammates",
            "Shared responsibility",
            "Coordination",
        ],
    },

    "Communication": {
        "description": (
            "Clear communication, active listening, "
            "and appropriate information sharing."
        ),
        "scenario": (
            "Your project will be delayed because of an "
            "unexpected technical problem. How would you "
            "communicate this to your manager and team?"
        ),
        "evidence_dimensions": [
            "Clarity",
            "Transparency",
            "Active listening",
            "Appropriate communication",
        ],
    },

    "Conflict Resolution": {
        "description": (
            "Managing disagreements constructively "
            "and finding workable solutions."
        ),
        "scenario": (
            "Two team members strongly disagree about "
            "the technical approach to a project. Their "
            "disagreement is delaying progress. How would "
            "you handle the situation?"
        ),
        "evidence_dimensions": [
            "Understanding different perspectives",
            "Constructive discussion",
            "Conflict management",
            "Agreement or resolution",
        ],
    },

    "Problem Solving": {
        "description": (
            "Identifying problems, evaluating options, "
            "and choosing appropriate solutions."
        ),
        "scenario": (
            "Your team discovers a serious defect shortly "
            "before a project deadline. What steps would "
            "you take to address the problem?"
        ),
        "evidence_dimensions": [
            "Problem identification",
            "Root-cause analysis",
            "Evaluation of options",
            "Decision-making",
        ],
    },
}


# ==================================================
# 3. CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>
        .stApp {
            background-color: #090d0b;
            color: #f2f5f3;
        }

        [data-testid="stSidebar"] {
            background-color: #111814;
            border-right: 1px solid #28382e;
        }

        .brand {
            color: #48df91;
            font-size: 30px;
            font-weight: 800;
            letter-spacing: -1px;
        }

        .tagline {
            color: #9aa99f;
            font-size: 12px;
            letter-spacing: 1px;
        }

        .hero-label {
            color: #48df91;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 3px;
        }

        .hero-title {
            color: #f2f5f3;
            font-size: 44px;
            font-weight: 800;
            line-height: 1.15;
            margin-top: 12px;
        }

        .hero-title span {
            color: #48df91;
        }

        .description {
            color: #a1afa6;
            font-size: 15px;
            line-height: 1.8;
        }

        .scenario-card {
            background-color: #14251a;
            border: 1px solid #2b5039;
            padding: 24px;
            border-radius: 14px;
            margin: 15px 0 24px 0;
        }

        .scenario-label {
            color: #48df91;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 12px;
        }

        .scenario-text {
            color: #f2f5f3;
            font-size: 17px;
            line-height: 1.8;
        }

        .innovation-card {
            background-color: #111814;
            border: 1px solid #29382e;
            padding: 18px;
            border-radius: 12px;
            min-height: 150px;
        }

        .innovation-title {
            color: #48df91;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .innovation-description {
            color: #a1afa6;
            font-size: 13px;
            line-height: 1.7;
        }

        .footer {
            color: #87958c;
            font-size: 12px;
            text-align: center;
            margin-top: 45px;
            line-height: 1.8;
        }

        div.stButton > button[kind="primary"],
        div.stFormSubmitButton > button[kind="primary"] {
            background-color: #48df91;
            color: #08110b;
            border: none;
            font-weight: 700;
        }

        div.stButton > button[kind="primary"]:hover,
        div.stFormSubmitButton > button[kind="primary"]:hover {
            background-color: #36c87c;
            color: #08110b;
        }

        div[data-testid="stMetric"] {
            background-color: #111814;
            border: 1px solid #29382e;
            padding: 15px;
            border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# 4. SESSION STATE
# ==================================================

if "selected_competency" not in st.session_state:
    st.session_state.selected_competency = "Teamwork"

if "initial_response" not in st.session_state:
    st.session_state.initial_response = ""

if "response_submitted" not in st.session_state:
    st.session_state.response_submitted = False


# ==================================================
# 5. SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">WorkInsight AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="tagline">'
        'EVIDENCE-DRIVEN ASSESSMENT'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader("Assessment Setup")

    competency_names = list(COMPETENCIES.keys())

    selected_competency = st.selectbox(
        "Select a competency",
        options=competency_names,
        index=competency_names.index(
            st.session_state.selected_competency
        ),
    )

    if selected_competency != st.session_state.selected_competency:

        st.session_state.selected_competency = selected_competency

        st.session_state.initial_response = ""

        st.session_state.response_submitted = False
        st.session_state.evidence_result = None
        st.session_state.sufficiency_result = None
        st.session_state.follow_up_questions = []
        st.session_state.follow_up_submitted = False
        st.session_state.assessment_response = ""

        st.rerun()

    # Assessment Flow
    st.divider()
    st.subheader("Assessment Flow")

    st.markdown("🟢 **1. Competency Selection**")
    st.caption(f"Selected: {st.session_state.selected_competency}")

    if st.session_state.response_submitted:
        st.markdown("🟢 **2. Response Submission**")
        st.caption("Response received")
    else:
        st.markdown("⚪ **2. Response Submission**")
        st.caption("Waiting for your response")

    if st.session_state.evidence_result is not None:
        st.markdown("🟢 **3. AI Evidence Extraction**")
        st.caption("Evidence analysis completed")
    elif st.session_state.response_submitted:
        st.markdown("🟡 **3. AI Evidence Extraction**")
        st.caption("Awaiting successful extraction")
    else:
        st.markdown("⚪ **3. AI Evidence Extraction**")
        st.caption("Not started")

    if st.session_state.sufficiency_result is not None:
        st.markdown("🟢 **4. Evidence Sufficiency Check**")
        st.caption(st.session_state.sufficiency_result["status"])
    elif st.session_state.evidence_result is not None:
        st.markdown("🟡 **4. Evidence Sufficiency Check**")
        st.caption("Evaluating evidence")
    else:
        st.markdown("⚪ **4. Evidence Sufficiency Check**")
        st.caption("Waiting for evidence extraction")

    if st.session_state.follow_up_submitted:
        st.markdown("🟢 **5. Follow-up Questions**")
        st.caption("Answers received and evidence rechecked")
    elif st.session_state.follow_up_questions:
        st.markdown("🟡 **5. Follow-up Questions**")
        st.caption("Waiting for your answers")
    elif (
        st.session_state.sufficiency_result is not None
        and st.session_state.sufficiency_result.get("is_sufficient")
    ):
        st.markdown("🟢 **5. Follow-up Questions**")
        st.caption("Not needed — evidence appears sufficient")
    elif st.session_state.evidence_result is not None:
        st.markdown("🟡 **5. Follow-up Questions**")
        st.caption("Preparing targeted questions")
    else:
        st.markdown("⚪ **5. Follow-up Questions**")
        st.caption("Waiting for sufficiency check")

    if st.session_state.evidence_result is not None and st.session_state.sufficiency_result is not None:
        st.markdown("🟢 **6. Final Assessment Report**")
        st.caption("Report ready to review and download")
    else:
        st.markdown("⚪ **6. Final Assessment Report**")
        st.caption("Waiting for assessment results")

    st.caption("Prototype v0.1")


# ==================================================
# 6. MAIN HEADER
# ==================================================

st.markdown(
    """
    <div class="hero-label">
        INTELLIGENT WORKPLACE ASSESSMENT
    </div>

    <div class="hero-title">
        Understand behaviour.<br>
        <span>Evaluate evidence.</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

st.markdown(
    """
    <div class="description">
        Explore workplace scenarios and explain how you would
        approach real-world professional challenges. Our goal
        is to assess the evidence in your response rather than
        rely on unsupported assumptions.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


# ==================================================
# 7. INNOVATION CARDS
# ==================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="innovation-card">
            <div class="innovation-title">
                01 / Evidence-driven
            </div>
            <div class="innovation-description">
                Extract specific actions and explanations
                that support an assessment.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="innovation-card">
            <div class="innovation-title">
                02 / Evidence sufficiency
            </div>
            <div class="innovation-description">
                Identify missing information before
                drawing conclusions.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="innovation-card">
            <div class="innovation-title">
                03 / Adaptive questions
            </div>
            <div class="innovation-description">
                Ask relevant follow-up questions to
                gather additional evidence.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")
st.divider()


# ==================================================
# 8. SELECTED COMPETENCY
# ==================================================

competency = st.session_state.selected_competency

details = COMPETENCIES[competency]

st.subheader(f"01 / {competency}")

st.caption(details["description"])


# ==================================================
# 9. WORKPLACE SCENARIO
# ==================================================

st.markdown(
    """
    <style>
        .workplace-scenario {
            background: linear-gradient(
                135deg,
                #14251a,
                #0e1711
            );
            border: 1px solid #2b5039;
            border-left: 4px solid #48df91;
            border-radius: 14px;
            padding: 25px;
            margin: 12px 0 24px 0;
        }

        .workplace-scenario-label {
            color: #48df91;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2px;
            margin-bottom: 20px;
        }

        .workplace-scenario-text {
            color: #f2f5f3;
            font-size: 17px;
            line-height: 1.9;
        }

        .workplace-scenario-footer {
            color: #9aa99f;
            font-size: 12px;
            margin-top: 22px;
            padding-top: 15px;
            border-top: 1px solid #29382e;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):

    st.markdown(
        """
        <div class="workplace-scenario">
            <div class="workplace-scenario-label">
                YOUR WORKPLACE SCENARIO
            </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        details["scenario"],
    )

    st.caption(
        "Consider your actions, reasoning, and expected outcome."
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ==================================================
# 10. RESPONSE FORM
# ==================================================

st.subheader("02 / Your Response")

st.write(
    "Explain what you would do, why you would do it, "
    "and what outcome you would expect."
)

with st.form("response_form"):

    response = st.text_area(
        "Describe your approach",
        value=st.session_state.initial_response,
        placeholder=(
            "Describe the steps you would take, "
            "the reasons behind your decisions, and "
            "how you would handle the situation..."
        ),
        height=180,
        max_chars=5000,
    )

    submitted = st.form_submit_button(
        "Submit Response",
        type="primary",
        use_container_width=True,
    )

if submitted:

    cleaned_response = response.strip()

    if len(cleaned_response) < 10:
        st.error(
            "Please provide a response containing "
            "at least 10 characters."
        )
    else:
        st.session_state.initial_response = cleaned_response
        st.session_state.assessment_response = cleaned_response
        st.session_state.response_submitted = True
        st.session_state.evidence_result = None
        st.session_state.sufficiency_result = None
        st.session_state.follow_up_questions = []
        st.session_state.follow_up_submitted = False

        try:
            with st.spinner("Llama 3.2 is extracting evidence..."):
                evidence_result = extract_evidence(
                    competency=competency,
                    scenario=details["scenario"],
                    response=cleaned_response,
                    evidence_dimensions=details["evidence_dimensions"],
                )

            st.session_state.evidence_result = evidence_result

            sufficiency_result = assess_evidence_sufficiency(
                evidence_result=evidence_result,
                evidence_dimensions=details["evidence_dimensions"],
            )
            st.session_state.sufficiency_result = sufficiency_result

            if sufficiency_result["is_sufficient"]:
                st.success("Evidence extraction completed. Evidence appears sufficient for the next stage.")
            else:
                st.warning("Evidence extraction completed. More evidence may be needed.")
                follow_up_targets = sufficiency_result.get("follow_up_targets", [])

                with st.spinner("Generating targeted follow-up questions..."):
                    questions = generate_followup_questions(
                        competency=competency,
                        missing_dimensions=follow_up_targets,
                        ambiguities=evidence_result.get("ambiguities", []),
                        max_questions=3,
                    )

                # Ensure that the user still gets questions if the local model
                # returns an empty list or cannot generate questions.
                if not questions:
                    questions = [
                        f"What specific actions would you take to demonstrate "
                        f"{dimension.lower()} in this situation?"
                        for dimension in follow_up_targets[:3]
                    ]

                if not questions:
                    questions = [
                        "What specific steps would you take first, and why?",
                        "How would you coordinate with others and check progress?",
                        "What outcome would you expect, and how would you evaluate it?",
                    ]

                st.session_state.follow_up_questions = questions

        except (RuntimeError, ValueError) as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error(f"An unexpected error occurred: {exc}")



# 11. INITIAL WORKFLOW STATUS
# ==================================================

if st.session_state.response_submitted:

    st.divider()

    st.subheader("03 / Assessment Workflow")

    st.write(
        f"**Selected competency:** {competency}"
    )

    st.write(
        f"**Response length:** "
        f"{len(st.session_state.initial_response)} characters"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Evidence extraction",
            value="Completed" if st.session_state.evidence_result else "Pending",
        )

    with col2:
        st.metric(
            label="Final assessment",
            value="Pending",
        )



# ==================================================
# 12. EVIDENCE SUFFICIENCY AND ADAPTIVE FOLLOW-UPS
# ==================================================

if st.session_state.sufficiency_result is not None:
    sufficiency = st.session_state.sufficiency_result

    st.divider()
    st.subheader("04 / Evidence Sufficiency Check")

    if sufficiency.get("is_sufficient"):
        st.success(sufficiency.get("status", "Evidence appears sufficient."))
    else:
        st.warning(sufficiency.get("status", "More evidence may be needed."))

    metric1, metric2, metric3 = st.columns(3)
    with metric1:
        st.metric("Evidence coverage", f"{sufficiency.get('coverage_percent', 0)}%")
    with metric2:
        st.metric("Verified evidence items", sufficiency.get("verified_evidence_count", 0))
    with metric3:
        st.metric("Missing dimensions", sufficiency.get("missing_dimension_count", 0))

    st.markdown("**Why this result?**")
    for reason in sufficiency.get("reasons", []):
        st.write(f"- {reason}")

if (
    st.session_state.sufficiency_result is not None
    and not st.session_state.sufficiency_result.get("is_sufficient")
    and st.session_state.follow_up_questions
    and not st.session_state.follow_up_submitted
):
    st.divider()
    st.subheader("05 / Adaptive Follow-up Questions")
    st.write(
        "Your response may need additional evidence. Answer these targeted "
        "questions to clarify your approach."
    )

    with st.form("followup_form"):
        answers = {}
        for index, question in enumerate(st.session_state.follow_up_questions, start=1):
            answers[question] = st.text_area(
                f"Question {index}: {question}",
                key=f"follow_up_answer_{index}",
                max_chars=2000,
            )

        follow_up_submitted = st.form_submit_button(
            "Submit Follow-up Answers",
            type="primary",
            use_container_width=True,
        )

    if follow_up_submitted:
        unanswered = [question for question, answer in answers.items() if not answer.strip()]

        if unanswered:
            st.warning("Please answer all follow-up questions.")
        else:
            follow_up_text = "\n\nAdditional information from follow-up questions:\n" + "\n".join(
                f"Question: {question}\nAnswer: {answer.strip()}"
                for question, answer in answers.items()
            )
            combined_response = st.session_state.assessment_response + follow_up_text

            try:
                with st.spinner("Re-extracting evidence from your answers..."):
                    updated_evidence = extract_evidence(
                        competency=competency,
                        scenario=details["scenario"],
                        response=combined_response,
                        evidence_dimensions=details["evidence_dimensions"],
                    )
                    updated_sufficiency = assess_evidence_sufficiency(
                        evidence_result=updated_evidence,
                        evidence_dimensions=details["evidence_dimensions"],
                    )

                st.session_state.assessment_response = combined_response
                st.session_state.evidence_result = updated_evidence
                st.session_state.sufficiency_result = updated_sufficiency
                st.session_state.follow_up_submitted = True
                st.session_state.follow_up_questions = []
                st.rerun()
            except Exception as exc:
                st.error(f"Unable to re-evaluate the response: {exc}")

elif (
    st.session_state.sufficiency_result is not None
    and not st.session_state.sufficiency_result.get("is_sufficient")
    and not st.session_state.follow_up_questions
    and not st.session_state.follow_up_submitted
):
    st.info("The evidence may need manual review. If the question generator returned no questions, submit the original response again after checking that Ollama is running.")

elif (
    st.session_state.sufficiency_result is not None
    and st.session_state.sufficiency_result.get("is_sufficient")
):
    st.success("Follow-up questions are not needed at this stage because the evidence meets the prototype's sufficiency criteria.")


# ==================================================
# 13. EVIDENCE EXTRACTION RESULTS
# ==================================================

if st.session_state.evidence_result is not None:

    result = st.session_state.evidence_result

    st.divider()
    st.subheader("04 / Evidence Extraction Results")

    st.markdown("**Evidence Summary**")
    st.write(result.get("summary", "No summary was returned."))

    st.markdown("**Identified Evidence**")
    evidence_items = result.get("evidence_items", [])

    if evidence_items:
        for index, item in enumerate(evidence_items, start=1):
            with st.container(border=True):
                st.markdown(
                    f"**Evidence {index} / {item.get('dimension', 'Unspecified')}**"
                )
                st.write(item.get("evidence", ""))
                st.caption(
                    f"Type: {item.get('evidence_type', 'Not specified')} "
                    f"| Status: {item.get('status', 'Not specified')}"
                )
                st.caption("Supporting text from the response")
                st.write(f"“{item.get('supporting_text', '')}”")
    else:
        st.warning("No evidence items were identified in this response.")

    found_col, gap_col = st.columns(2)

    with found_col:
        st.markdown("**Evidence Found**")
        covered = result.get("covered_dimensions", [])
        if covered:
            for dimension in covered:
                st.success(dimension)
        else:
            st.info("No competency dimensions have been supported yet.")

    with gap_col:
        st.markdown("**Evidence Gaps**")
        missing = result.get("missing_dimensions", [])
        if missing:
            for dimension in missing:
                st.warning(dimension)
        else:
            st.success("Evidence was identified for every listed dimension.")

    st.markdown("**Items Requiring Clarification**")
    ambiguities = result.get("ambiguities", [])
    if ambiguities:
        for ambiguity in ambiguities:
            st.info(ambiguity)
    else:
        st.write("The model did not identify explicit ambiguities.")

    st.caption(
        "This is preliminary AI-generated evidence extraction, not a validated "
        "employee rating. Sufficiency thresholds are prototype rules and should "
        "not be used as a hiring or employment decision."
    )


# ==================================================
# 14. FINAL ASSESSMENT REPORT
# ==================================================

if (
    st.session_state.evidence_result is not None
    and st.session_state.sufficiency_result is not None
):
    result = st.session_state.evidence_result
    sufficiency = st.session_state.sufficiency_result

    st.divider()
    st.subheader("06 / Final Assessment Report")
    st.write(
        "Review the evidence and sufficiency findings below. "
        "This is an evidence summary for the prototype, not an employee rating."
    )

    report_status = sufficiency.get(
        "status",
        "Sufficiency status unavailable",
    )
    covered_dimensions = result.get("covered_dimensions", [])
    configured_dimensions = details.get("evidence_dimensions", [])
    missing_dimensions = [
        dimension
        for dimension in configured_dimensions
        if dimension not in covered_dimensions
    ]
    evidence_items = result.get("evidence_items", [])
    ambiguities = result.get("ambiguities", [])

    report_lines = [
        "WORKINSIGHT AI — FINAL ASSESSMENT REPORT",
        "=" * 48,
        "",
        f"Competency: {competency}",
        f"Scenario: {details['scenario']}",
        "",
        "RESPONSE",
        "-" * 48,
        st.session_state.assessment_response or st.session_state.initial_response or "No response recorded.",
        "",
        "EVIDENCE SUMMARY",
        "-" * 48,
        result.get("summary", "No summary was returned."),
        "",
        "SUFFICIENCY CHECK",
        "-" * 48,
        f"Status: {report_status}",
        f"Evidence coverage: {sufficiency.get('coverage_percent', 0)}%",
        f"Verified evidence items: {sufficiency.get('verified_evidence_count', 0)}",
        f"Missing dimensions: {sufficiency.get('missing_dimension_count', 0)}",
        "",
        "SUFFICIENCY REASONS",
    ]

    report_lines.extend(
        [f"- {reason}" for reason in sufficiency.get("reasons", [])]
        or ["- No reasons were provided."]
    )

    report_lines.extend(["", "IDENTIFIED EVIDENCE", "-" * 48])
    if evidence_items:
        for index, item in enumerate(evidence_items, start=1):
            if isinstance(item, dict):
                report_lines.extend([
                    f"{index}. Dimension: {item.get('dimension', 'Unspecified')}",
                    f"   Evidence: {item.get('evidence', '')}",
                    f"   Type: {item.get('evidence_type', 'Not specified')}",
                    f"   Status: {item.get('status', 'Not specified')}",
                    f"   Supporting text: {item.get('supporting_text', '')}",
                    "",
                ])
    else:
        report_lines.append("No evidence items were identified.")

    report_lines.extend(["", "DIMENSIONS WITH EVIDENCE", "-" * 48])
    report_lines.extend(
        [f"- {dimension}" for dimension in covered_dimensions]
        or ["- No competency dimensions were marked as covered."]
    )

    report_lines.extend(["", "EVIDENCE GAPS", "-" * 48])
    report_lines.extend(
        [f"- {dimension}" for dimension in missing_dimensions]
        or ["- No configured dimensions remain uncovered."]
    )

    report_lines.extend(["", "ITEMS REQUIRING CLARIFICATION", "-" * 48])
    report_lines.extend(
        [f"- {ambiguity}" for ambiguity in ambiguities]
        or ["- No explicit ambiguities were identified."]
    )

    report_lines.extend([
        "",
        "IMPORTANT NOTE",
        "-" * 48,
        "This report summarizes AI-extracted evidence and transparent prototype rules. "
        "It is not a validated employee rating and must not be used on its own for "
        "hiring, promotion, or other employment decisions.",
    ])

    report_text = "\n".join(report_lines)

    with st.container(border=True):
        st.markdown("**Report Overview**")
        st.write(f"**Competency:** {competency}")
        st.write(f"**Sufficiency status:** {report_status}")
        st.write(f"**Evidence coverage:** {sufficiency.get('coverage_percent', 0)}%")

        if sufficiency.get("is_sufficient"):
            st.success("The extracted evidence meets the prototype's configured sufficiency criteria.")
        else:
            st.warning("The extracted evidence does not yet meet all prototype sufficiency criteria.")

        st.markdown("**Assessment explanation**")
        for reason in sufficiency.get("reasons", []):
            st.write(f"- {reason}")

    st.download_button(
        label="Download Final Assessment Report (.txt)",
        data=report_text,
        file_name=f"workinsight_{competency.lower().replace(' ', '_')}_report.txt",
        mime="text/plain",
        type="primary",
        use_container_width=True,
    )


# ==================================================
# 15. FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer">
        WorkInsight AI · Evidence-driven workplace assessment
        <br>
        Prototype only. This version does not yet perform
        AI-based employee assessment.
    </div>
    """,
    unsafe_allow_html=True,
)

