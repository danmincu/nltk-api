class DefinitionResponseBuilder(object):
    def __init__(self, word, result_set, pos=None):
        mapped_collection = list(map(lambda el: {
            'definition': el['definition'].capitalize(),
            'result': el['word'].word(),
            'lexname': el['lexname'] if 'lexname' in el else None,
            'rawname': el['rawname'],
            'partOfSpeech': el['word'].part_of_speech(),
            'function': el['function'] if 'function' in el else None
        }, result_set))

        self._output = {
            'word': word.replace('_', ' '),
            'results': mapped_collection,
        }
        if pos is not None:
            self._output['partOfSpeech'] = pos

    def build(self):
        return self._output
