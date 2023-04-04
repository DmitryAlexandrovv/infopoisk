# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pymorphy2
import operator
from numpy import dot
from numpy.dual import norm
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup

def calc_cos_similarity(query_tf_idf_vector, document_tf_idf_vector):
    query_vector = list(query_tf_idf_vector.values())
    movie_vector = list(document_tf_idf_vector.values())

    if norm(query_vector) == 0 or norm(movie_vector) == 0:
        return 0

    return dot(query_vector, movie_vector) / (norm(query_vector) * norm(movie_vector))

def searchQuery(query):
    query_words = []
    for word in query.split():
        query_words.append(morph_analyzer.parse(word)[0].normal_form)
    unique_query_words= set(query_words)

    query_tf_vector = {}

    for term in unique_query_words:
        word_count_in_query = len([x for x in query_words if x == term])
        query_tf_vector.update({term: {'tf': word_count_in_query / len(query_words)}})

    result = {}

    for i, lines in lemmas_tf_idf_vector.items():
        document_tf_idf_vector = {}
        query_tf_idf_vector = {}
        query_terms = []

        for line in lines:
            line_data = line.split()
            term = line_data[0]
            idf = line_data[1]
            tf_idf = line_data[2]

            if term in unique_query_words:
                query_terms.append(term)
                query_tf_idf_vector[term] = query_tf_vector.get(term).get('tf') * float(idf)
                document_tf_idf_vector[term] = float(tf_idf)

        for term in unique_query_words:
            if term not in query_terms:
                query_tf_idf_vector[term] = 1
                document_tf_idf_vector[term] = 0

        cos_sim = calc_cos_similarity(query_tf_idf_vector, document_tf_idf_vector)
        if cos_sim != 0:
            result[i] = cos_sim

    sorted_result = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    
    res = []
    for item in sorted_result:
        line = []
        text = pages.get(item[0])

        soup = BeautifulSoup(text, 'html.parser')

        line.append(item[0])
        line.append(soup.title.get_text())
        res.append(line)

    return res

app = Flask(__name__)

morph_analyzer = pymorphy2.MorphAnalyzer()
lemmas_tf_idf_vector = {}

k = 100
for i in range(0, k):
    with open('./dataset/lemmas_tf_idf/page-' + str(i) + '.txt', 'r', encoding='utf-8') as file:
        lemmas_tf_idf_vector[i] = file.readlines()

pages = {}
for i in range(0, k):
    with open('./templates/page' + str(i) + '.html', 'r', encoding='utf-8') as file:
        pages.update({i: file.read()})

CORS(app)

@app.route("/", methods = ['GET'])
def root():
    return jsonify(['Hello world'])

@app.route("/search", methods = ['POST'])
def find():
    query = request.json.get('query')
    data = searchQuery(query)
    return jsonify(data)

@app.route("/page", methods = ['GET'])
def page():
    page = request.args.get('page', type = int)
    return render_template('page' + str(page) + '.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
