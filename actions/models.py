from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings

class Action(models.Model):
    member = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='actions',db_index=True,on_delete=models.CASCADE)
    # describes the action that the member performes
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    # model for the relationship
    target_ct = models.ForeignKey(ContentType,blank=True,null=True,related_name='target_obj',on_delete=models.CASCADE)
    # for matching django's automatic primary key fields
    target_id = models.PositiveIntegerField(null=True,blank=True,db_index=True)
    # to define and manage the relation using target_ct and target_id
    target = GenericForeignKey('target_ct','target_id')

    class Meta:
        ordering = ('-created',)

