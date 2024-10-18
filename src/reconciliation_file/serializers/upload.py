from importlib.util import source_hash

from rest_framework import serializers
from .models import ReconciliationFile
from reconciliation_file.helpers import fields as input_fields
from reconciliation_file.helpers.file_hash import FileHash

class ReconciliationFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconciliationFile
        fields = [input_fields.SOURCE_FILE, input_fields.TARGET_FILE]

    def validate(self, attrs):
        sourcehash = FileHash(attrs.get(input_fields.SOURCE_FILE)).get_hash()
        targethash = FileHash(attrs.get(input_fields.TARGET_FILE)).get_hash()
        combined_hash = f"{sourcehash}:{targethash}"
        if ReconciliationFile.objects.filter(hash=combined_hash).exists():
            raise serializers.ValidationError(input_fields.FILE_RECONCILIATION_EXIST)

        attrs[input_fields.SOURCE_FILE] = sourcehash
        attrs[input_fields.TARGET_HASH] = targethash
        attrs[input_fields.COMBINED_HASH] = combined_hash
        return attrs
