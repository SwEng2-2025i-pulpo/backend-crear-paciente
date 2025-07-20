from fastapi import APIRouter, HTTPException, Depends, Body
from app.db.client import db_client
from bson import ObjectId
from datetime import datetime
from bson import ObjectId, errors as bson_errors
from app.db.schemas.patient import *
from app.db.Models.patient import PatientCreate, Patient_Update
from datetime import datetime, date
from app.security.auth import get_current_user

router = APIRouter(prefix="/create-patient", tags=["create-patient"])

#POST PACIENTE FUNCIONANDO
@router.post("/", response_model=PatientCreate, summary="Crear un nuevo paciente", response_description="Paciente creado")
async def create_patient(
    patient_data: PatientCreate,
    current_user: dict = Depends(get_current_user)  # cuidador autenticado desde JWT
):
    # Verificar duplicado por documento
    duplicated = search_duplicated(patient_data.document)
    if isinstance(duplicated, PatientCreate):
        raise HTTPException(status_code=409, detail="El documento ya existe")

    # Convertimos modelo a dict y eliminamos el campo 'id'
    patient_dict = dict(patient_data)
    patient_dict.pop("id", None)

    # Convertir birth_date de date a datetime (con hora mínima)
    if isinstance(patient_dict.get("birth_date"), date):
        patient_dict["birth_date"] = datetime.combine(patient_dict["birth_date"], datetime.min.time())

    # Procesar caretakers_ids: convertir strings a ObjectId si ya vienen
    caretakers_ids = patient_dict.get("caretakers_ids", [])
    patient_dict["caretakers_ids"] = [ObjectId(cid) for cid in caretakers_ids if cid]

    # Agregar el cuidador actual si no está
    current_caretaker_id = ObjectId(current_user["id"])
    if current_caretaker_id not in patient_dict["caretakers_ids"]:
        patient_dict["caretakers_ids"].append(current_caretaker_id)

    # Insertar paciente en la base de datos
    inserted_id = db_client.conectacare.patient.insert_one(patient_dict).inserted_id
    new_patient = db_client.conectacare.patient.find_one({"_id": inserted_id})

    return PatientCreate(**patient_schema(new_patient))


def search_duplicated(document: int):
    patient_found = db_client.conectacare.patient.find_one({"document": document})
    if patient_found:
        return PatientCreate(**patient_schema(patient_found))
    return None

#PUT PACIENTE FUNCIONANDO
@router.put("/{patient_id}/edit_patient", response_model=PatientCreate, summary="Editar un paciente", response_description="Paciente actualizado")
async def editpatient(patient_id: str, patient_update:Patient_Update):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = db_client.conectacare.patient.find_one({"_id": object_id})

    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    patient_update_dict = patient_update.dict()
    patient_update_dict["_id"] = object_id

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
        return Patient_Update(**patient_schema(updated_patient))

    raise HTTPException(status_code=304, detail="No se realizaron cambios en el paciente")


#GET PATIENTS FUNCIONANDO
@router.get("/", summary="Obtener lista de pacientes", response_description="Lista de pacientes")
async def get_patients(current_user: dict = Depends(get_current_user)):
    caretaker_id = current_user["id"]
    caretaker_id_object = ObjectId(caretaker_id)

    # Buscamos pacientes cuyo caretakers_ids contenga el ID del cuidador
    patients_cursor = db_client.conectacare.patient.find({
        "caretakers_ids": caretaker_id_object 
    })

    patients = patient_schema_starting_list(patients_cursor)
    return patients