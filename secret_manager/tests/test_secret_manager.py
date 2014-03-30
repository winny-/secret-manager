from .. import secret_manager
import unittest
from StringIO import StringIO


class Test(unittest.TestCase):

    def setUp(self):
        self.secrets = {
            'github': {
                'username': 'someuser',
                'password': 'somepassword'
            },
        }
        self.vault = '-----BEGIN PGP MESSAGE-----\nVersion: GnuPG v1' \
            '\n\njA0EAwMCkSkZuGk6Eg1gyUUhNxGnhSQjaBNK2TpDiE+iTaPVvav' \
            'D1YehZRjtHql8\nAVJADg72tKclDfOZtCo7IoSAUSlgu6Bg/AA0v1cp' \
            'a1P0ic5Zihk=\n=XCn4\n-----END PGP MESSAGE-----\n'
        self.passphrase = 'passphrase'

    def test_load_vault(self):
        f = StringIO(self.vault)
        decoded_secrets = secret_manager.load_vault(f, self.passphrase)
        self.assertEquals(decoded_secrets, self.secrets)

    def test_vault_reversibility(self):
        f = StringIO()
        secret_manager.save_vault(f, self.passphrase, self.secrets)
        decoded_secrets = secret_manager.load_vault(f, self.passphrase)
        self.assertEquals(decoded_secrets, self.secrets)


    def test_Vault_class(self):
        f = StringIO(self.vault)
        vault = secret_manager.Vault()
        vault.load(f, self.passphrase)
        self.assertEquals(vault.vault, self.secrets)
        vault.save()
        vault.reload()
        self.assertEquals(vault.vault, self.secrets)



if __name__ == '__main__':
    unittest.main()
