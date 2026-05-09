import cloudinary
import cloudinary.uploader
from cloudinary import CloudinaryImage
import cloudinary.api
from dotenv import load_dotenv

load_dotenv()

class CloudinaryProvider:
    def __init__(self):
        self.client=cloudinary.uploader

    def upload_image(self, image):
        result = self.client.upload(image)
        return {
            'url': result['secure_url'],
            'public_id': result['public_id'],
        }
    def delete (self,public_id):
        self.client.destroy(public_id)




