from django.db import models

from utilities.timestamp import TimeStamp

class User(TimeStamp):
    google_email  = models.CharField(max_length=100, unique=True, blank=False)
    name          = models.CharField(max_length=50, blank=False)
    day_of_birth  = models.DateField(null=True)
    profile_image = models.CharField(max_length=2000, null=True)
    ordinal       = models.ForeignKey('users.Ordinal', on_delete=models.CASCADE)
    admin         = models.ForeignKey('users.Admin', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'users'
        
class Ordinal(models.Model):
    ordinal = models.IntegerField(max_length=4, unique=True)
    
    class Meta:
        db_table = 'ordinals'
        
class Admin(models.Model):
    title = models.CharField(max_length=10, unique=True)
    
    class Meta:
        db_table = 'admins'
        
class Paper_like(TimeStamp):
    user  = models.ForeignKey('users.User', on_delete=models.CASCADE)
    paper = models.ForeignKey('buckets.Paper', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'paper_likes'
        constraints = [models.UniqueConstraint(
            fields = ['user', 'paper'],
            name = 'likes_user_paper_unq'
            )
        ]

class Paper_bookmark(TimeStamp):
    user  = models.ForeignKey('users.User', on_delete=models.CASCADE)
    paper = models.ForeignKey('buckets.Paper', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'paper_bookmarks'
        constraints = [models.UniqueConstraint(
            fields = ['user', 'paper'],
            name = 'bookmarks_user_paper_unq'
            )
        ]