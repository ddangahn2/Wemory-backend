from email.policy import default
from django.db import models

from utilities.timestamp import TimeStamp

class Bucket(TimeStamp):
    title   = models.CharField(max_length=200, blank=False)
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    ordinal = models.ForeignKey('users.Ordinal', on_delete=models.CASCADE)
    public  = models.BooleanField()
    background_color = models.ForeignKey('buckets.Background_color', on_delete= models.CASCADE, default = 1)
    
    class Meta:
        db_table = 'buckets'

# class Bucket_auth(models.Model):
#     user   = models.ForeignKey('users.User', on_delete=models.CASCADE)
#     bucket = models.ForeignKey('buckets.Bucket', on_delete=models.CASCADE)
#     edit   = models.BooleanField()
#     public = models.BooleanField()
    
#     class Meta:
#         db_table = 'bucket_auths'
        
class Paper(TimeStamp):
    bucket           = models.ForeignKey('buckets.Bucket', on_delete=models.CASCADE)
    user             = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content          = models.TextField(max_length=5000)
    x_axis           = models.IntegerField()
    y_axis           = models.IntegerField()
    background_color = models.ForeignKey('buckets.Background_color', on_delete=models.CASCADE)
    font             = models.ForeignKey('buckets.Font', on_delete=models.CASCADE)
    font_color       = models.ForeignKey('buckets.Font_color', on_delete=models.CASCADE)
    font_size        = models.ForeignKey('buckets.Font_size', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'papers'
        
class Comment(TimeStamp):
    paper   = models.ForeignKey('buckets.Paper', on_delete=models.CASCADE)
    user    = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
        
    class Meta:
        db_table = 'comments'
        
class Paper_image(models.Model):
    paper     = models.ForeignKey('buckets.Paper', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=2000)
    
    class Meta:
        db_table = 'paper_images'
        
class Background_color(models.Model):
    color_code = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'background_colors'
        
class Font(models.Model):
    name = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'fonts'
        
class Font_color(models.Model):
    color_code = models.CharField(max_length=10)
    
    class Meta:
        db_table = 'font_colors'
        
class Font_size(models.Model):
    size = models.IntegerField()
    
    class Meta:
        db_table = 'font_sizes'