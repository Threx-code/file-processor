from rest_framework.parsers import (MultiPartParser, FormParser, JSONParser, FileUploadParser)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .serializers.upload import ReconciliationFileSerializer
from .helpers import fields as input_fields
from .bases.base_reconcile import ReconciliationBase


from reconciliation_file.helpers.nomalize import Normalizer


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



    def get(self, request, hash, req_format=None):
        req_hash = hash
        recon_file = self.service.get_reconciliation_file(req_hash)
        if not recon_file:
            return Response(status=status.HTTP_404_NOT_FOUND)

        reconciliation_result = self.perform_reconciliation(recon_file)

        return Response(data=reconciliation_result, status=status.HTTP_200_OK)




    def perform_reconciliation(self, recon_file):
        source_file = Normalizer().nomalize(recon_file.source_file)
        target_file = Normalizer().nomalize(recon_file.target_file)

        missing_in_target, missing_in_source, discrepancies = self.reconcile(source_file, target_file)

        return {
            'missing_in_target': missing_in_target,
            'missing_in_source': missing_in_source,
            'discrepancies': discrepancies
        }




    def reconcile(self, source_data, target_data):
        source_dict = { row[input_fields.ID]: row for row in source_data}
        target_dict = { row[input_fields.ID]: row for row in target_data}

        missing_in_target = [row for row in source_data if row[input_fields.ID] not in target_dict]
        missing_in_source = [row for row in target_data if row[input_fields.ID] not in source_dict]

        discrepancies = []

        for id, source_now in source_dict.items():
            target_now = target_dict.get(id)
            if target_now:
                diff = {
                    input_fields.ID:id,
                    'difference': {
                        key: {
                            'source': source_now[key],
                            'target': target_now[key]
                        }
                        for key in source_now if source_now[key] != target_now[key]
                    }
                }
                if diff['difference']:
                    discrepancies.append(diff)

        return missing_in_target, missing_in_source, discrepancies








