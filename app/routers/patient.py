from fastapi import APIRouter, HTTPException, Body
from app.db.client import db_client
from bson import ObjectId
from datetime import datetime
from bson import ObjectId, errors as bson_errors
from app.db.schemas.patient import *
from app.db.Models.patient import PatientCreate
from datetime import datetime, date

router = APIRouter(prefix="/create-patient", tags=["create-patient"])


#POST PACIENTE FUNCIONANDO
@router.post("/", response_model = PatientCreate, summary="Crear un nuevo paciente", response_description="Paciente creado")

async def create_patient(patient_data: PatientCreate):

    duplicated = search_duplicated(patient_data.document)
    if isinstance(duplicated, PatientCreate):
        raise HTTPException(status_code=409, detail="El documento ya existe")

    patient_dict = dict(patient_data)
    del patient_dict["id"]

    # Convertir birth_date de date a datetime
    if isinstance(patient_dict["birth_date"], date):
        patient_dict["birth_date"] = datetime.combine(patient_dict["birth_date"], datetime.min.time())

     # Convertimos caretakers_ids de str a ObjectId si existe
    if "caretakers_ids" in patient_dict:
        patient_dict["caretakers_ids"] = [ObjectId(cid) for cid in patient_dict["caretakers_ids"]]

    ide = db_client.conectacare.patient.insert_one(patient_dict).inserted_id
    new_patient = patient_schema(db_client.conectacare.patient.find_one({"_id": ide}))
    return PatientCreate(**new_patient)


def search_duplicated(document: int):
    patient_found = db_client.conectacare.patient.find_one({"document": document})
    if patient_found:
        return PatientCreate(**patient_schema(patient_found))
    return None

#PUT PACIENTE FUNCIONANDO
@router.put("/{patient_id}/edit_patient", response_model=PatientCreate, summary="Editar un paciente", response_description="Paciente actualizado")
async def editpatient(patient_id: str, patient_update:PatientCreate):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = db_client.conectacare.patient.find_one({"_id": object_id})

    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    patient_update_dict = patient_update.dict()
    patient_update_dict["id"] = object_id

    if isinstance(patient_update_dict["birth_date"], date):
        patient_update_dict["birth_date"] = datetime.combine(patient_update_dict["birth_date"], datetime.min.time())

    
    result = db_client.conectacare.patient.update_one(
        {"_id": object_id},
        {"$set": patient_update_dict}
    )
    if result.modified_count == 1:
        updated_patient = db_client.conectacare.patient.find_one({"_id": object_id})
        if updated_patient is None:
            raise HTTPException(status_code=400, detail="Error interno: paciente actualizado no encontrado")
        return PatientCreate(**patient_schema(updated_patient))

    raise HTTPException(status_code=304, detail="No se realizaron cambios en el paciente")


#GET PATIENTS FUNCIONANDO
@router.get("/", summary="Obtener lista de pacientes", response_description="Lista de pacientes")
async def get_patients():

    patients = patient_schema_starting_list(db_client.conectacare.patient.find())
    return patients
