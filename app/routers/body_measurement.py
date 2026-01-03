from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from  .. import schemas,models
from typing import List


router = APIRouter(
    prefix='/bodymeasurements',
    tags=['BodyMeasurements']
)

@router.get('/',status_code=status.HTTP_200_OK,response_model=List[schemas.BodyMeasurementResponse])
def get_measurements(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    measurements = db.query(models.BodyMeasurement).all()
    return measurements



@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.BodyMeasurementResponse)
def get_measurement(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_measurement = db.query(models.BodyMeasurement).filter(models.BodyMeasurement.id == id).first()
    if db_measurement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'body measurement with id {id} not found')
    return db_measurement



@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.BodyMeasurementResponse)
def create_measurement(body_measurement:schemas.BodyMeasurementBase,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    measurement_db = models.BodyMeasurement(**body_measurement.dict())
    db.add(measurement_db)
    db.commit()
    db.refresh(measurement_db)
    return measurement_db



@router.patch('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.BodyMeasurementResponse)
def update_measurement(id:int,measurements:schemas.BodyMeasurementUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_measurement = db.query(models.BodyMeasurement).filter(models.BodyMeasurement.id == id)
    existing_db = db_measurement.first()
    if existing_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'body measuremt with id {id} not found')
    db_measurement.update(measurements.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    updated_measurement = db_measurement.first()
    return updated_measurement



@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.BodyMeasurementResponse)
def update_measurement(id:int,body_measurement:schemas.BodyMeasurementBase,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_measurement = db.query(models.BodyMeasurement).filter(models.BodyMeasurement.id == id)
    existing_db = db_measurement.first()
    if existing_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'body measurement with id {id} not found')
    db_measurement.update(body_measurement.dict(),synchronize_session=False)
    db.commit()
    updated_db = db_measurement.first()
    return updated_db


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_measurement(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_measurement = db.query(models.BodyMeasurement).filter(models.BodyMeasurement.id == id).first()
    if db_measurement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'body measurement with id {id} not found')
    db.delete(db_measurement)
    db.commit()
    return {'message':'successfully deleted the body measurement'}