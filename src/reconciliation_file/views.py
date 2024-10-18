from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from reconciliation_file.models import ReconciliationFile
from .serializers.upload import ReconciliationFileSerializer
from .helpers import fields as input_fields
from .services.upload_service import ReconciliationFileUploadService
from .repositories.reconciliation import ReconciliationFileRepository

class ReconciliationFileUploadApi(CreateAPIView):
    serializer_class = ReconciliationFileSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = ReconciliationFileUploadService(
            repository=ReconciliationFileRepository()
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        source_file = serializer.validated_data[input_fields.SOURCE_FILE]
        target_file = serializer.validated_data[input_fields.TARGET_FILE]
        combined_hash = serializer.validated_data[input_fields.COMBINED_HASH]

        reconciliation_file = self.service.upload_reconciliation_file(source_file, target_file, combined_hash)

        return Response({
            input_fields.MESSAGE: input_fields.FILE_UPLOADED_SUCCESSFULLY,
            input_fields.DATA: {
                input_fields.HASH: combined_hash
            }
        }, status=status.HTTP_201_CREATED)

