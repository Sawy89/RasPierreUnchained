from django.db import models



class Language(models.Model):
    '''
    Class identyfing the available launguages
    '''
    code = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name+" ("+self.code+")"


class Content(models.Model):
    '''
    Class for Content
    '''
    name = models.CharField(max_length=32)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="content")
    title = models.CharField(max_length=128)
    text_short = models.TextField(max_length=5000)
    text_all = models.TextField(max_length=5000)

    class Meta:
        unique_together = (("name", "language"),)
