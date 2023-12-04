from django.db import models
from django.contrib import auth

# Create your models here.
class Manuscript(models.Model):
    manuscript_id = models.AutoField(primary_key=True, unique=True)
    manuscript_title = models.CharField(max_length=200, default='')
    manuscript_owner = models.ForeignKey(auth.models.User, on_delete=models.CASCADE, null=True)
    manuscript_abstract = models.TextField(default='')
    manuscript_api = models.TextField(default='')
    novelty_score = models.IntegerField(default=1)
    similarity_percentage = models.DecimalField(decimal_places=2, max_digits=5, default=0.00)

    def __str__(self) -> str:
        return super().__str__()
    
    def createManuscript(self, manuscript_title, manuscript_owner, manuscript_abstract, manuscript_api, novelty_score, similarity_percentage):
        self.manuscript_title = manuscript_title
        self.manuscript_owner = manuscript_owner
        self.manuscript_abstract = manuscript_abstract
        self.manuscript_api = manuscript_api
        self.novelty_score = novelty_score
        self.similarity_percentage = similarity_percentage # Save the Manuscript object to the database

    def deleteManuscript(self, manuscript_id):
        self.objects.filter(id=manuscript_id).delete()
