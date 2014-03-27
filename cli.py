from secret_manager import save_vault, load_vault
from pprint import pprint
from getpass import getpass
import os
import sys
try:
    from itertools import izip_longest
except ImportError:
    from itertools import zip_longest as izip_longest


try:
    input = raw_input
except NameError:
    pass


def possible_matches(string):
    l = []
    last = ''
    for c in string:
        last = last + c
        l.append(last)
    return l


def matches(target, string):
    if len(target) < len(string):
        return False
    possible_target = possible_matches(target)
    possible_string = possible_matches(string)
    for t, s in izip_longest(possible_target, possible_string, fillvalue=None):
        if None in (t, s):
            return True
        if t != s:
            return False
    else:
        return True


def ask_yn(prompt):
    valid_yes, valid_no = possible_matches('yes'), possible_matches('no')
    valid = valid_yes + valid_no
    response = ''
    while response not in valid:
        response = input(prompt)
    if response in valid_yes:
        return True
    elif response in valid_no:
        return False


class CLI(object):

    VERB_PREFIX = 'verb_'

    def __init__(self, filename=None, passphrase=None):
        self.filename = filename
        self.passphrase = passphrase
        self.secrets = {}

    @property
    def verbs(self):
        return [verb.replace(self.VERB_PREFIX, '', 1) for verb in dir(self)
                if verb.startswith(self.VERB_PREFIX)]

    def start(self):
        if self.filename is None:
            self.filename = input('Filename: ')
        if self.passphrase is None:
            self.passphrase = getpass('Passphrase: ')

        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                self.secrets = load_vault(f, self.passphrase)
        else:
            print('File {} does not exist, will create on save.'.format(self.filename))

        while True:
            self._loop()

    def _loop(self):
        command = input('{}> '.format(os.path.basename(self.filename)))
        components = command.split()
        verb, args = components[0], components[1:]
        resolved_verb = self._resolve_verb(verb)
        if resolved_verb is None:
            self.verb_usage([])
            return
        function = getattr(self, resolved_verb)
        function(args)

    def _resolve_verb(self, verb):
        verb_matches = [maybe_verb for maybe_verb in self.verbs if matches(maybe_verb, verb)]
        if len(verb_matches) > 1:
            raise RuntimeError('More than one verb match.')
        elif len(verb_matches) == 0:
            return None
        else:
            return self.VERB_PREFIX + verb_matches[0]

    def verb_get(self, args):
        for node in args:
            pprint(self.secrets.get(node, 'Invalid node "{}"'.format(node)))

    def verb_set(self, args):
        if len(args) != 1:
            print('Wrong number of args for set (needs one).')
            return
        name = args[0]
        value, values = None, []
        while value != '':
            value = input('> ')
            values.append(value)
        self.secrets[name] = eval('\n'.join(values))

    def verb_list(self, args):
        pprint(sorted(self.secrets.keys()))

    def verb_exit(self, args):
        should_save = ask_yn('Save? ')
        if should_save:
            self.verb_write([])
        exit()

    def verb_write(self, args):
        with open(self.filename, 'wb') as f:
            save_vault(f, self.passphrase, self.secrets)

    def verb_usage(self, args):
        message = 'Verbs: ' + ' '.join(self.verbs)
        print(message)


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) > 1:
        sys.stdout.write('Usage: {} [filename]'.format(sys.argv[0]))
        exit(1)
    if len(args) == 1:
        filename = args[0]
    else:
        filename = None
    cli = CLI(filename=filename)
    cli.start()
