
class ReconciliationFileUploadService:
    def __init__(self, repository):
        self.repository = repository

    def upload_reconciliation_file(self, source_file, target_file, combined_hash):
        return self.repository.create(
            source_file=source_file,
            target_file=target_file,
            combined_hash=combined_hash
        )

    def get_reconciliation_file(self, req_hash: str):
        return self.repository.get(req_hash)