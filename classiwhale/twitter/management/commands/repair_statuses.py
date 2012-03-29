from django.core.management.base import BaseCommand, CommandError
from twython import Twython, TwythonError, APILimit, AuthError
from twitter.models import *


class Command(BaseCommand):
    args = 'none'
    help = 'Repairs Statuses in Status table'

    def handle(self, *args, **options):
        api = Twython()
        cached_statuses = {}
        cached_user_since_ids = {}
        cached_user_max_ids = {}
        statuses = (Status.objects.filter(text__isnull=True) |
                    Status.objects.filter(user__isnull=True) |
                    Status.objects.filter(created_at__isnull=True))
        self.stdout.write("Broken statuses: {0}\n".format(len(statuses)))
        for s in statuses:
            if s.id in cached_statuses: 
                status = cached_statuses[s.id]
            else:
                try: status = Status.construct_from_dict(api.showStatus(id=s.id))
                except APILimit:
                    self.stdout.write('Rate limit exceeded\n')
                    break
                except TwythonError:
                    continue
                try: max_id = cached_user_max_ids[status.user.id]
                except KeyError: max_id = None
                try: 
                    userstatuses = Status.construct_from_dicts(
                        api.getUserTimeline(user_id=status.user.id, 
                                            count=200, max_id=max_id))
                    for us in userstatuses:
                        cached_statuses[us.id] = us
                    cached_user_since_ids[status.user.id] = min([s.id for s in userstatuses])
                except ValueError: pass
            status.save()

            self.stdout.write('Repaired Status id {0}\n'.format(status.id))
