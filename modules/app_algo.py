import pkg_resources
from symspellpy import SymSpell, Verbosity
import pandas as pd
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt"
)
# term_index is the column of the term and count_index is the
# column of the term frequency
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

text_log = ''
def correct_word(text):
    global text_log
    text_log = ''
    words = text.split()
    for idx, i in enumerate(words):
        text_log += f"word: {i}"
        word = symspell(i)
        if word.lower() == words[idx].lower():
            text_log += f'\n\nUnable to find similar words (perhaps it is already correct?): {words[idx]}\n\n'
        else:
            text_log += f'\n\nSimilar word found: {word}\n\n'
            text_log += 15*'-' + '\n'
        words[idx] = word
    
    return (' '.join(words).capitalize()), text_log


def symspell(input_term):
    global text_log
    suggestions = sym_spell.lookup(input_term, Verbosity.ALL, max_edit_distance=2, include_unknown=True, transfer_casing=True)
    # display suggestion term, edit distance, and term frequency
    pd_term = []
    pd_close = []
    pd_count = []
    correct = ''
    for idx, suggestion in enumerate(suggestions):
        if idx == 0:
            correct = suggestion._term
        pd_term.append(suggestion._term)
        pd_close.append(suggestion._distance)
        pd_count.append(suggestion._count)

    df = pd.DataFrame()
    df['term'] = pd_term
    df['distance'] = pd_close
    df['count'] = pd_count
    text_log += f"\n{df}"
    return correct