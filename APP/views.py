from django.views import View

import nltk

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk import SnowballStemmer
from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer

from django.shortcuts import render
from django.http import HttpResponse

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

stopwords.words('english')


def normalize(text):
    lexical_tokens = word_tokenize(text)
    return lexical_tokens


def cleanner(tokens):
    clean_tokens = tokens[:]

    sr = stopwords.words('english')

    for token in tokens:
        if token in sr:
            clean_tokens.remove(token)
    return clean_tokens


def tokensToString(tokens):
    str = ""
    for token in tokens:
        str += token
        str += " "
    return str


class Index(View):
    template_name = "index.html"
    spanishStemmer = SnowballStemmer('spanish')
    porter = PorterStemmer()
    lancaster = LancasterStemmer()
    lemmatizer = WordNetLemmatizer()
    context = {}

    def post(self, request):
        text = request.POST.get('my_textarea')
        self.context['txt'] = text
        tokens = normalize(text)
        # print(cleanner(tokens))
        if 'stm' in request.POST:
            stems = [self.porter.stem(token) for token in tokens]
            self.context['answer'] = tokensToString(stems)
            # print(stems)
        elif 'lmt' in request.POST:
            lems = [self.lemmatizer.lemmatize(token, pos='v') for token in tokens]
            self.context['answer'] = tokensToString(lems)
            # print(lems)
        return render(request, self.template_name, self.context)

    def get(self, request):
        return render(request, self.template_name)


