from pydantic import BaseModel
from typing import Optional
from datetime import date
from typing import List
from app.db.Models.activity import MedicalHistoryEntry, Meal, MedicationLog, HygieneLog, VitalSigns, Symptom



class PatientCreate(BaseModel):
    
    id: Optional[str] = None
    name: str                      
    last_name: str                 
    birth_date: date
    age: int
    document: int
    cholesterol: Optional[int] = None
    glucose: Optional[int] = None
    conditions: List[str] = []
    medications: List[str] = []
    activity_level: Optional[str] = None
    caretakers_ids: List[str] = []            
    medical_history: List[MedicalHistoryEntry] = []
    meals: List[Meal] = []
    medication_logs: List[MedicationLog] = []
    hygiene_logs: List[HygieneLog] = []
    vital_signs: List[VitalSigns] = []
    symptoms: List[Symptom] = []

class Patient_Update(BaseModel):
    name: str
    last_name: str
    birth_date: date
    age: int
    document: int
