#!/usr/bin/env python3
""" frequency counting code
"""

from collections import Counter
from numpy import log, array, roll

from encryption import ALEPH, decrypt_ct

EPSILON = 0.5

def compute_p(text_string, chars, prior=EPSILON):
    ''' compute the prob dist of chars from data
    '''
    frequencies = {}
    counts = Counter(text_string)
    for char in chars:
        charcount = counts[char]
        frequencies[char] = charcount if charcount > 0 else prior

    total_count = sum(frequencies.values())

    for char in chars:
        frequencies[char] = frequencies[char]/total_count

    return frequencies

def get_sorted_values(p_dict):
    ''' from a p_dict make a sorted numpy array sorted by key
    '''
    return [p_dict[k] for k in sorted(p_dict.keys())]

### don't need to do this
def computeps_ps_for_offsets(text_string, chars, prior=EPSILON):
    ''' compute p's for all offsets
    '''
    p_at_offsets = {}
    for offset in range(1,len(chars)):
        p_at_offsets[str(offset)] = compute_p(ct_string, chars, prior)


def compute_kl_divergence(dist1, dist2):
    ''' compute the kl-divergence from dist1 to dist2 '''
    return sum(dist1*log(dist1/dist2))

def find_all_divergences(p_ct, p_data):
    """ compute all the divergences
    """
    divergences = {}
    for offset in range(1, len(p_ct)):
        divergences[str(offset)] = compute_kl_divergence(
                roll(p_ct, offset),
                p_data
            )

    return divergences

def run_analysis(ct, data):
    ''' run the analysis
    '''
    p_data = compute_p(data, chars=ALEPH)
    p_ct = compute_p(ct, chars=ALEPH)

    kl_divs = find_all_divergences(
            get_sorted_values(p_data),
            get_sorted_values(p_ct)
        )

    return kl_divs

def print_l2h(kl_divs_dict):
    sorted_keys = sorted(kl_divs_dict.keys(), key=lambda k: kl_divs_dict[k])
    for k in sorted_keys:
        v = kl_divs_dict[k]
        print(f"=> Shift {k} - Kl divergence: {v:.4}")


def main():
    from sys import argv, stdin
    datapath = argv[1]
    with open(datapath, "r") as fp:
        dataset = fp.read()
        
    if len(argv) == 2:
        ct = stdin.read()
    elif len(argv) == 3:
        with open(argv[2], "r") as fp:
            ct = fp.read()
    else:
        raise ValueError("[!!!!] ciphertext must be provided!!!")

    print_l2h(run_analysis(ct, dataset))

if __name__ == "__main__":
    main()
