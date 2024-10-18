import hashlib

class FileHash:
    def __init__(self, file_path):
        self.file_path = file_path

    def generate_file_hash(self, hash_type="sha256"):
        hash_format = hashlib.new(hash_type)
        with open(self.file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_format.update(chunk)
        return hash_format.hexdigest()