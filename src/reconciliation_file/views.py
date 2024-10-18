from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from reconciliation_file.models import ReconciliationFile
from .serializers.upload import ReconciliationFileSerializer
from .helpers import fields as input_fields

class ReconciliationFileUploadApi(CreateAPIView):
    serializer_class = ReconciliationFileSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        source_file = serializer.validated_data[input_fields.SOURCE_FILE]
        target_file = serializer.validated_data[input_fields.TARGET_FILE]
        source_hash = serializer.validated_data[input_fields.SOURCE_HASH]
        target_hash = serializer.validated_data[input_fields.TARGET_HASH]
        combined_hash = serializer.validated_data[input_fields.COMBINED_HASH]

        reconciliation_file = ReconciliationFile.objects.create(
            source_file=source_file,
            target_file=target_file,
            file_hash=combined_hash
        )


        return Response({
            input_fields.MESSAGE: input_fields.FILE_UPLOADED_SUCCESSFULLY,
            input_fields.DATA: {
                input_fields.HASH: combined_hash
            }
        }, status=status.HTTP_201_CREATED)

