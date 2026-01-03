from fastapi import APIRouter,HTTPException,status,Depends,Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from  .. import schemas,models
from typing import List
import math
from sqlalchemy import asc,desc

router = APIRouter(
    prefix='/bodymeasurements',
    tags=['BodyMeasurements']
)

@router.get('/',status_code=status.HTTP_200_OK,response_model=schemas.PaginatedBodyMeasuresResponse)
def get_measurements(db:Session=Depends(get_db),current_user=Depends(get_current_user),limit:int=Query(10,ge=1,le=10),page:int=Query(1,ge=1),sort_by:str=Query('id'),order:str=Query('asc')):
    
    sort_fields = {
        'id':models.BodyMeasurement.id,
        'weight':models.BodyMeasurement.weight,
        'chest':models.BodyMeasurement.chest
    }

    total = db.query(models.BodyMeasurement).count()
    total_pages = math.ceil(total/limit)
    offset = (page-1) * limit

    sort_column = sort_fields.get(sort_by,models.BodyMeasurement.id)
    query = db.query(models.BodyMeasurement).filter(models.BodyMeasurement.owner_id == current_user.id)

    if order == 'desc':
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    measurements = query.limit(limit).offset(offset).all()
    return {
        'data':measurements,
        'total':total,
        'page':page,
        'totalPages':total_pages
    }



@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.BodyMeasurementResponse)
def get_measurement(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_measurement = db.query(models.BodyMeasurement).filter(models.BodyMeasurement.id == id,models.BodyMeasurement.owner_id == current_user.id).first()
    if db_measurement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'body measurement with id {id} not found')
    return db_measurement



@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.BodyMeasurementResponse)
def create_measurement(body_measurement:schemas.BodyMeasurementBase,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    measurement_db = models.BodyMeasurement(**body_measurement.dict(),owner_id=current_user.id)
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
    if existing_db.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Not authorized to perform the requested action')
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
    if existing_db.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Not authorized to perform the requested action')
    db_measurement.update(body_measurement.dict(),synchronize_session=False)
    db.commit()
    updated_db = db_measurement.first()
    return updated_db


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_measurement(id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    db_measurement = db.query(models.BodyMeasurement).filter(models.BodyMeasurement.id == id).first()
    if db_measurement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'body measurement with id {id} not found')
    if db_measurement.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Not authorized to perform the requested action')
    db.delete(db_measurement)
    db.commit()
    return {'message':'successfully deleted the body measurement'}