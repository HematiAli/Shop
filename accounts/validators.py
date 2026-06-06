import uuid
from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from django.core.files.base import ContentFile


MAX_FILE_SIZE = 2 * 1024 * 1024 # 2MB
ALLOWED_FORMATS = ['JPG', 'JPEG','PNG', 'WEBP']

def avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1].upper()
    if ext not in ALLOWED_FORMATS:
        ext = 'jpg'
    
    return f"avatars/{uuid.uuid4()}.{ext}"
 

def validate_avatar(file):
    if file.size > MAX_FILE_SIZE:
        raise ValidationError('file size must be under 2MB')
    
    try:
        img = Image.open(file)
        img.verify()
    except (OSError, UnidentifiedImageError):
        raise ValidationError("invalid image file.")
    finally:
        file.seek(0)

    img = Image.open(file)
    if img.format not in ALLOWED_FORMATS:
        raise ValidationError("Only JPG, JPEG, WEBP, PNG, allowed")
    
    width, height = img.size
    if width > 1000 or height > 1000:
        raise ValidationError("image dimensions too large")

    file.seek(0) #دوباره فایل رو باز میکنم تا باهاش کار کنم

def process_image(file):
    try:
        img = Image.open(file)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        img.thumbnail((512,512))
        output = BytesIO() #save on RAM
        img.save(output, format='JPEG', quality=85, optimze=True)
        output.seek(0)
        filename = f"{uuid.uuid4()}.jpg"
        return ContentFile(output.read(), name=filename)
    except Exception:
        raise ValidationError('Failed to process image')
