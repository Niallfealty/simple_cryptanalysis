""" encrypt/decrypt with vignere cipher
"""

from caesar import build_lookup, ALEPH

class Vignere:
    """ Tool for encryption of data with a vignere cipher

        we keep the key in the object and expose encrypt/decrypt function
    """
    CHARS = ALEPH # nick this to at least keep errors consistent!

    def __init__(self, key):
        self.key = key
        self._get_offsets_from_key() # this is for actual use
        self._construct_lookups()

    def _get_offsets_from_key(self):
        ''' Use the alphabet to compute offsets from the key
        '''
        # set the offsets so we only do this once, add 1 for offset
        self._offsets = [self.CHARS.find(k) + 1 for k in self.key]
        return
        
    def _construct_lookups(self):
        ''' memoize the lookups
        '''
        self.lookup = {o: build_lookup(o, alphabet=self.CHARS) for o in self._offsets}

    def _encrypt_word(self, pt_word):
        ''' encrypt pt with key
        '''
        encrypted_array = []
        for i, char in enumerate(pt_word):
            encrypted_array.append(
                    self.lookup[
                            self._offsets[i % len(self._offsets)]
                        ][char]
                ) 

        return "".join(encrypted_array)
