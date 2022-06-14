from django.core.management.base import BaseCommand, CommandError

from meeting_manager.services.zoomapi.api import get_users_list
from meeting_manager.services.zoomapi.exceptions import InvalidRefreshTokenError

class Command(BaseCommand):
    help = 'Update zoom_users database'

    def handle(self, *args, **options):
        try:
            user_list = get_users_list()
            self.stdout.write(self.style.SUCCESS('Successfully update zoom_users database'))
        except InvalidRefreshTokenError:
            CommandError(user_list)