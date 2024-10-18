from ..helpers import fields as input_fields
from ..helpers.nomalize import Normalizer
from ..repositories.reconciliation import ReconciliationFileRepository


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

    def it_exist(self, combined_hash):
        return self.repository.it_exist(combined_hash)


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
