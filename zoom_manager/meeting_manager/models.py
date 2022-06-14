from django.db import models

# Create your models here.


class ZoomUsers(models.Model):

    host_id = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.host_id

    class Meta:
        db_table = "zoom_users"


class ZoomMeetings(models.Model):

    uuid = models.CharField(max_length=255, primary_key=True)
    host_id = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255)
    duration = models.IntegerField()
    type = models.IntegerField()
    join_url = models.CharField(max_length=1000)

    def __str__(self):
        return self.topic

    class Meta:

        db_table = "zoom_meetings"


class ZoomCredentionals(models.Model):

    name_data = models.CharField(max_length=255, primary_key=True)
    data = models.CharField(max_length=255)

    def __str__(self):
        return self.name_data

    class Meta:
        db_table = "zoom_credentionals"
