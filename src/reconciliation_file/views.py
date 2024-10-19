from rest_framework.parsers import (MultiPartParser, FormParser, JSONParser, FileUploadParser)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .serializers.upload import ReconciliationFileSerializer
from .helpers import fields as input_fields
from .bases.base_reconcile import ReconciliationBase



class ReconciliationFileUploadAPI(CreateAPIView, ReconciliationBase):
    serializer_class = ReconciliationFileSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser, FileUploadParser)

    def __init__(self, *args, **kwargs):
        ReconciliationBase.__init__(self)
        super().__init__(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        source_file = serializer.validated_data[input_fields.SOURCE_FILE]
        target_file = serializer.validated_data[input_fields.TARGET_FILE]
        combined_hash = serializer.validated_data[input_fields.COMBINED_HASH]

        reconciliation_file = self.service.upload_reconciliation_file(
            source_file=source_file,
            target_file=target_file,
            combined_hash=combined_hash
        )

        return Response(data={
            input_fields.MESSAGE: input_fields.FILE_UPLOADED_SUCCESSFULLY,
            input_fields.DATA: {
                input_fields.HASH: combined_hash
            }
        }, status=status.HTTP_201_CREATED)




class ReconciliationFileReportAPI(APIView, ReconciliationBase):

    def __init__(self, *args, **kwargs):
        ReconciliationBase.__init__(self)
        super().__init__(*args, **kwargs)

    def get(self, request, req_hash, file_format=None):
        recon_file = self.service.get_reconciliation_file(req_hash)
        if not recon_file:
            return Response(data={
                input_fields.MESSAGE: input_fields.FILE_RECONCILIATION_NOT_EXIST,
                input_fields.DATA: {
                    input_fields.HASH: req_hash
                }
            },status=status.HTTP_404_NOT_FOUND)

        reconciliation_result = self.service.perform_reconciliation(recon_file)

        if file_format == input_fields.CSV:
            return self.service.download_csv(reconciliation_result)

        return Response(data=reconciliation_result, status=status.HTTP_200_OK)


