from django.db import models

# Create your models here.
class Pages(models.Model):
    post_author = models.ForeignKey("core.UserAccount", verbose_name=_(""), on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now=True)
    post_content = models.TextField()
    post_title = models.TextField()
    post_excerpt = models.TextField()
    #TODO: add in a choice field for post status, comment_status and ping status 
    post_status = models.CharField()
    comment_status = models.BooleanField(default=False)
    post_name = models.CharField()
    post_modified = models.DateTimeField()
    guid = models.CharField(max_length=255)
    # TODO: create choice field for post type
    post_type = models.CharField()
    post_mime_type = models.CharField()
    comment_count = models.BigIntegerField()
    