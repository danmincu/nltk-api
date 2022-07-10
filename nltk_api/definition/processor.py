from nltk.corpus import wordnet
from nltk_api.definition.processed_word import ProcessedWord
from nltk_api.lemma.processor import POS
from nltk.corpus import wordnet_ic as wnic

class DefinitionProcessor(object):
    def __init__(self):
        pass

    # higher score = more similar
    def similarity(self, word1, word2, algorithm=None):

        synset1 = wordnet.synset(word1)
        synset2 = wordnet.synset(word2)
        if algorithm is not None:
            algorithm = algorithm.lower()
        if algorithm == "wup":
            return synset2.wup_similarity(synset1)
        else:
            if algorithm == "lch":
                return synset2.lch_similarity(synset1)
            else:
                # this one is the exception >> lower score = more similar
                if algorithm == "res":
                    return synset2.res_similarity(synset1, wnic.ic('ic-bnc-resnik-add1.dat'))
                else:
                    if algorithm == "lin":
                        return synset2.lin_similarity(synset1, wnic.ic('ic-bnc-add1.dat'))
                    else:
                        if algorithm == "jcn":
                            return synset2.jcn_similarity(synset1, wnic.ic('ic-bnc-add1.dat'))
                        else:
                            return synset2.path_similarity(synset1)

    def look_up(self, word, pos=None, similar=True):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        if pos is None:
            for synset in synsets:
                output.append(self._prepare_synset_entry(synset, ProcessedWord(synset.name(), synset, synset)))
        else:
            for synset in synsets:
                processed_word = ProcessedWord(synset.name(), synset, synset)
                if processed_word.is_part_of_speech(pos):
                    output.append(self._prepare_synset_entry(synset, processed_word))

        if not similar:
            output = list(filter(lambda item: item['word'].raw_word() == word, output))

        return output

    def similar_look_up(self, word, pos=None, exclusive=True):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        if pos is None:
            for synset in synsets:
                for lemma in synset.lemmas():
                    output.append(self._prepare_synset_entry(synset, ProcessedWord(lemma.name()+f".{synset.pos()}.01", None, synset)))
        else:
            for synset in synsets:
                for lemma in synset.lemmas():
                    processed_word = ProcessedWord(lemma.name()+f".{synset.pos()}.01", None, synset)
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_synset_entry(synset, processed_word))

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
                for hypernym in synset.hypernyms():
                    output.append(self._prepare_synset_entry(synset, ProcessedWord(hypernym.name(), hypernym, synset)))
        else:
            for synset in synsets:
                for hypernym in synset.hypernyms():
                    processed_word = ProcessedWord(hypernym.name(), hypernym)
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_synset_entry(synset, processed_word))

        return output

    def hyponym_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        if pos is None:
            for synset in synsets:
                for hyponym in synset.hyponyms():
                    output.append(self._prepare_synset_entry(synset, ProcessedWord(hyponym.name(), hyponym, synset)))
        else:
            for synset in synsets:
                for hyponym in synset.hyponyms():
                    processed_word = ProcessedWord(hyponym.name(), hyponym)
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_synset_entry(synset, processed_word))
        return output

    def entailment_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        for synset in synsets:
            for entailment in synset.entailments():
                processed_word = ProcessedWord(entailment.name(), entailment, synset)
                if processed_word.is_part_of_speech('verb'):
                    output.append(self._prepare_synset_entry(synset, processed_word))
        return output

    def verbgroup_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        for synset in synsets:
            for verbgroup in synset.verb_groups():
                processed_word = ProcessedWord(verbgroup.name(), verbgroup, synset)
                if processed_word.is_part_of_speech('verb'):
                    output.append(self._prepare_synset_entry(synset, processed_word))
        return output

    def attribute_look_up(self, word):
        synsets = wordnet.synsets(word, POS.get(None))

        output = []
        for synset in synsets:
            for attribute in synset.attributes():
                processed_word = ProcessedWord(attribute.name(), attribute, synset)
                output.append(self._prepare_synset_entry(synset, processed_word))
        return output

    def troponym_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        for synset in synsets:
            for troponym in synset.hyponyms():
                processed_word = ProcessedWord(troponym.name(), troponym, synset)
                if processed_word.is_part_of_speech('verb'):
                    output.append(self._prepare_synset_entry(synset, processed_word))
        return output

    def meronym_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        if pos is None:
            for synset in synsets:
                for meronym in synset.part_meronyms():
                    output.append(self._prepare_synset_entry(synset, ProcessedWord(meronym.name(), meronym, synset), 'part_meronym'))
                for meronym in synset.substance_meronyms():
                    output.append(self._prepare_synset_entry(synset, ProcessedWord(meronym.name(), meronym, synset), 'substance_meronym'))

        else:
            for synset in synsets:
                for meronym in synset.part_meronyms():
                    processed_word = ProcessedWord(meronym.name(), meronym, synset)
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_synset_entry(synset, processed_word, 'part_meronym'))
                for meronym in synset.substance_meronyms():
                    processed_word = ProcessedWord(meronym.name(), meronym, synset)
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_synset_entry(synset, processed_word, 'substance_meronym'))
        return output


    def holonym_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        if pos is None:
            for synset in synsets:
                for holonym in synset.part_holonyms():
                    output.append(self._prepare_synset_entry(synset, ProcessedWord(holonym.name(), holonym, synset), 'part_holonym'))
                for holonym in synset.substance_holonyms():
                    output.append(self._prepare_synset_entry(synset, ProcessedWord(holonym.name(), holonym, synset), 'substance_holonym'))

        else:
            for synset in synsets:
                for holonym in synset.part_holonyms():
                    processed_word = ProcessedWord(holonym.name(), holonym, synset)
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_synset_entry(synset, processed_word, 'part_holohym'))
                for holonym in synset.substance_holonyms():
                    processed_word = ProcessedWord(holonym.name(), holonym, synset)
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_synset_entry(synset, processed_word, 'substance_holonym'))
        return output

    # e.g. code, software, math etc
    def topicdomains_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))
      # https://stackoverflow.com/questions/13881425/get-wordnets-domain-name-for-the-specified-word
        output = []
        if pos is None:
            for synset in synsets:
                for topicd in synset.topic_domains():
                    output.append(self._prepare_synset_entry(synset, ProcessedWord(topicd.name(), topicd, synset)))
        else:
            for synset in synsets:
                for topicd in synset.topic_domains():
                    processed_word = ProcessedWord(topicd.name(), topicd, synset)
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_synset_entry(synset, processed_word))

        return output

    def usagedomains_look_up(self, word, pos=None):
        if pos not in POS and pos is not None:
            raise ValueError('Passed pos is not recognized.')

        synsets = wordnet.synsets(word, POS.get(pos))

        output = []
        if pos is None:
            for synset in synsets:
                for usaged in synset.usage_domains():
                    output.append(self._prepare_synset_entry(synset, ProcessedWord(usaged.name(), usaged, synset)))
        else:
            for synset in synsets:
                for usaged in synset.usage_domains():
                    processed_word = ProcessedWord(usaged.name(), usaged, synset)
                    if processed_word.is_part_of_speech(pos):
                        output.append(self._prepare_synset_entry(synset, processed_word))

        return output


    def _prepare_synset_entry(self, synset, processed_word, function=None):
        if function is None:
            return {'definition': synset.definition(), 'lexname': synset.lexname(), 'rawname': synset.name(), 'word': processed_word}
        else:
            return {'definition': synset.definition(), 'lexname': synset.lexname(), 'rawname': synset.name(), 'word': processed_word, 'subfunction': function}
