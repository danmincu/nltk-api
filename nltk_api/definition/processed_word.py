from nltk.corpus.reader.wordnet import NOUN, VERB, ADJ, ADJ_SAT, ADV

IDX_WORD, IDX_POS, IDX_SEQ = 0, 1, 2

REVERSE_POS = {
    NOUN: 'noun',
    VERB: 'verb',
    ADJ: 'adjective',
    ADJ_SAT: 'adjective',
    ADV: 'adverb',
}


class ProcessedWord(object):
    def __init__(self, sysnet_word, sysnet=None, original_synset=None):
        if not isinstance(sysnet_word, str):
            raise TypeError('Constructor expects string argument.')

        tokens = sysnet_word.split('.')

        if not len(tokens) == 3:
            raise ValueError('The word should contain two dots separating meta information <lemma>.<pos>.<number>')

        self._word_raw = tokens[IDX_WORD]
        self._pos_raw = tokens[IDX_POS]
        self._index = int(tokens[IDX_SEQ])

        self._normalized_word = self._word_raw.replace("_", " ")
        self._pos = REVERSE_POS.get(self._pos_raw)
        self._original_word = sysnet_word
        self._original_sysnet = original_synset
        self._sysnet = sysnet

    def raw_word(self):
        return self._word_raw

    def word(self):
        """
        Return human readable representation of the word
        :return:
        """
        if self._sysnet:
            return {"clean_name": self._normalized_word,
                    "synset_name": self._original_word,
                    "lexname": self._sysnet.lexname(),
                    "definition": self._sysnet.definition(),
                    "lemmas": list(map(lambda item: {'lemma': item.name().replace('_', ' '), 'frame_strings': item.frame_strings()}, self._sysnet.lemmas())),
                    "synset_vectors": {
                        "examples": self._sysnet.examples(),
                        "hyponyms": list(map(lambda item: {'hyponym': self.normalized_word(item.name()), 'raw': item.name(),'definition': item.definition()}, self._sysnet.hyponyms())),
                        "hypernyms": list(map(lambda item: {'hypernym': self.normalized_word(item.name()), 'raw': item.name(),'definition': item.definition()}, self._sysnet.hypernyms())),
                        "part_holonyms": list(map(lambda item: {'holonym': self.normalized_word(item.name()), 'raw': item.name(),'definition': item.definition()}, self._sysnet.part_holonyms())),
                        "substance_holonyms": list(map(lambda item: {'holonym': self.normalized_word(item.name()), 'raw': item.name(),'definition': item.definition()}, self._sysnet.substance_holonyms())),
                        "part_meronyms": list(map(lambda item: {'meronym': self.normalized_word(item.name()), 'raw': item.name(),'definition': item.definition()}, self._sysnet.part_meronyms())),
                        "substance_meronyms": list(map(lambda item: {'meronym': self.normalized_word(item.name()), 'raw': item.name(), 'definition': item.definition()}, self._sysnet.substance_meronyms())),
                        "topic_domains": list(map(lambda item: {'domains': self.normalized_word(item.name()), 'raw': item.name(),'definition': item.definition()}, self._sysnet.topic_domains())),
                        "usage_domains": list(map(lambda item: {'domains': self.normalized_word(item.name()), 'raw': item.name(),'definition': item.definition()}, self._sysnet.usage_domains())),
                        "verb_groups": list(map(lambda item: {'verbgroup': self.normalized_word(item.name()), 'raw': item.name(),'definition': item.definition()}, self._sysnet.verb_groups())),
                        "entailments": list(map(lambda item: {'entailment': self.normalized_word(item.name()), 'raw': item.name(),'definition': item.definition()}, self._sysnet.entailments())),
                        "attributes": list(map(lambda item: {'attribute': self.normalized_word(item.name()), 'raw': item.name(),'definition': item.definition()}, self._sysnet.attributes()))}}
        else:
            return {"clean_name": self._normalized_word, "rawname": self._original_word}

    def normalized_word(self, synset_word):
        tokens = synset_word.split('.')
        if not len(tokens) == 3:
            raise ValueError('The word should contain two dots separating meta information <lemma>.<pos>.<number>')
        return tokens[IDX_WORD].replace("_", " ")

    def part_of_speech(self):
        return self._pos

    def lemma_names(self):
        if self._original_sysnet:
            return self._original_sysnet.lemma_names()
        else:
            return []

    def raw_part_of_speech(self):
        return self._pos_raw

    def word_index(self):
        return self._index

    def is_part_of_speech(self, pos):
        if isinstance(pos, str) and len(pos) == 1:
            return self._pos_raw == pos

        if isinstance(pos, str):
            return self._pos == pos

        raise TypeError("Cannot check part of speech with provided argument.")

    def __str__(self):
        return "Word: %s, part of speech: %s".format(self._normalized_word, self._pos)
