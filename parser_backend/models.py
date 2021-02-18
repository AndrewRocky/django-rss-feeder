from django.db import models
from django.utils import timezone

# Create your models here.

class Folder(models.Model):
    title = models.TextField(verbose_name="Title of this folder")

    def __str__(self):
        return self.title


class Feed(models.Model):
    url = models.URLField(verbose_name="URL of the site this feed refers to. Also is used as GUID.")
    title = models.TextField(verbose_name="Default name of the feed.")
    preferred_title = models.TextField(verbose_name="User-preferred name of the feed. By default same as title.", default = title)
    description = models.TextField(verbose_name="Description taken from feed.", blank=True, default="")
    picture = models.URLField(verbose_name="URL to the picture.", blank=True, default="static/images/default_feed.ico")
    update_frequency = models.PositiveIntegerField(verbose_name="Feed update frequency in seconds.", default=600)
    last_modified = models.DateTimeField(verbose_name="Date and time of last update of this Feed.", default=timezone.now)
    last_updated = models.DateTimeField(verbose_name="Date and time when this feed was last checked for updates")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date when this Feed was added to the database.")
    parent_folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Database link to the Folder this Feed is put into.")
    is_available = models.BooleanField(verbose_name="False if last update wasn't succesful.", default= True)

    def __str__(self):
        return self.title

class Post(models.Model):
    is_read = models.BooleanField(verbose_name="True if read, False(default) if not read")
    title = models.TextField(verbose_name="Name of the Post")
    release_date = models.DateTimeField(verbose_name="Date and time when this post was released")
    recieved_date = models.DateTimeField(auto_now_add=True, verbose_name="Date and time when this post was recieved")
    url = models.URLField(verbose_name="Link that this post refers to")
    is_starred = models.BooleanField(verbose_name="True is starred, False(default) if not starred")
    parent_feed = models.ForeignKey(Feed, on_delete=models.CASCADE, verbose_name="Database link to the Feed this Post came from")
    guid = models.TextField(verbose_name="Unigue GUID for this post. When checking for new posts server will compare posts' GUID.")

    def __str__(self):
        return self.title

if __name__ == "__main__":
    pass