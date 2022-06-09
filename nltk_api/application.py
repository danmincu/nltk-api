from flask import Flask, request, render_template

from nltk_api.definition.response import DefinitionResponseBuilder
from nltk_api.lemma.processor import POS
from werkzeug.exceptions import BadRequest

from nltk_api.definition.processor import DefinitionProcessor
from nltk_api.tokenize.response import TokenizeResponseBuilder
from nltk_api.tokenize.sentence import tokenize_sentences
from nltk_api.util.responses import BadRequestIncorrectPos
from nltk_api.util.response_wrappers import json_response_with_time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('layout.html')


@app.route('/definition/<string:word>')
@app.route('/definition/<string:word>/<string:pos>')
@json_response_with_time
def definitions(word, pos=None):
    if pos is not None and pos not in POS:
        return BadRequestIncorrectPos()

    processor = DefinitionProcessor()
    results = processor.look_up(word, pos, similar=False)
    builder = DefinitionResponseBuilder(word, results, pos)

    return builder.build()


@app.route('/similar/<string:word>')
@app.route('/similar/<string:word>/<string:pos>')
@json_response_with_time
def similar(word, pos=None):
    if pos is not None and pos not in POS:
        return BadRequestIncorrectPos()

    processor = DefinitionProcessor()
    results = processor.look_up(word, pos, similar=True)
    builder = DefinitionResponseBuilder(word, results, pos)

    return builder.build()


@app.route('/lemma', methods=['POST'])
@json_response_with_time
def lemmas():
    from nltk_api.lemma.response import LemmaResponseBuilder
    from nltk_api.lemma.processor import LemmaProcessor, assert_correct_format

    payload = request.get_json()
    for query in payload:
        try:
            assert_correct_format(query)
        except (TypeError, KeyError):
            return BadRequest("Incorrect format of query.")
    builder = LemmaResponseBuilder()
    processor = LemmaProcessor()

    for entry in payload:
        if entry["partOfSpeech"] != "all":
            builder.add_entry(entry["word"], processor.lemma(entry["word"], entry["partOfSpeech"]))
        elif entry["partOfSpeech"] == "all":
            builder.add_entry(entry["word"], processor.all_lemma(entry["word"]))
        else:
            continue
    builder.add_query(payload)
    return builder.build()


@app.route('/tagger', methods=['POST'])
@json_response_with_time
def tagger():
    payload = request.get_json()
    if not all(isinstance(entry, str) for entry in payload):
        return BadRequest("Incorrect format of entered data. Expects JSON array with strings.")
    from nltk_api.tag.sentence import tag_sentences
    from nltk_api.tag.response import TaggerResponseBuilder
    remove_stops = request.args.get('remove_stops', None) is not None
    show_symbols = request.args.get('symbols', None) is not None
    result = tag_sentences(payload, remove_stops, show_symbols)
    builder = TaggerResponseBuilder(payload, result)

    return builder.build()

@app.route('/tokenizer', methods=['POST'])
@json_response_with_time
def tokenizer():
    payload = request.get_json()
    if not all(isinstance(entry, str) for entry in payload):
        return BadRequest("Incorrect format of entered data. Expects JSON array with strings.")
    from nltk_api.tag.sentence import tag_sentences
    from nltk_api.tag.response import TaggerResponseBuilder
    remove_stops = request.args.get('remove_stops', None) is not None
    symbols = request.args.get('symbols', None) is not None
    result = tokenize_sentences(payload, remove_stops, symbols)
    builder = TokenizeResponseBuilder(payload, result)

    return builder.build()


@app.route('/doc/definition', methods=['GET'])
def doc_definition():
    return render_template('definition.html')


@app.route('/doc/lemmatization', methods=['GET'])
def doc_lemmatization():
    return render_template('lemma.html')


@app.route('/doc/tagger', methods=['GET'])
def doc_tagger():
    return render_template('tagger.html')


@app.route('/doc/similar', methods=['GET'])
def doc_similar():
    return render_template('similar.html')


@app.route('/credits', methods=['GET'])
def about():
    return render_template('about.html')
