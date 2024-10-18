from rest_framework import serializers
from ..models import ReconciliationFile
from ..helpers import fields as input_fields
from ..helpers.file_hash import FileHash
from ..repositories.reconciliation import ReconciliationFileRepository

class ReconciliationFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationFile
        fields = [input_fields.SOURCE_FILE, input_fields.TARGET_FILE]

    def validate(self, attrs):
        sourcehash = FileHash(attrs.get(input_fields.SOURCE_FILE)).generate_file_hash()
        targethash = FileHash(attrs.get(input_fields.TARGET_FILE)).generate_file_hash()

        combined_hash = f"{sourcehash}:{targethash}"
        if ReconciliationFileRepository().it_exist(combined_hash):
            raise serializers.ValidationError(input_fields.FILE_RECONCILIATION_EXIST)

        attrs[input_fields.COMBINED_HASH] = combined_hash
        return attrs
