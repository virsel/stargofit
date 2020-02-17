from django.contrib.contenttypes.models import ContentType
from .models import Action
import datetime
from django.utils import timezone

def create_action(member,verb,target=None):
    # check for any similar action made in the las minute
    now = timezone.now()
    last_minute= now - datetime.timedelta(seconds=60)
    #  retrieve any identical actions performed by member since then
    similar_actions = Action.objects.filter(member_id=member.id,verb=verb,created=last_minute)

    if target:
        target_ct=ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,target_id=target.id)

    if not similar_actions:
        # no existing actions found
        action = Action(member=member, verb=verb,target=target)
        action.save()
        return True

    return False