# สร้างไฟล์ users/management/commands/setup_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from reviews.models import Movie, Review
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Setup user groups and permissions'

    def handle(self, *args, **options):
        # สร้างกลุ่ม Admins
        admin_group, created = Group.objects.get_or_create(name='Admins')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Admins group'))
        
        # สร้างกลุ่ม Regular Users
        user_group, created = Group.objects.get_or_create(name='Regular Users')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Regular Users group'))
        
        # กำหนดสิทธิ์สำหรับ Admins (ทุกอย่าง)
        movie_content_type = ContentType.objects.get_for_model(Movie)
        review_content_type = ContentType.objects.get_for_model(Review)
        user_content_type = ContentType.objects.get_for_model(User)
        
        # สิทธิ์สำหรับ Movie
        movie_permissions = Permission.objects.filter(content_type=movie_content_type)
        admin_group.permissions.add(*movie_permissions)
        
        # สิทธิ์สำหรับ Review
        review_permissions = Permission.objects.filter(content_type=review_content_type)
        admin_group.permissions.add(*review_permissions)
        
        # สิทธิ์สำหรับ User
        user_permissions = Permission.objects.filter(content_type=user_content_type)
        admin_group.permissions.add(*user_permissions)
        
        # กำหนดสิทธิ์สำหรับ Regular Users (จำกัด)
        # สิทธิ์ในการดู Movie
        view_movie = Permission.objects.get(codename='view_movie', content_type=movie_content_type)
        user_group.permissions.add(view_movie)
        
        # สิทธิ์ในการดู, เพิ่ม, แก้ไข, ลบ Review ของตัวเอง
        view_review = Permission.objects.get(codename='view_review', content_type=review_content_type)
        add_review = Permission.objects.get(codename='add_review', content_type=review_content_type)
        change_review = Permission.objects.get(codename='change_review', content_type=review_content_type)
        delete_review = Permission.objects.get(codename='delete_review', content_type=review_content_type)
        
        user_group.permissions.add(view_review, add_review, change_review, delete_review)
        
        self.stdout.write(self.style.SUCCESS('Successfully set up permissions'))