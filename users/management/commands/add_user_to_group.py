# สร้างไฟล์ users/management/commands/add_user_to_group.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User

class Command(BaseCommand):
    help = 'Add user to a group'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username')
        parser.add_argument('group', type=str, help='Group name (Admins or Regular Users)')

    def handle(self, *args, **options):
        username = options['username']
        group_name = options['group']
        
        try:
            user = User.objects.get(username=username)
            group = Group.objects.get(name=group_name)
            
            user.groups.add(group)
            
            # ถ้าเป็นกลุ่ม Admins ให้กำหนด is_staff เป็น True
            if group_name == 'Admins':
                user.is_staff = True
                user.save()
            
            self.stdout.write(self.style.SUCCESS(f'Successfully added {username} to {group_name}'))
        
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {username} does not exist'))
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Group {group_name} does not exist'))