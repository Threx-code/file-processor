from django.http import HttpResponse
from rest_framework.parsers import (MultiPartParser, FormParser, JSONParser, FileUploadParser)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from .serializers.upload import ReconciliationFileSerializer
from .helpers import fields as input_fields
from .bases.base_reconcile import ReconciliationBase
import csv


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


    def get(self, request, hash, file_format=None):

        req_hash = hash
        recon_file = self.service.get_reconciliation_file(req_hash)
        if not recon_file:
            return Response(status=status.HTTP_404_NOT_FOUND)

        reconciliation_result = self.service.perform_reconciliation(recon_file)

        if file_format == input_fields.CSV:
            return self.download_csv(reconciliation_result)

        return Response(data=reconciliation_result, status=status.HTTP_200_OK)

    def download_csv(self, reconciliation_result):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        writer = csv.writer(response)
        writer.writerow([input_fields.ID.upper(),
                         input_fields.NAME.Capitalize(),
                         input_fields.DATE.Capitalize(),
                            input_fields.AMOUNT.Capitalize(),
                            input_fields.TYPE.Capitalize()
                         ])
        for item in reconciliation_result.get(input_fields.MISSING_IN_TARGET, []):
            writer.writerow([
                item[input_fields.ID],
                item[input_fields.NAME],
                item[input_fields.DATE],
                item[input_fields.AMOUNT],
                input_fields.TARGET.capitalize()
            ])

        for item in reconciliation_result.get(input_fields.MISSING_IN_SOURCE, []):
            writer.writerow([
                item[input_fields.ID],
                item[input_fields.NAME],
                item[input_fields.DATE],
                item[input_fields.AMOUNT],
                input_fields.SOURCE.capitalize()
            ]
            )

        for discrepancy in reconciliation_result.get(input_fields.DISCREPANCIES, []):
            row = [discrepancy[input_fields.ID],
                   input_fields.EMPTY_STRING,
                   input_fields.EMPTY_STRING,
                   input_fields.EMPTY_STRING,
                   input_fields.DISCREPANCIES.capitalize()
                   ]
            difference = discrepancy[input_fields.DIFFERENCE]

            if input_fields.NAME in difference:
                row[1] = difference
            if input_fields.DATE in difference:
                row[2] = difference
            if input_fields.AMOUNT in difference:
                row[3] = difference
            writer.writerow(row)

        return response



