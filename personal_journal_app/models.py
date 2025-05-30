from django.db import models
from django.contrib.auth.models import User

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)  # ⭐ Favorite field added

    def __str__(self):
        return self.title
