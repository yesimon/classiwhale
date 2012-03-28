from datetime import datetime, timedelta
from celery.decorators import task, periodic_task
from django.db import transaction, connection
from twitter.models import Status, TwitterUserProfile, CachedStatus, Rating
from twitter.utils import get_authorized_twython

from algorithmio.interface import get_predictions, force_train


def cache_statuses(statuses, tp):
    s_ids = [s.id for s in statuses]
    s_cached = set([s.id for s in tp.cached_statuses.filter(id__in=s_ids)])
    Status.savemany(statuses, is_cached=True)

    usercache_statuses = []
    for s in statuses:
        if s.id in s_cached: continue
        s_cached.add(s.id)
        usercache_statuses.append(s)
    predictions = get_predictions(tp, usercache_statuses)
    CachedStatus.objects.create_in_bulk(tp, usercache_statuses, predictions)

@periodic_task(run_every=timedelta(hours=2))
def cache_clean():
    Status.clear_cache()

@task
def cache_timeline_backfill(tp, twitter_tokens, statuses):
    """ Backfill cached timeline from the oldest tweet in statuses to
    the cached_time in TwitterUserProfile or 72 hours, whichever is sooner"""
    api = get_authorized_twython(twitter_tokens)
    cutoff_time = datetime.utcnow()-timedelta(hours=72)

    if not statuses:
        statuses = Status.construct_from_dicts(api.getFriendsTimeline(include_rts=True))

    backfill_maxid = min(statuses, key=lambda x: x.id).id
    backfill_newestid = max(statuses, key=lambda x: x.id).id

    # Maxid and minid indicate contiguous cached status ids
    minid = getattr(tp, 'cached_minid', 0)
    maxid = getattr(tp, 'cached_maxid', 0)

    # No new tweets at all
    if backfill_newestid == maxid: return

    # Only one page of new tweets - just cache these
    if backfill_maxid < maxid:
        cache_statuses(statuses, tp)
        return

    # Cache as far back as 800 tweets or 72 hours worth
    num_apicalls = 1
    finished = False
    total_num_statuses = len(statuses)
    while not finished:
        print "backfill minid: " + str(maxid)
        print "backfill maxid: " + str(backfill_maxid)


        recieved_statuses = Status.construct_from_dicts(
            api.getFriendsTimeline(count=200, include_rts=True,
                                   max_id=backfill_maxid, min_id=maxid))
        num_apicalls += 1
        total_num_statuses += len(recieved_statuses)

        statuses.extend(recieved_statuses)

        oldest_status = min(recieved_statuses, key=lambda x: x.id)
        if (oldest_status.created_at < cutoff_time or
            oldest_status.id <= maxid or
            num_apicalls >= 5): finished = True
        else: backfill_maxid = oldest_status.id

    # Set new minid, maxid for contiguous cached statuses
    if oldest_status.id <= maxid:
        tp.cached_minid = minid
    else:
        tp.cached_minid = oldest_status.id
    tp.cached_maxid = backfill_newestid
    tp.save()

    # If less than 50 rated statuses: force train user classifier
    if Rating.objects.filter(user=tp).count() < 50:
        force_train(tp)

#    print "num apicalls: " + str(num_apicalls)
    cache_statuses(statuses, tp)
