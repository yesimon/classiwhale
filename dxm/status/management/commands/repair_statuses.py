from django.core.management.base import BaseCommand, CommandError
from status.models import Status
from status.views import full_create_status
import twitter

class Command(BaseCommand):
    args = 'none'
    help = 'Repairs Statuses in Status table'

    def handle(self, *args, **options):
        api = twitter.Api()
        cached_statuses = {}
        cached_user_since_ids = {}
        statuses = (Status.objects.filter(text__isnull=True) |
                    Status.objects.filter(user_profile__isnull=True) |
                    Status.objects.filter(created_at__isnull=True))
        for s in statuses:
            if s.id in cached_statuses:
                status = cached_statuses[s.id]
            else:
                status = api.GetStatus(id=s.id)
                try: since_id = cached_user_since_ids[status.user.id]
                except KeyError: since_id = None
                try: 
                    userstatuses = api.GetUserTimeline(status.user.id, 
                                                   count=200, since_id=since_id)
                    for us in userstatuses:
                        cached_statuses[us.id] = us
                    cached_user_since_ids[status.user.id] = min([s.id for s in userstatuses])
                except ValueError: pass
            full_create_status(status)

            self.stdout.write('Repaired Status id {0}\n'.format(status.id))
