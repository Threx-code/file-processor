from django.template.loader import render_to_string

from ..helpers import fields as input_fields
from ..helpers.nomalize import Normalizer
from django.http import HttpResponse
import csv

class ReconciliationFileDownloadService:
    def __init__(self, repository):
        self.repository = repository

    def get_reconciliation_file(self, req_hash: str):
        return self.repository.get(req_hash)

    def perform_reconciliation(self, recon_file):
        source_file = Normalizer().nomalize(recon_file.source_file)
        target_file = Normalizer().nomalize(recon_file.target_file)

        missing_in_target, missing_in_source, discrepancies = self.reconcile(source_file, target_file)

        return {
            input_fields.MISSING_IN_TARGET: missing_in_target,
            input_fields.MISSING_IN_SOURCE: missing_in_source,
            input_fields.DISCREPANCIES: discrepancies
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
                    input_fields.DIFFERENCE: {
                        key: {
                            input_fields.SOURCE: source_now[key],
                            input_fields.TARGET: target_now[key]
                        }
                        for key in source_now if source_now[key] != target_now[key]
                    }
                }
                if diff[input_fields.DIFFERENCE]:
                    discrepancies.append(diff)

        return missing_in_target, missing_in_source, discrepancies

    def download_html(self, reconciliation_result):
        html_content = render_to_string(input_fields.HTML_TEMPLATE, reconciliation_result)
        response = HttpResponse(html_content, content_type=input_fields.HTML_TYPE)
        response[input_fields.CONTENT_DISPOSITION] = input_fields.FILE_HTML_NAME
        return response

    def download_csv(self, reconciliation_result):
        response = HttpResponse(content_type=input_fields.CSV_TYPE)
        response[input_fields.CONTENT_DISPOSITION] = input_fields.FILE_ATTACHMENT_NAME

        writer = csv.writer(response)
        writer.writerow([input_fields.ID.upper(),
                         input_fields.NAME.capitalize(),
                         input_fields.DATE.capitalize(),
                            input_fields.AMOUNT.capitalize(),
                            input_fields.TYPE.capitalize()
                         ])
        self.source_target_format(reconciliation_result, input_fields.MISSING_IN_TARGET, input_fields.TARGET,  writer)
        self.source_target_format(reconciliation_result, input_fields.MISSING_IN_SOURCE, input_fields.SOURCE, writer)

        self.discrepancy_format(reconciliation_result, writer)

        return response

    def discrepancy_format(self, reconciliation_result, writer):
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

    def source_target_format(self, reconciliation_result, input_type, item_type, writer):
        for item in reconciliation_result.get(input_type, []):
            writer.writerow([
                item[input_fields.ID],
                item[input_fields.NAME],
                item[input_fields.DATE],
                item[input_fields.AMOUNT],
                item_type.capitalize()
            ])

