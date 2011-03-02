from datetime import datetime, timedelta
from celery.decorators import task
from django.db import transaction
from twitter.models import Status, TwitterUserProfile
from twitter.utils import get_authorized_twython

"""
@task
def cache_statuses(statuses, tp):
    with transaction.commit_manually():
        for s in statuses:
            tp.cached_statuses.add(s)
        s_ids = [s.id for s in statuses]
        s_found = set([s.id for s in Status.objects.filter(id__in=s_ids)])
        new_statuses = filter(lambda x: x.id not in s_found, statuses)
        for s in new_statuses:
            s.is_cached = True
            s.save()
        tp.save()
"""


@transaction.commit_on_success()
def cache_statuses(statuses, tp):
    s_ids = [s.id for s in statuses]

    s_cached = set([s.id for s in tp.cached_statuses.filter(id__in=s_ids)])
    usercache_statuses = filter(lambda x: x.id not in s_cached, statuses)
    for s in usercache_statuses:
        tp.cached_statuses.add(s)

    Status.savemany(statuses, is_cached=True)


@task
def cache_timeline_backfill(tp, twitter_tokens, statuses):
    """ Backfill cached timeline from the oldest tweet in statuses to
    the cached_time in TwitterUserProfile or 72 hours, whichever is sooner"""
    api = get_authorized_twython(twitter_tokens)
    oldest_time = datetime.now()-timedelta(hours=72)

    cache_statuses(statuses, tp)

    backfill_maxid = min(statuses, key=lambda x: x.id).id
    try: 
        backfill_minid = max(tp.cached_statuses.filter(created_at__gt=oldest_time), key=lambda x: x.id).id
        if backfill_maxid < backfill_minid: return
    except (IndexError, ValueError):
        backfill_minid = None
    print "backfill minid: " + str(backfill_minid)
    print "backfill maxid: " + str(backfill_maxid)

    finished = False
    total_num_statuses = len(statuses)
    while not finished:
        recieved_statuses = Status.construct_from_dicts(
            api.getFriendsTimeline(count=200, include_rts=True, 
                                   max_id=backfill_maxid, min_id=backfill_minid))
        total_num_statuses += len(recieved_statuses)

        cache_statuses(statuses, tp)
        if min(recieved_statuses, key=lambda x: x.created_at).created_at < oldest_time or total_num_statuses >= 600 or len(recieved_statuses) < 200: finished = True
        else: backfill_maxid = statuses[-1].id
