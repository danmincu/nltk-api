from nltk.corpus import wordnet
from nltk_api.definition.processed_word import ProcessedWord
from nltk_api.lemma.processor import POS


class DefinitionProcessor(object):
    def __init__(self):
        pass

    def look_up(self, word, pos=None, similar=True):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        if pos is None:
            for synset in synsets:
                output.append(self._prepare_entry(synset.definition(), ProcessedWord(synset.name())))
        else:
            for synset in synsets:
                processed_word = ProcessedWord(synset.name())
                if processed_word.is_part_of_speech(pos):
                    output.append(self._prepare_entry(synset.definition(), processed_word))

        if not similar:
            output = list(filter(lambda item: item['word'].raw_word() == word, output))

        return output

    def uber_look_up(self, word, pos=None, exclusive=True):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        if pos is None:
            for synset in synsets:
                for lemma in synset.lemmas():
                    output.append(self._prepare_entry(synset.definition(), ProcessedWord(lemma.name()+f".{synset.pos()}.01")))
        else:
            for synset in synsets:
                for lemma in synset.lemmas():
                    processed_word = ProcessedWord(lemma.name()+f".{synset.pos()}.01")
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_entry(synset.definition(), processed_word))

        if exclusive:
            output = list(filter(lambda item: item['word'].raw_word() != word, output))

        return output

    def hypernym_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        if pos is None:
            for synset in synsets:
                for hypenym in synset.hypernyms():
                    output.append(self._prepare_entry(synset.definition(), ProcessedWord(hypenym.name())))
        else:
            for synset in synsets:
                for hypenym in synset.hypernyms():
                    processed_word = ProcessedWord(hypenym.name())
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_entry(synset.definition(), processed_word))

        return output

    def hyponym_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        if pos is None:
            for synset in synsets:
                for hyponym in synset.hyponyms():
                    output.append(self._prepare_entry_f(synset.definition(), ProcessedWord(hyponym.name()), 'hyponym'))
        else:
            for synset in synsets:
                for hyponym in synset.hyponyms():
                    processed_word = ProcessedWord(hyponym.name())
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_entry_f(synset.definition(), processed_word, 'hyponym'))
        return output

    def entailment_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        for synset in synsets:
            for entailment in synset.entailments():
                processed_word = ProcessedWord(entailment.name())
                if processed_word.is_part_of_speech('verb'):
                    output.append(self._prepare_entry_f(synset.definition(), processed_word, 'entailment'))
        return output


    def troponym_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        for synset in synsets:
            for hyponym in synset.hyponyms():
                processed_word = ProcessedWord(hyponym.name())
                if processed_word.is_part_of_speech('verb'):
                    output.append(self._prepare_entry_f(synset.definition(), processed_word, 'troponym'))
        return output

    def meronym_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        if pos is None:
            for synset in synsets:
                for meronym in synset.part_meronyms():
                    output.append(self._prepare_entry_f(synset.definition(), ProcessedWord(meronym.name()), 'part_meronym'))
                for meronym in synset.substance_meronyms():
                    output.append(self._prepare_entry_f(synset.definition(), ProcessedWord(meronym.name()), 'substance_meronym'))

        else:
            for synset in synsets:
                for meronym in synset.part_meronyms():
                    processed_word = ProcessedWord(meronym.name())
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_entry_f(synset.definition(), processed_word, 'part_meronym'))
                for meronym in synset.substance_meronyms():
                    processed_word = ProcessedWord(meronym.name())
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_entry_f(synset.definition(), processed_word, 'substance_meronym'))
        return output


    def holonym_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        if pos is None:
            for synset in synsets:
                for holonym in synset.part_holonyms():
                    output.append(self._prepare_entry_f(synset.definition(), ProcessedWord(holonym.name()), 'part_holonym'))
                for holonym in synset.substance_holonyms():
                    output.append(self._prepare_entry_f(synset.definition(), ProcessedWord(holonym.name()), 'substance_holonym'))

        else:
            for synset in synsets:
                for holonym in synset.part_holonyms():
                    processed_word = ProcessedWord(holonym.name())
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_entry_f(synset.definition(), processed_word, 'part_holohym'))
                for holonym in synset.substance_holonyms():
                    processed_word = ProcessedWord(holonym.name())
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_entry_f(synset.definition(), processed_word, 'substance_holonym'))
        return output

    def topicdomains_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        if pos is None:
            for synset in synsets:
                for topicd in synset.topic_domains():
                    output.append(self._prepare_entry(synset.definition(), ProcessedWord(topicd.name())))
        else:
            for synset in synsets:
                for topicd in synset.topic_domains():
                    processed_word = ProcessedWord(topicd.name())
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_entry(synset.definition(), processed_word))

        return output

    def usagedomains_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        if pos is None:
            for synset in synsets:
                for usaged in synset.usage_domains():
                    output.append(self._prepare_entry(synset.definition(), ProcessedWord(usaged.name())))
        else:
            for synset in synsets:
                for usaged in synset.usage_domains():
                    processed_word = ProcessedWord(usaged.name())
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_entry(synset.definition(), processed_word))

        return output


    def _prepare_entry(self, definition, processed_word):
        return {'definition': definition, 'word': processed_word}

    def _prepare_entry_f(self, definition, processed_word, function):
        return {'definition': definition, 'word': processed_word, 'function': function}