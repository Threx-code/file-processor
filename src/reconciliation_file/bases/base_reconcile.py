from reconciliation_file.services.upload_service import ReconciliationFileUploadService
from reconciliation_file.repositories.reconciliation import ReconciliationFileRepository


class ReconciliationBase:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = ReconciliationFileUploadService(repository=ReconciliationFileRepository())
