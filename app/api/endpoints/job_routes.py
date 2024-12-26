from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlmodel import Session
import pandas as pd
import io

from core.database import get_session
from models.job import Job
from services.job_service import JobService
from core.exceptions import ResourceNotFoundError, DatabaseOperationError



router = APIRouter(prefix='/jobs', tags=['jobs'])


@router.post('/', response_model=Job)
def create_job(job: Job, session: Session = Depends(get_session)):
    """
    Create a new job.

    Parameters
    ----------
    job : Job
        Job details to be created
    session : Session
        Database session dependency

    Returns
    -------
    Job
        Created job with assigned ID
    """
    try:
        job_service = JobService(session)
        return job_service.create(job)
    except DatabaseOperationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{job_id}', response_model=Job)
def get_job(job_id: int, session: Session = Depends(get_session)):
    """
    Retrieve a job by its ID.

    Parameters
    ----------
    job_id : int
        Unique identifier of the job
    session : Session
        Database session dependency

    Returns
    -------
    Job
        Job details
    """
    try:
        job_service = JobService(session)
        return job_service.get_by_id(job_id)
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/', response_model=list[Job])
def list_jobs(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    """
    List all jobs with optional pagination.

    Parameters
    ----------
    offset : int, optional
        Number of records to skip, by default 0
    limit : int, optional
        Maximum number of records to return, by default 100
    session : Session
        Database session dependency

    Returns
    -------
    list[Job]
        List of jobs
    """
    job_service = JobService(session)
    return job_service.get_all(offset, limit)


@router.put('/{job_id}', response_model=Job)
def update_job(job_id: int, job_update: Job, session: Session = Depends(get_session)):
    """
    Update an existing job.

    Parameters
    ----------
    job_id : int
        Unique identifier of the job to update
    job_update : Job
        Updated job details
    session : Session
        Database session dependency

    Returns
    -------
    Job
        Updated job details
    """
    try:
        job_service = JobService(session)
        return job_service.update(job_id, job_update)
    except (ResourceNotFoundError, DatabaseOperationError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{job_id}', status_code=204)
def delete_job(job_id: int, session: Session = Depends(get_session)):
    """
    Delete a job by its ID.

    Parameters
    ----------
    job_id : int
        Unique identifier of the job to delete
    session : Session
        Database session dependency
    """
    try:
        job_service = JobService(session)
        job_service.delete(job_id)
    except (ResourceNotFoundError, DatabaseOperationError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/csv')
async def upload_job_csv(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
) -> dict[str, str]:
    """
    Upload a CSV file containing job data.

    Parameters:
    -----------
    file : UploadFile
        The CSV file to be uploaded
    session : Session
        Database session dependency

    Returns:
    --------
    dict
        A dictionary with upload status and details
    """
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents), names=['id', 'job'])

        job_service = JobService(session)

        successful_imports = 0
        failed_imports = 0

        for _, row in df.iterrows():
            try:
                job = Job(id=row['id'], job=row['job'])
                job_service.create(job)
                successful_imports += 1
            except Exception:
                failed_imports += 1

        session.commit()

        return {
            'status': 'success',
            'successful_imports': str(successful_imports),
            'failed_imports': str(failed_imports),
        }

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))