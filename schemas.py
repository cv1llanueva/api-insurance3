from pydantic import BaseModel
from datetime import date

class Claim(BaseModel):
    claim_number: str
    policy_number: str
    description: str
    amount: float
    insured_person: str
    date_of_incident: date
    incident_location: str
    date_filed: date
    claim_status: str
    adjuster_notes: str  = None
