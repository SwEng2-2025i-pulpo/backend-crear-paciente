def patient_schema(patient) -> dict:
    return {
        "id": str(patient["_id"]),
        "name": patient.get("name", ""),
        "last_name": patient.get("last_name", ""),
        "birth_date": patient["birth_date"].date().isoformat() if "birth_date" in patient else "",
        "age": patient.get("age", 0),
        "document": patient.get("document", 0),
        "cholesterol": patient.get("cholesterol", 0),
        "glucose": patient.get("glucose", 0),
        "conditions": patient.get("conditions", []),
        "medications": patient.get("medications", []),
        "activity_level": patient.get("activity_level", ""),
        "caretakers_ids": [str(cid) for cid in patient.get("caretakers_ids", [])],
        "medical_history": patient.get("medical_history", []),
        "meals": patient.get("meals", []),
        "medication_logs": patient.get("medication_logs", []),
        "hygiene_logs": patient.get("hygiene_logs", []),
        "vital_signs": patient.get("vital_signs", []),
        "symptoms": patient.get("symptoms", [])
    }

def patient_schema_starting(patient) -> dict:
    return {
        "id": str(patient["_id"]),
        "name": patient.get("name", ""),
        "last_name": patient.get("last_name", ""),
        "birth_date": patient["birth_date"].date().isoformat() if "birth_date" in patient else "",
        "age": patient.get("age", 0),
        "document": patient.get("document", 0)

    }

def patient_schema_starting_list(patient) -> list:
    return [patient_schema_starting(patient) for patient in patient]
