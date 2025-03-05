import spacy #this library is used for natural language processing and is useful when we have texts in spanish, it is a good alternative to nltk
import string
import sys
from collections import Counter
from nltk import FreqDist, ngrams
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Redirigir la salida a un archivo
output_file = "text_analysis/final_analysis.txt"
sys.stdout = open(output_file, "w", encoding="utf-8")

# Cargar modelo en español de spaCy
nlp = spacy.load("es_core_news_sm")

# Abrir el archivo de texto asegurando la codificación correcta
with open("text_analysis/tei.txt", "r", encoding="utf-8") as f:
    orig_text = f.read()

# Procesar el texto con spaCy
doc = nlp(orig_text.lower())

# Crear conjuntos de puntuación y stopwords en español
excluded_punct = set(string.punctuation)
stop_words = nlp.Defaults.stop_words

# Tokenización, lematización y limpieza de stopwords y puntuación
clean_text = [token.lemma_ for token in doc if token.text not in excluded_punct and token.text.lower() not in stop_words and not token.is_space]

print("Tokens limpios:", clean_text[:30])

# Frecuencia de palabras con Counter
freq = Counter(clean_text).most_common(30)
print("Frecuencia de palabras:", freq)

# Frecuencia de palabras con FreqDist
fdist1 = FreqDist(clean_text).most_common(30)
print("Frecuencia con FreqDist:", fdist1)

# Obtener bigramas y calcular frecuencia
n_grams = list(ngrams(clean_text, 2))
fdist3 = FreqDist(n_grams).most_common(20)
print("Bigramas más frecuentes:", fdist3)

# Medidas de colocation para bigramas
bigrams = BigramAssocMeasures()

# Encontrar bigramas en el corpus
finder = BigramCollocationFinder.from_words(clean_text)
finder.apply_freq_filter(3)

# Calcular Chi-cuadrado
print("Bigrams Chi-squared:")
scored_chi = finder.score_ngrams(bigrams.chi_sq)
for bigram, score in scored_chi[:5]:
    print(bigram, score)

print(finder.nbest(bigrams.chi_sq, 10))

# Calcular PMI
print("Bigrams PMI:")
scored_pmi = finder.score_ngrams(bigrams.pmi)
for bigram, score in scored_pmi[:5]:
    print(bigram, score)

print(finder.nbest(bigrams.pmi, 10))

# Concordancia: Buscar palabra específica en contexto
search_word = "ojeras"
print(f"Concordancia para '{search_word}':")
for sent in doc.sents:
    if search_word in sent.text:
        print(sent.text)

# TF-IDF: Dividir el texto en fragmentos separados por doble salto de línea
texts = [t for t in orig_text.split('\n\n') if t and len(t) > 1]
print(f"Número de textos en el corpus: {len(texts)}")

# Inicializar TF-IDF
tfidf = TfidfVectorizer(analyzer='word', sublinear_tf=True, max_features=500, tokenizer=lambda text: [token.lemma_ for token in nlp(text) if token.text not in stop_words])
tdidf = tfidf.fit(texts)

# Obtener términos con mayor IDF
inds = np.argsort(tfidf.idf_)[::-1][:10]
top_IDF_tokens = [list(tfidf.vocabulary_)[ind] for ind in inds]
print("Términos con mayor IDF:", top_IDF_tokens)

# Cerrar el archivo de salida
sys.stdout.close()
