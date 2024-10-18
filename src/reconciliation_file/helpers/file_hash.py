import hashlib

class FileHash:
    def __init__(self, file_path):
        self.file_path = file_path

    def generate_file_hash(self, hash_type="md5"):
        hash_format = hashlib.new(hash_type)
        for chunk in self.file_path.chunks():
            hash_format.update(chunk)
        return hash_format.hexdigest()