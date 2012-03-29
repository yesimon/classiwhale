import django.dispatch
from datetime import datetime, timedelta

from twitter.models import Status
from twitter.utils import get_authorized_twython



cache_timeline_signal = django.dispatch.Signal(providing_args=
                                               ['statuses', 'twitter_user_profile'])
cache_timeline_backfill_signal = django.dispatch.Signal(providing_args=
                            ['statuses', 'twitter_user_profile', 'twitter_tokens'])


def cache_timeline_callback(sender, **kwargs):
    statuses, tp = kwargs['statuses'], kwargs['twitter_user_profile']
    tp.cached_time = datetime.now()
    for s in statuses:
        print s
        try:
            Status.objects.get(id=s.id)
        except Status.DoesNotExist:
            tp.cached_statuses.add(s)
            s.is_cached = True
            s.save()
    tp.save(override=True)

    


def cache_timeline_backfill_callback(sender, **kwargs):
    """ Backfill cached timeline from the oldest tweet in statuses to
    the cached_time in TwitterUserProfile or 72 hours, whichever is sooner"""
    statuses, tp = kwargs['statuses'], kwargs['twitter_user_profile']
    twitter_tokens = kwargs['twitter_tokens']
    api = get_authorized_twython(twitter_tokens)
    oldest_time = datetime.now()-timedelta(hours=72)

    """
    backfill_start = min(statuses, key=lambda x: x.created_at)
    backfill_end = max([tp.cached_time, oldest_time])
    if backfill_start < backfill_end: return
    """

    backfill_maxid = min(statuses, key=lambda x: x.id).id
    try: 
        backfill_minid = max(tp.cached_statuses.filter(created_at__gt=oldest_time), key=lambda x: x.id).id
        if backfill_maxid < backfill_minid: return
    except IndexError:
        backfill_minid = None
 
#    print "backfill minid: " + str(backfill_minid)
#    print "backfill maxid: " + str(backfill_maxid)

    cache_timeline_signal.send(sender=sender, statuses=statuses,
                               twitter_user_profile=tp)

    finished = False
    total_num_statuses = len(statuses)
    while not finished:
        recieved_statuses = Status.construct_from_dicts(
            api.getFriendsTimeline(count=200, include_rts=True, 
                                   max_id=backfill_maxid, min_id=backfill_minid))
        total_num_statuses += len(recieved_statuses)
        cache_timeline_signal.send(sender=sender, statuses=recieved_statuses,
                                   twitter_user_profile=tp)
        if total_num_statuses >= 600 or len(recieved_statuses) < 200: finished = True
        else: backfill_maxid = statuses[-1].id
        
    




cache_timeline_signal.connect(cache_timeline_callback)
cache_timeline_backfill_signal.connect(cache_timeline_backfill_callback)
