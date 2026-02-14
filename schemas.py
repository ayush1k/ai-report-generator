from pydantic import BaseModel, Field
from typing import List

# --- Intermediate Extraction Schemas ---
class Observation(BaseModel):
    area: str = Field(description="The physical location, e.g., 'Master Bedroom'")
    issue_description: str = Field(description="What is wrong in this area")
    severity: str = Field(description="Low, Medium, or High")

class DocumentExtraction(BaseModel):
    observations: List[Observation]

# --- Final Output Schemas ---
class MergedObservation(BaseModel):
    area: str
    combined_issue: str
    conflict_notes: str = Field(description="Mention 'Not Available' or note any conflicts between reports here.")

class FinalDDR(BaseModel):
    property_issue_summary: str = Field(description="A 2-3 sentence executive summary.")
    area_wise_observations: List[MergedObservation]
    probable_root_cause: str = Field(description="Must be 'Not Available' if not explicitly stated in the source documents.")
    # Updated to require reasoning per the assignment prompt
    severity_assessment: str = Field(description="State the severity (Low, Medium, High) AND provide a 1-sentence reasoning based on the findings.")
    recommended_actions: List[str]
    additional_notes: str
    missing_unclear_information: List[str]