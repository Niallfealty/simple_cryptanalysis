#!/usr/bin/env python3
""" Basic caeser cipher encrypt/decrypt
"""

ALEPH = "abcdefghijklmnopqrstuvwxyz"

class Lookup:
    """ Like a dict but maps to itself if not present
    """
    def __init__(self, lookup_dict):
        self._lookup = lookup_dict

    def __getitem__(self, key):
        return self._lookup.get(key, key)

def build_lookup(offset, alphabet=ALEPH):
    lookup = {} # this will map from unencrypted to encrypted or v.v.
    for i, char in enumerate(alphabet):
        enc_index = (i + offset) % len(alphabet)
        lookup[char] = alphabet[enc_index]
    return Lookup(lookup)

def shift_chars_word(word, lookup):
    ''' Shift chars in word using lookup already built
    '''
    return "".join([lookup[char] for char in word])

def encrypt_pt(pt, offset):
    ''' Encrypt a single line plaintext pt by shifting chars by offset
    '''
    lookup = build_lookup(offset)
    return " ".join(
            [shift_chars_word(word, lookup) for word in pt.split(" ")]
        )

def decrypt_ct(ct, encrypt_offset):
    ''' Recalculate the offset and use the encrypt function to decrypt
    '''
    decrypt_offset = 26 - encrypt_offset
    return encrypt_pt(ct, decrypt_offset)

def read_stream_if_empty_input(cli_input):
    ''' If no input then read stdin instead
    '''
    if len(cli_input) > 0:
        return cli_input.replace("\n", " ").lower()
    else:
        from sys import stdin
        return stdin.read().replace("\n", " ").lower()

if __name__ == "__main__":
    from sys import argv
    action  = argv[1].lower()
    if action in ("-h", "--help", "h", "help"):
        print(f"{argv[0]} <action> [<encryption_offset> <data_to_encrypt>]")
    elif action == "encrypt":
        offset = int(argv[2])
        pt = " ".join(argv[3:]).replace("\n", " ")
        print(encrypt_pt(read_stream_if_empty_input(pt), offset))
    elif action == "decrypt":
        offset = int(argv[2])
        ct = " ".join(argv[3:])
        print(decrypt_ct(read_stream_if_empty_input(ct), offset))
