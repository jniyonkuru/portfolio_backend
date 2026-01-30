
from app.repositories.base_repository import ExperienceRepository
from fastapi import Depends,HTTPException,status
from app.dependencies import create_experience_repo
from app.schemas.schemas import ExperienceCreate
from app.models.models import Experience


def create_experience_service(experience:ExperienceCreate,experience_repo:ExperienceRepository):
        experience_exists=experience_repo.get_by_attributes({"role":experience.role,"organization":experience.organization})
        if experience_exists:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Experience as{experience.role} , at {experience.organization} already exists.")
        db_experience=Experience(**experience.model_dump())
        return experience_repo.create(db_experience)