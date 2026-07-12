print("******** MANUFACTURING JOB LOADED ********")

from pydantic import BaseModel
from typing import Optional


class ManufacturingJob(BaseModel):

    job_id: Optional[str] = None
    date_created: Optional[str] = None

    part_name: str
    material: str
    quantity: int
    machine: str
    deadline: str

    assigned_to: str = "-"
    assigned_email: str = "-"
    status: str = "Planned"
    estimated_time: str = "-"
    remarks: str = "-"


print("FIELDS =", ManufacturingJob.model_fields.keys())