from ..services.upload_service import ReconciliationFileUploadService
from ..repositories.reconciliation import ReconciliationFileRepository


class ReconciliationBase:

    def __init__(self, *args, **kwargs):
        self.service = ReconciliationFileUploadService(repository=ReconciliationFileRepository())
