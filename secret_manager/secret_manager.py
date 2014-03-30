import json
from gnupg import GPG


def load_vault(file_descriptor, passphrase):
    """Load a secret vault from file_descriptor."""
    vault = Vault()
    vault.load(file_descriptor, passphrase)
    return vault.vault


def save_vault(file_descriptor, passphrase, vault):
    """Save a secret vault to file_descriptor."""
    vault_ = Vault()
    vault_.vault = vault
    vault_.save(file_descriptor, passphrase)


class Vault(object):

    def __init__(self):
        self.vault = {}
        self._gpg = GPG()
        self._file_descriptor = None
        self.passphrase = None

    def reload(self):
        if None in (self._file_descriptor, self.passphrase):
            raise RuntimeError('Cannot reload before calling .load()')
        self.load(self._file_descriptor, self.passphrase)

    def load(self, file_descriptor, passphrase):
        self._file_descriptor = file_descriptor
        self.passphrase = passphrase
        self._file_descriptor.seek(0)
        json_ = self._gpg.decrypt_file(self._file_descriptor, passphrase=self.passphrase)
        self.vault = json.loads(str(json_))

    def save(self, file_descriptor=None, passphrase=None):
        if file_descriptor is not None:
            self._file_descriptor = file_descriptor
        if passphrase is not None:
            self.passphrase = passphrase
        self._file_descriptor.seek(0)
        json_ = json.dumps(self.vault)
        encrypted = self._gpg.encrypt(json_, False, passphrase=self.passphrase, symmetric=True)
        self._file_descriptor.write(str(encrypted))

    def __getitem__(self, key):
        return self.vault[key]

    def get(self, name, default=None):
        return self.vault.get(name, default)

    def __setitem__(self, key, value):
        self.vault[key] = value

    def __delitem__(self, key):
        del self._vault[key]

    def list(self):
        return sorted(self._vault.keys())
