from __future__ import unicode_literals
from django.db import models
from apps.login_app.models import *
from apps.appointment_app.models import Appointments

class MessageManager(models.Manager):
    def message_validator(self, postData):
        errors = {}
        print(postData)
        print("ppppppppppppppppppppppppppppppppppppppp")
        if len(postData['post']) < 1:
            errors['length'] = "Cannot post a blank message!"
        return errors

class Messages(models.Model):
    content = models.TextField()
    message_owner = models.ForeignKey(Users, related_name = 'messages')
    appointment = models.ForeignKey(Appointments, related_name = 'messages')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = MessageManager()
