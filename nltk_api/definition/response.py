class DefinitionResponseBuilder(object):
    def __init__(self, word, result_set, pos=None, function=None):
        mapped_collection = list(map(lambda el: {
            'input': {'definition': el['definition'].capitalize(),
                'lexname': el['lexname'] if 'lexname' in el else None,
                'synset_name': el['rawname'],
                'clean_name': word,
                'partOfSpeech': el['word'].part_of_speech(),
                'lemmas': el['word'].lemma_names()},
            'output': el['word'].word(),
            'function_variant': el['subfunction'] if 'subfunction' in el else None
        }, result_set))

        # remove the "subfunction":None entries
        list(filter(lambda el: el.pop('function_variant'), list(filter(lambda el: el['function_variant'] == None, mapped_collection))))

        self._output = {
            'function_input': word.replace('_', ' '),
            'input_variants': mapped_collection,
            'function': function
        }
        if pos is not None:
            self._output['partOfSpeech'] = pos

    def build(self):
        return self._output
