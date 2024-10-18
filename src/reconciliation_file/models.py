from django.db import models

class ReconciliationFile(models.Model):
    source_file = models.FileField(upload_to='reconciliation_files/')
    target_file = models.FileField(upload_to='reconciliation_files/')
    file_hash = models.CharField(max_length=255, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Source: {self.source_file.name} - Target: {self.target_file.name}"
