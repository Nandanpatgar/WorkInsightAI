# WorkInsight AI

### AI-Assisted Employee Competency Assessment and Behavioural Insights

WorkInsight AI is a technology-driven platform designed to analyse employee responses to structured workplace scenarios and generate meaningful behavioural insights. It aims to help HR professionals identify strengths, recognise development areas, and explore suitable training interventions through evidence-oriented assessment.

## Project Background

**Event:** Nexathon 2026
**Institution:** Shree Devi Institute of Technology, Mangaluru, Karnataka
**Team Name:** Clutch Crew
**Project Type:** Hackathon Prototype

### Problem Statement

> Develop a technology-driven platform that uses structured workplace scenarios and employee responses to generate meaningful behavioural insights for HR, helping organizations identify strengths, development areas and suitable training interventions.

WorkInsight AI was developed as a solution to this provided problem statement during Nexathon 2026.

## Project Objectives

* Analyse employee responses to structured workplace scenarios.
* Identify information relevant to predefined workplace competencies.
* Recognise missing or unclear information in responses.
* Generate targeted follow-up questions to gather additional details.
* Organise behavioural evidence into structured assessment reports.
* Support HR professionals in identifying potential development areas and training needs.

## Problem Overview

Traditional competency assessments can involve subjective interpretation, inconsistent questioning, and difficulties in organising qualitative responses.

WorkInsight AI explores how AI can assist this process by structuring employee responses, highlighting relevant evidence, and identifying areas that require further clarification.

The platform is intended to support human evaluators rather than replace human judgement.

## Key Features

* **Competency-Based Analysis:** Analyses responses against predefined criteria for selected workplace competencies.
* **Evidence-Oriented Insights:** Identifies relevant information explicitly stated in employee responses.
* **Missing Information Detection:** Highlights details that are absent or insufficiently explained.
* **Adaptive Follow-Up:** Generates targeted questions to gather additional information when supported by the implemented workflow.
* **Structured Assessment Output:** Organises findings into a format that is easier for evaluators to review.
* **Local LLM Execution:** Uses Ollama to run Llama 3.2 locally, avoiding paid per-request hosted LLM inference for the core model.

## Competencies Covered

The platform focuses on four workplace competencies.

| Competency          | Assessment Focus                                               |
| ------------------- | -------------------------------------------------------------- |
| Teamwork            | Collaboration, individual contribution, and shared outcomes    |
| Communication       | Communication approach, audience understanding, and outcomes   |
| Problem-Solving     | Problem identification, reasoning, solutions, and outcomes     |
| Conflict Resolution | Conflict context, resolution approach, reasoning, and outcomes |

These criteria provide a structured basis for analysing responses. They are not presented as a validated psychological or employment assessment framework.

## System Workflow

1. **Competency Selection:** The user selects the workplace competency to assess.
2. **Response Input:** An employee response describing an experience or workplace scenario is provided.
3. **AI-Powered Analysis:** The language model analyses the response against predefined criteria.
4. **Evidence Identification:** Relevant information explicitly present in the response is identified.
5. **Information Sufficiency Assessment:** Missing, incomplete, or unclear details are highlighted.
6. **Follow-Up Generation:** Targeted questions can be generated to gather additional information.
7. **Assessment Output:** Structured findings are presented for human review.

The system analyses the information provided by the employee. Its output does not independently establish the truthfulness of a response or prove a person's actual competency.

## Technology Stack

| Technology | Purpose                                            |
| ---------- | -------------------------------------------------- |
| Python     | Backend logic and workflow orchestration           |
| Streamlit  | Interactive user interface                         |
| Llama 3.2  | Language model used for response analysis          |
| Ollama     | Local execution of the language model              |
| Requests   | HTTP communication between Python and Ollama       |
| JSON       | Structured data exchange and model output handling |
|            |                                                    |

## System Architecture

```text
             Employee / Evaluator
                      |
                      v
              Streamlit Interface
                      |
                      v
                Python Backend
                      |
                      v
             Assessment Workflow
                      |
                      v
             Llama 3.2 via Ollama
                      |
                      v
              Response Analysis
                      |
                      v
           Evidence and Missing Details
                      |
                      v
          Follow-Up / Assessment Output
                      |
                      v
                 Human Review
```

The Streamlit interface collects user input and calls the Python backend. The backend coordinates the assessment workflow and communicates with the locally running language model through Ollama. The generated output is returned to the interface for presentation.

## Example Use Case

**Selected Competency:** Problem-Solving

**Employee Response:**

> I encountered an error while developing a web application. I examined the logs, identified a missing input validation check, implemented the fix, and tested the application with different inputs.

**Potential Assessment Output:**

* **Problem:** An error occurred during application development.
* **Analysis:** The employee examined the logs.
* **Action:** A missing input validation check was implemented.
* **Outcome:** The application was tested with different inputs.
* **Review:** A human evaluator can determine whether the available information is sufficient or requires further clarification.

This example illustrates how a response can be organised into relevant evidence. It does not establish that the employee possesses a particular level of competency.

## Getting Started

### Prerequisites

* Python
* Ollama
* Llama 3.2
* Git
* A terminal or code editor

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd WorkInsight-AI
```

Replace `<your-repository-url>` with the actual GitHub repository URL.

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

If the repository contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Otherwise, install the dependencies specified by the implementation.

### 4. Set Up Ollama

Ensure Ollama is installed and running. Download the required model if it is not already available:

```bash
ollama pull llama3.2
```

### 5. Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, typically:

```text
http://localhost:8501
```

These instructions assume the repository contains `app.py` and the required application modules.

## Limitations

* Language models can misinterpret responses or generate unsupported conclusions.
* Written responses cannot independently establish an employee's actual abilities or the truthfulness of their claims.
* Missing information should not automatically be interpreted as a lack of competency.
* Output quality depends on the response, model behaviour, and assessment criteria.
* The proposed criteria require appropriate validation before use in consequential employment decisions.
* Human review remains essential, particularly for recruitment, promotion, performance evaluation, and training decisions.

WorkInsight AI is a prototype for AI-assisted assessment, not a replacement for professional HR judgement.

## Future Enhancements

* Develop a labelled evaluation dataset for competency-related responses.
* Evaluate evidence extraction and missing-information detection against human-reviewed examples.
* Improve the consistency and relevance of generated follow-up questions.
* Introduce explainability features that link findings to specific portions of employee responses.
* Add assessment history and reporting with appropriate privacy controls.
* Evaluate the system with HR professionals and representative workplace scenarios.
* Explore structured recommendations for training and employee development.
* Investigate bias, reliability, privacy, and fairness before real-world deployment.

## Learning Outcomes

This project explores the practical application of:

* Large Language Models (LLMs)
* Prompt engineering
* Natural Language Processing (NLP)
* AI-assisted decision support
* Python application development
* Human-in-the-loop system design
* Structured evidence analysis

## Project Information

**Project Name:** WorkInsight AI
**Event:** Nexathon 2026
**Institution:** Shree Devi Institute of Technology, Mangaluru, Karnataka
**Team:** Clutch Crew
**Domain:** Artificial Intelligence, Human Resources Technology, and Decision Support
**Status:** Hackathon Prototype

## Acknowledgement

We thank the organisers of Nexathon 2026 at Shree Devi Institute of Technology, Mangaluru, for providing the problem statement and the opportunity to explore an AI-assisted approach to workplace competency assessment.
