import os
import fitz  # PyMuPDF
from PIL import Image
from dotenv import load_dotenv
from google import genai

# Import your custom schemas
from schemas import DocumentExtraction, FinalDDR

# Load the variables from the .env file into the system environment
load_dotenv()

# Initialize the GenAI client (it automatically picks up GEMINI_API_KEY from the environment)
client = genai.Client() 
MODEL_ID = 'gemini-2.5-flash'

def extract_text_from_pdf(pdf_path: str) -> str:
    """Helper function to extract raw text from a PDF document."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_general_report(text_content: str) -> DocumentExtraction:
    """Extracts structured observations from the text report."""
    prompt = "Extract all property observations from this inspection report. Do not invent details."
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[prompt, text_content],
        config={
            'response_mime_type': 'application/json',
            'response_schema': DocumentExtraction,
            'temperature': 0.1 
        }
    )
    return response.parsed

def extract_thermal_report(pdf_path: str) -> DocumentExtraction:
    """Converts PDF pages to images and extracts thermal anomalies."""
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
        
    prompt = "Analyze these thermal images and any associated text. Extract all temperature anomalies as observations."
    
    # Pass the prompt and the list of PIL images directly to the multimodal model
    contents = [prompt] + images 
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=contents,
        config={
            'response_mime_type': 'application/json',
            'response_schema': DocumentExtraction,
            'temperature': 0.1
        }
    )
    return response.parsed

def synthesize_final_report(general_data: DocumentExtraction, thermal_data: DocumentExtraction) -> FinalDDR:
    """Merges the two structured datasets into the final DDR format."""
    
    general_json = general_data.model_dump_json()
    thermal_json = thermal_data.model_dump_json()
    
    prompt = f"""
    You are an expert Property Diagnostic Analyst. Merge the following two inspection datasets into a single Detailed Diagnostic Report (DDR).
    
    General Inspection Data:
    {general_json}
    
    Thermal Inspection Data:
    {thermal_json}
    
    STRICT RULES:
    1. Combine observations for the same 'area'. Do not duplicate points.
    2. If visual data contradicts thermal data, explicitly note this in 'conflict_notes'.
    3. DO NOT invent root causes. If not explicitly stated, output 'Not Available' for 'probable_root_cause'.
    4. Use simple, client-friendly language. Remove technical jargon.
    """
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': FinalDDR,
            'temperature': 0.2
        }
    )
    return response.parsed

def generate_markdown_report(report_data: FinalDDR) -> str:
    """Converts the structured JSON into a client-ready Markdown document."""
    
    md = "# Detailed Diagnostic Report (DDR)\n\n"
    
    md += "## 1. Property Issue Summary\n"
    md += f"{report_data.property_issue_summary}\n\n"
    
    md += "## 2. Area-wise Observations\n"
    for obs in report_data.area_wise_observations:
        md += f"**{obs.area}**\n"
        md += f"- **Observation:** {obs.combined_issue}\n"
        if obs.conflict_notes and obs.conflict_notes.lower() != "not available":
            md += f"- **Note:** {obs.conflict_notes}\n"
        md += "\n"
        
    md += "## 3. Probable Root Cause\n"
    md += f"{report_data.probable_root_cause}\n\n"
    
    md += "## 4. Severity Assessment\n"
    md += f"{report_data.severity_assessment}\n\n"
    
    md += "## 5. Recommended Actions\n"
    for action in report_data.recommended_actions:
        md += f"- {action}\n"
    md += "\n"
    
    md += "## 6. Additional Notes\n"
    md += f"{report_data.additional_notes}\n\n"
    
    md += "## 7. Missing or Unclear Information\n"
    for missing in report_data.missing_unclear_information:
        md += f"- {missing}\n"
        
    return md

def main():
    # Ensure these file names match the PDFs in your directory exactly
    general_pdf_path = "sample_general_report.pdf" 
    thermal_pdf_path = "sample_thermal_report.pdf"
    
    print("1. Extracting text from General Report PDF...")
    general_text = extract_text_from_pdf(general_pdf_path)
    
    print("2. Structuring General Data via AI...")
    general_data = extract_general_report(general_text)
    
    print("3. Extracting Thermal Data directly from PDF images...")
    thermal_data = extract_thermal_report(thermal_pdf_path)
    
    print("4. Synthesizing Final DDR...")
    final_report = synthesize_final_report(general_data, thermal_data)
    
    print("\n5. Generating Client-Ready Markdown Report...")
    markdown_output = generate_markdown_report(final_report)
    
    # Save to a file for your submission
    output_filename = "Final_Client_Report.md"
    with open(output_filename, "w") as f:
        f.write(markdown_output)
        
    print(f"\n✅ Success! Report saved as '{output_filename}' in your current directory.")

if __name__ == "__main__":
    main()