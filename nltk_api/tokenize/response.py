class TokenizeResponseBuilder(object):
    def __init__(self, input_elements, result_set):
        self._outputCollection = []
        self._outputRoot = {'input': input_elements}
        self._prepare_result_items(result_set)

    def build(self):
        self._outputRoot['results'] = self._outputCollection
        return self._outputRoot

    def _create_item(self, word, pos):
        return {'sentence': word, 'words': pos}

    def _prepare_result_items(self, result_set):
        print(result_set)
        for sentence_collection in result_set:
            sentence_processed = [self._create_item(sentence_collection[0], sentence_collection[1])]
            self._outputCollection.append(sentence_processed)
