from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
import pytz
from authentication.models import PSTDateTimeRecord


class Command(BaseCommand):
    help = "Insert PST datetime records"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        user, created = User.objects.get_or_create(
            username="pst_dummy_user",
            defaults={"email": "pst_user@example.com"}
        )
        if created:
            # Set a default password so user can login
            user.set_password("admin123")  # or generate a random one
            user.save()

        self.stdout.write(f"Using user: {user.username} (created: {created})")

        # 🔥 Current UTC time
        utc_now = timezone.now()
        self.stdout.write(f"Current UTC Time: {utc_now}")

        # 🔥 Convert UTC to PST manually
        pst = pytz.timezone("America/Los_Angeles")
        pst_time = utc_now.astimezone(pst)
        self.stdout.write(f"Converted PST Time (manual): {pst_time}")

        # # 🔥 Django localtime (uses TIME_ZONE from settings)
        # local_time = timezone.localtime(utc_now)
        # self.stdout.write(f"Django Local Time (from settings): {local_time}")

        records = []

        for i in range(100):
            records.append(
                PSTDateTimeRecord(
                    user=user,
                    title=f"PST Record {i+1}",
                    datetime_pst=pst_time
                )
            )

        PSTDateTimeRecord.objects.bulk_create(records)

        self.stdout.write(self.style.SUCCESS("Successfully inserted records."))