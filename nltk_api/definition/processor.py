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

    def hypernym_look_up(self, word, pos=None, exclusive=True):
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

        if exclusive:
            output = list(filter(lambda item: item['word'].raw_word() != word, output))

        return output

    def hyponym_look_up(self, word, pos=None, exclusive=True):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        if pos is None:
            for synset in synsets:
                for hyponym in synset.hyponyms():
                    print(synset.pos(), hyponym)
                    output.append(self._prepare_entry(synset.definition(), ProcessedWord(hyponym.name())))
        else:
            for synset in synsets:
                for hyponym in synset.hyponyms():
                    processed_word = ProcessedWord(hyponym.name())
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_entry(synset.definition(), processed_word))

        if exclusive:
            output = list(filter(lambda item: item['word'].raw_word() != word, output))

        return output


    def _prepare_entry(self, definition, processed_word):
        return {'definition': definition, 'word': processed_word}