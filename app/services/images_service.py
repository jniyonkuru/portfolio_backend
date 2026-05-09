from sqlalchemy.sql.coercions import expect

from app.utils.cloudinary_utils import CloudinaryProvider
from fastapi import Depends


class ImagesService:
    def __init__(self,cloudinary_provider=Depends(CloudinaryProvider)) -> None:
        self.cloudinary_provider=cloudinary_provider

    def upload_image(self,image):

            result= self.cloudinary_provider.upload_image(image)
            return {
           "url": result['url'],
           "public_id": result['public_id'],}


