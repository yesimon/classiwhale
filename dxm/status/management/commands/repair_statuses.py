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
        cached_user_max_ids = {}
        statuses = (Status.objects.filter(text__isnull=True) |
                    Status.objects.filter(user_profile__isnull=True) |
                    Status.objects.filter(created_at__isnull=True))
        self.stdout.write("Broken statuses: {0}\n".format(len(statuses)))
        for s in statuses:
            if s.id in cached_statuses:
                status = cached_statuses[s.id]
            else:
                try: status = api.GetStatus(id=s.id)
                except twitter.TwitterError as error: 
                    e = error
                    if e.__str__().startswith('Sorry'):
                        continue
                    elif e.__str__().startswith('Rate'):
                        self.stdout.write('Rate limit exceeded\n')
                        break
                    else:
                        continue
                try: max_id = cached_user_max_ids[status.user.id]
                except KeyError: max_id = None
                try: 
                    userstatuses = api.GetUserTimeline(status.user.id, 
                                                   count=200, max_id=max_id)
                    for us in userstatuses:
                        cached_statuses[us.id] = us
                    cached_user_since_ids[status.user.id] = min([s.id for s in userstatuses])
                except ValueError: pass
            full_create_status(status)

            self.stdout.write('Repaired Status id {0}\n'.format(status.id))
