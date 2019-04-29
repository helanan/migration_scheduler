import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Migration

# Create your tests here.


class MigrationModelTests(TestCase):

    def test_was_published_recently_with_future_migration(self):
        """
        was_published_recently() returns False for migrations whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_migration = Migration(pub_date=time)
        self.assertIs(future_migration.was_published_recently(), False)

    def test_was_published_recently_with_old_migration(self):
        """
        was_published_recently() returns False for migrations whose pub_date is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_migration = Migration(pub_date=time)
        self.assertIs(old_migration.was_published_recently(), False)

    def test_was_published_recently_with_recent_migration(self):
        """
        was_published_recently() returns True for migrations whose pub_date is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_migration = Migration(pub_date=time)
        self.assertIs(recent_migration.was_published_recently(), True)


def create_migration(migration_text, days):
    """
    Create a migration with the given "migration_text" and published the given number of `days` offset to now (negative for migrations published in the past, positive for migrations that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Migration.objects.create(migration_text=migration_text, pub_date=time)


class MigrationIndexViewTests(TestCase):
    def test_no_migrations(self):
        """
        If no migrations exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('dicalendar:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No migrations are available.")
        self.assertQuerysetEqual(response.context['latest_migration_list'], [])

    def test_past_migration(self):
        """
        Migrations with a pub_date in the past are displayed on the index page.
        """
        create_migration(migration_text="Past migration.", days=-30)
        response = self.client.get(reverse('dicalendar:index'))
        self.assertQuerysetEqual(
            respoonse.context['latest_migration_list'],
            ['<Migration: Past migration.>']
        )

    def test_future_migration(self):
        """
        Migrations with a pub_date in the future arent displayed on the index page.
        """
        create_migration(migration_text="Future migration.", days=30)
        response = self.client.get(reverse('dicalendar:index'))
        self.assertContains(response, "No calendars are available.")
        self.assertQuerysetEqual(response.context['latest_migration_list'], [])

    def test_future_migration_and_past_migration(self):
        """
        Even if both past and future migrations exist, only past migrations are displayed.
        """
        create_migration(migration_text="Past migration.", days=-30)
        create_migration(migration_text="Future migration.", days=30)
        response = self.client.get(reverse('dicalendar:index'))
        self.assertQuerysetEqual(
            response.context['latest_migration_list'], [
                'Migration: Past migration.']
        )
