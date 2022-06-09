from nltk import pos_tag_sents as tagger
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords

POS_TAGS = {
    '$': 'dollar',
    "''": 'quote_close',
    '(': 'parenthesis_open',
    ')': 'parenthesis_close',
    ',': 'comma',
    '--': 'dash',
    '.': 'terminator',
    ':': 'colon_ellipsis',
    'CC': 'conj_coordinating',
    'CD': 'numeral_cardinal',
    'DT': 'determiner',
    'EX': 'existential_there',
    'FW': 'foreign word',
    'IN': 'prep_or_conj_subordinating',
    'JJ': 'adj_or_numeral_ordinal',
    'JJR': 'adj_comparative',
    'JJS': 'adj_superlative',
    'LS': 'list_item_marker',
    'MD': 'modal_aux',
    'NN': 'noun_comm_sing_or_mass',
    'NNP': 'noun_proper_sing',
    'NNPS': 'noun_proper_pl',
    'NNS': 'noun_comm_pl',
    'PDT': 'pre-determiner',
    'POS': 'genitive_marker',
    'PRP': 'pronoun_personal',
    'PRP$': 'pronoun_possessive',
    'RB': 'adverb',
    'RBR': 'adverb_comparative',
    'RBS': 'adverb_superlative',
    'RP': 'particle',
    'SYM': 'symbol',
    'TO': 'to_infi_pre',
    'UH': 'interjection',
    'VB': 'verb_base',
    'VBD': 'verb_past',
    'VBG': 'verb_present',
    'VBN': 'verb_past_parti',
    'VBP': 'verb_present_not_3rd_person',
    'VBZ': 'verb_present_3rd_person',
    'WDT': 'wh-determiner',
    'WP': 'wh-pronoun',
    'WP$': 'wh-pronoun_possessive',
    'WRB': 'wh-adverb',
    '``': 'quote_open'
}
_IDX_WORD, _IDX_SYMBOL = 0, 1


def tokenize_sentences(sentences, remove_stops=False):
    tokenized = []
    stop_words = set(stopwords.words('english'))

    for sent in sentences:
        sentences = sent_tokenize(sent)
        for prop in sentences:
            if remove_stops:
                tokenized.append([prop, [w for w in word_tokenize(prop) if not w.lower() in stop_words]])
            else:
                tokenized.append([prop, word_tokenize(prop)])

    print(tokenized)

    return tokenized
