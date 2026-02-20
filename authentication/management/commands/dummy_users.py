# authentication/management/commands/insert_dummy_users.py
import random
from django.core.management.base import BaseCommand
from authentication.models import CustomUser

class Command(BaseCommand):
    help = 'Insert 100 dummy users with hashed passwords efficiently'

    def handle(self, *args, **options):
        users = []

        for i in range(1, 101):
            username = f"dummyuser{i}"
            email = f"dummy{i}@example.com"
            phone_number = f"03{random.randint(100000000, 999999999)}"

            user = CustomUser(username=username, email=email, phone_number=phone_number)

            user.set_password("password123")

            users.append(user)

        CustomUser.objects.bulk_create(users)

        self.stdout.write(self.style.SUCCESS('✅ Successfully inserted 100 dummy users with hashed passwords!'))