Applied AI Builder: Automated DDR Generation Pipeline

Project Overview

This repository contains a production-ready AI workflow designed to automate the generation of Detailed Diagnostic Reports (DDR). It processes raw, unstructured property inspection data (PDF text) and thermal imaging reports (PDF images), logically merges the findings, and outputs a client-ready, strictly formatted Markdown document.

Objective: To demonstrate enterprise-grade LLM control, deterministic data extraction, and reliable conflict resolution without hallucinations.

System Architecture

To ensure 100% adherence to the requested DDR structure and eliminate LLM hallucinations, this system abandons the "single massive prompt" approach in favor of a Decompose, Extract, and Synthesize pipeline.

Independent Extraction (Parallel):

The General Report is parsed using PyMuPDF and processed by Gemini 2.5 Flash to extract textual observations.

The Thermal Report is converted into raw images and passed through Gemini 2.5 Flash's multimodal vision capabilities to extract thermal anomalies.

Schema Enforcement (schemas.py): Both extraction streams are forced into a rigid Pydantic JSON schema. This ensures the LLM grounds its output as structured data rather than free-flowing text.

The Synthesizer: A secondary LLM call receives both structured JSON objects. Its sole job is to cross-reference areas, merge duplicates, flag conflicting data, and explicitly output "Not Available" for missing facts (e.g., probable root cause).

Formatting: The finalized JSON is mapped directly into a clean, client-facing Markdown report.

Tech Stack

Language: Python 3.10+

LLM Provider: Google GenAI SDK (gemini-2.5-flash for high-speed, multimodal reasoning)

Data Validation: pydantic (for strict schema enforcement)

Document Processing: PyMuPDF (fitz) and Pillow (PIL)

Environment: python-dotenv for secure API key management

Repository Structure

main.py: The core execution engine and LLM pipeline logic.

schemas.py: The Pydantic classes defining the strict intermediate and final data structures.

sample_general_report.pdf: Input file 1 (Text-based inspection data).

sample_thermal_report.pdf: Input file 2 (Image-based thermal data).

Final_Client_Report.md: The generated output file.

Key Design Decisions

Zero Hallucination Guarantee: By separating the extraction from the synthesis, and using low-temperature settings (0.1) with Pydantic schemas, the system is mathematically constrained from inventing unprovided data.

Honest Conflict Resolution: If the visual text and thermal images contradict, or if data is missing, the synthesizer is explicitly programmed to state "Not Available" or explain the discrepancy.

Modular Codebase: The PDF extraction functions are decoupled from the AI logic, allowing easy future integration with Word docs, APIs, or database streams.

Step-by-Step Execution Guide

Follow these steps to run the DDR Generation Pipeline locally.

Step 1: Clone the Repository

Ensure you have all the necessary files in a single working directory:

main.py

schemas.py

sample_general_report.pdf

sample_thermal_report.pdf

Step 2: Set Up the Environment

It is recommended to use a virtual environment. Open your terminal and run:

# Create a virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate


Step 3: Install Dependencies

Install the required Python packages for the GenAI SDK, PDF processing, and environment management:

pip install google-genai pydantic pymupdf pillow python-dotenv


Step 4: Configure the API Key

Create a new file in the root of your project directory named exactly .env.

Open the .env file and paste your Gemini API key inside like this (no quotes or spaces around the equals sign):

GEMINI_API_KEY=your_actual_api_key_here


Step 5: Execute the Pipeline

Run the main Python script from your terminal:

python main.py


Step 6: Review the Output

The terminal will display the execution steps. Once completed, you will see a success message:
Success! Report saved as 'Final_Client_Report.md'

Open the newly generated Final_Client_Report.md file in your directory to view the final, structured output.