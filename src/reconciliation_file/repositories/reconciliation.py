from reconciliation_file.models import ReconciliationFile

class ReconciliationFileRepository:

    def create(self, source_file, target_file, combined_hash):
        reconciliation_file = ReconciliationFile.objects.create(
            source_file=source_file,
            target_file=target_file,
            file_hash=combined_hash
        )

        return reconciliation_file