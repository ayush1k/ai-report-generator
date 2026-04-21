# AI Report Generator

This project generates a Detailed Diagnostic Report (DDR) by combining:

- A general property inspection PDF (text-heavy)
- A thermal inspection PDF (image-heavy)

The pipeline extracts structured observations from both sources, merges them, and writes a client-ready Markdown report.

## How It Works

1. Extract text from the general report PDF.
2. Convert thermal PDF pages to images.
3. Run two structured extraction calls against Gemini.
4. Synthesize both extracted datasets into one final DDR JSON object.
5. Render that final object into Markdown.

The process uses Pydantic schemas to keep outputs consistent and reduce free-form model drift.

## Tech Stack

- Python 3.10+
- Google GenAI SDK (`gemini-2.5-flash`)
- Pydantic
- PyMuPDF (`fitz`)
- Pillow
- python-dotenv

## Repository Structure

- `main.py` - End-to-end pipeline (extract, synthesize, render)
- `schemas.py` - Pydantic schema definitions for intermediate and final outputs
- `sample_general_report.pdf` - Sample general inspection input
- `sample_thermal_report.pdf` - Sample thermal inspection input
- `README.md` - Project documentation

## Setup

### 1) Create and activate a virtual environment

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```bash
pip install google-genai pydantic pymupdf pillow python-dotenv
```

### 3) Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

## Run

```bash
python main.py
```

On success, the script writes:

- `Final_Client_Report.md`

## Output Format

The generated report contains:

1. Property issue summary
2. Area-wise observations
3. Probable root cause
4. Severity assessment
5. Recommended actions
6. Additional notes
7. Missing or unclear information

## Notes and Assumptions

- Input file names are currently hardcoded in `main.py` as:
	- `sample_general_report.pdf`
	- `sample_thermal_report.pdf`
- If these files are renamed or moved, update `main.py` accordingly.
- The script requires a valid Gemini API key at runtime.
