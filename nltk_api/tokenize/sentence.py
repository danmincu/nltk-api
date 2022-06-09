from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords

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
    return tokenized
