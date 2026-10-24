# WorkInsight AI

**An AI-assisted system for evidence extraction, evidence sufficiency assessment, and adaptive follow-up questioning in workplace competency evaluations.**

## Overview

WorkInsight AI is a prototype designed to analyze responses to workplace competency-based scenarios. It uses a locally running Large Language Model (LLM) to extract relevant evidence from a candidate's response and assess whether the available information meets predefined evidence sufficiency criteria.

When the extracted evidence is insufficient, the system can generate follow-up questions to gather additional information. The application then presents the extracted evidence, assessment results, identified gaps, and a consolidated report.

The project explores how AI can support structured, evidence-based competency evaluation while making the assessment process more transparent.

## Problem Statement

Traditional competency assessments can be difficult to standardize when responses are evaluated without a structured approach to identifying relevant evidence. Responses may lack specific examples, omit important details, or fail to demonstrate the expected competency dimensions.

WorkInsight AI addresses this challenge by introducing a structured workflow that extracts evidence, checks its sufficiency against configured criteria, and identifies areas requiring further clarification.

## Key Features

* **Scenario-Based Assessment:** Accepts responses to workplace competency scenarios.
* **AI-Based Evidence Extraction:** Identifies relevant evidence from submitted responses.
* **Evidence Sufficiency Assessment:** Evaluates extracted evidence against configurable prototype criteria.
* **Adaptive Follow-Up Questions:** Generates questions intended to address missing evidence and information gaps.
* **Evidence Coverage Analysis:** Displays coverage information and identifies dimensions requiring additional evidence.
* **Assessment Report:** Presents the scenario, reviewed response, extracted evidence, coverage results, and relevant assessment findings.
* **Local LLM Integration:** Uses Ollama to run a language model locally.

## System Workflow

1. **Scenario Selection:** Select the competency and workplace scenario to assess.
2. **Response Submission:** Enter a response to the selected scenario.
3. **Evidence Extraction:** The LLM identifies relevant evidence from the response.
4. **Sufficiency Assessment:** The extracted evidence is evaluated against configured rules.
5. **Follow-Up Generation:** If evidence is insufficient, the system generates follow-up questions to address identified gaps.
6. **Additional Response:** Submit answers to the follow-up questions.
7. **Final Report:** Review the consolidated assessment, including evidence, coverage, and remaining gaps.

## Technology Stack

| Component              | Technology              | Purpose                                                        |
| ---------------------- | ----------------------- | -------------------------------------------------------------- |
| User Interface         | Streamlit               | Builds the interactive web application                         |
| Programming Language   | Python                  | Implements application logic and workflow orchestration        |
| Large Language Model   | Llama 3.2               | Supports evidence extraction and follow-up question generation |
| Local Model Runtime    | Ollama                  | Runs and serves the language model locally                     |
| Evidence Extraction    | Custom Python service   | Processes responses and extracts relevant evidence             |
| Sufficiency Assessment | Python rule-based logic | Checks extracted evidence against configured criteria          |
| Follow-Up Generation   | Custom Python service   | Generates questions for gathering additional evidence          |
| Version Control        | Git and GitHub          | Tracks and hosts the project source code                       |

## Project Structure

```text
Work-Insight-AI/
├── app.py
├── services/
│   ├── evidence_extractor.py
│   ├── evidence_sufficiency.py
│   └── followup_generator.py
├── .gitignore
├── requirements.txt
└── README.md
```

The project structure may include additional files depending on the current implementation.

### Core Modules

**`app.py`**
Provides the Streamlit interface and coordinates the assessment workflow.

**`services/evidence_extractor.py`**
Extracts relevant evidence from the submitted response using the configured language model.

**`services/evidence_sufficiency.py`**
Evaluates whether the extracted evidence meets the prototype's configured sufficiency criteria and identifies potential evidence gaps.

**`services/followup_generator.py`**
Generates follow-up questions intended to obtain additional information about missing evidence dimensions.

## Evidence Sufficiency Criteria

The current prototype uses configurable rules to determine whether the extracted evidence is sufficient to proceed.

The configured criteria include:

* At least 75% of the configured evidence dimensions must be covered.
* At least two explicit evidence items must be identified, with supporting quotes that can be checked.

These thresholds are prototype configuration choices rather than scientifically validated measures of competency.

Meeting the sufficiency criteria indicates that the system has identified enough evidence according to its configured rules. It does not establish that the evidence is accurate or that the candidate has demonstrated the competency successfully.

## Installation and Setup

### Prerequisites

Install the following before running the application:

* Python
* Git
* Ollama
* Llama 3.2 model downloaded through Ollama

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Work-Insight-AI
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with the repository's actual clone URL.

### 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Start the Language Model

Install Ollama from its official website:

https://ollama.com/

Download the model:

```bash
ollama pull llama3.2
```

Ensure Ollama is running before launching the application.

### 5. Run the Application

From the project root, execute:

```bash
python -m streamlit run app.py
```

Streamlit will provide a local address through which the application can be accessed in a web browser.

## Limitations

* The application is a prototype and has not been validated for real-world employment decisions.
* Evidence extraction and follow-up question quality depend on the language model's outputs.
* Rule-based sufficiency checks do not independently establish the truth or reliability of extracted evidence.
* Evidence coverage depends on the configured dimensions and the quality of the extracted information.
* Local execution requires sufficient system resources to run the selected language model.
* The system is intended to support structured assessment workflows, not replace human judgment.

## Future Enhancements

Potential areas for further development include:

* More robust evidence validation and consistency checks.
* Improved identification of ambiguous or contradictory responses.
* Configurable competency frameworks and evidence dimensions.
* Enhanced traceability between extracted evidence and original responses.
* More comprehensive testing using representative assessment examples.
* Evaluation of extraction accuracy, question relevance, and sufficiency assessment reliability.

## Project Status

**Status:** Prototype under development.

WorkInsight AI demonstrates an initial workflow for extracting evidence from workplace scenario responses, checking evidence sufficiency, generating follow-up questions, and presenting assessment findings.

## License

A license has not yet been specified. Add an appropriate open-source license before distributing the project under specific reuse terms.
