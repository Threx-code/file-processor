from ..models import ReconciliationFile

class ReconciliationFileRepository:

    def create(self, source_file, target_file, combined_hash):
        return ReconciliationFile.objects.create(
            source_file=source_file,
            target_file=target_file,
            file_hash=combined_hash
        )

    def get(self, req_hash: str):
        try:
            return ReconciliationFile.objects.get(file_hash=req_hash)
        except ReconciliationFile.DoesNotExist:
            return None

    def it_exist(self, combined_hash):
        return ReconciliationFile.objects.filter(file_hash=combined_hash).exists()