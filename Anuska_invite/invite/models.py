

# Create your models here.
from django.db import models
 
class Response(models.Model):
    step_name = models.CharField(max_length=100)
    answer    = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)
 
    def __str__(self):
        return f"[{self.timestamp:%Y-%m-%d %H:%M}] {self.step_name} → {self.answer}"
 
    class Meta:
        ordering = ['-timestamp']