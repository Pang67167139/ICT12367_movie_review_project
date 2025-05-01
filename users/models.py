from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)  # เปลี่ยนจาก default='default.jpg'
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # ตรวจสอบว่ามีรูปภาพหรือไม่ก่อนที่จะปรับขนาด
        if self.image and hasattr(self.image, 'path') and os.path.exists(self.image.path):
            try:
                img = Image.open(self.image.path)
                
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
            except Exception as e:
                print(f"Error processing image: {e}")
    
    # เพิ่มเมธอดนี้เพื่อให้สามารถเข้าถึง URL ของรูปภาพได้แม้ไม่มีไฟล์
    def get_image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            # ส่งคืน URL ของรูปภาพเริ่มต้น
            return '/static/users/default.jpg'  # ต้องมีไฟล์นี้ในโฟลเดอร์ static