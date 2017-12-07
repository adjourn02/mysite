from django.db import models
import sys
sys.path.append('..')
from ckeditor_uploader.fields import RichTextUploadingField

class Country(models.Model):
    country_name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.country_name

class Place(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    place_name = models.CharField(max_length=20)

    def __str__(self):
        return self.place_name

class Post(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = RichTextUploadingField(blank=True)
    photo = models.ImageField(upload_to='blogs/images', blank=True, null=True)
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField('date published')
    featured = models.BooleanField(default=False)
    popular = models.BooleanField(default=False)

    def __str__(self):
        return self.title