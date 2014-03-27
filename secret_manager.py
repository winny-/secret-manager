import json
from gnupg import GPG


def load_vault(file_descriptor, passphrase):
    """Load a secret vault from file_descriptor."""
    gpg = GPG()
    file_descriptor.seek(0)
    json_ = gpg.decrypt_file(file_descriptor, passphrase=passphrase)
    return json.loads(str(json_))


def save_vault(file_descriptor, passphrase, vault):
    """Save a secret vault to file_descriptor."""
    gpg = GPG()
    file_descriptor.seek(0)
    json_ = json.dumps(vault)
    encrypted = gpg.encrypt(json_, False, passphrase=passphrase, symmetric=True)
    file_descriptor.write(str(encrypted))
