
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Member

# register as receiver func, attach m2m_changed signal (is sent when a ManyToManyField on a model is changed
@receiver(m2m_changed,sender=Member.followers.through)
def followers_changed(sender, instance, **kwargs):
    instance.total_followers = instance.followers.count()
    instance.save()