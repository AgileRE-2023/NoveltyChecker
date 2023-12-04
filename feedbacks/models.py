from django.db import models
from django.contrib import auth

# Create your models here.
class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True, unique=True)
    feedback_owner = models.ForeignKey(auth.models.User, on_delete=models.CASCADE, null=True)
    feedback_manuscript = models.ForeignKey('search.Manuscript', on_delete=models.CASCADE, null=True)
    feedback_score = models.IntegerField(default=5)
    feedback_content = models.TextField(default='')
    feedback_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return super().__str__()
    
    def createFeedback(self, feedback_owner, feedback_manuscript, feedback_content, feedback_score):
        self.feedback_owner = feedback_owner
        self.feedback_manuscript = feedback_manuscript
        self.feedback_content = feedback_content
        self.feedback_score = feedback_score

    def deleteFeedback(self, feedback_id):
        self.objects.filter(id=feedback_id).delete()