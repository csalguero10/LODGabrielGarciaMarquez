from collections import Counter
import string
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk import ngrams
from nltk import BigramAssocMeasures, BigramCollocationFinder
from nltk.text import Text 
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np 
import sys

# Redirigir la salida a un archivo
output_file = "text_analysis/final_analysis.txt"
sys.stdout = open(output_file, "w", encoding="utf-8")

# Descargar stopwords en español (solo la primera vez)
nltk.download('stopwords')
nltk.download('punkt')

# Crear conjuntos de puntuación y stopwords en español
stop_words = set(stopwords.words('spanish')) 
excluded_punct = set(string.punctuation)

# Abrir el archivo de texto asegurando la codificación correcta
with open("text_analysis/tei.txt", "r", encoding="utf-8") as f:
    orig_text = f.read()

# Convertir a minúsculas
text = orig_text.lower()

# Tokenización
words = word_tokenize(text)
print("Tokens originales:", words[:20])

# Limpiar tokens de puntuación y stopwords
clean_text = [w for w in words if w not in excluded_punct and w not in stop_words]
print("Tokens limpios:", clean_text[:20])

# Frecuencia de palabras con Counter
freq = Counter(clean_text).most_common(20)
print("Frecuencia de palabras:", freq)

# Frecuencia de palabras con FreqDist
fdist1 = FreqDist(clean_text).most_common(20)
print("Frecuencia con FreqDist:", fdist1)

# Obtener bigramas y calcular frecuencia
n_grams = ngrams(clean_text, 2)
fdist3 = FreqDist(n_grams).most_common(20)
print("Bigramas más frecuentes:", fdist3)

# Medidas de colocation para bigramas
bigrams = nltk.collocations.BigramAssocMeasures()

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

# Concordancia
tokens_to_be_analysed = Text(words)
tokens_to_be_analysed.concordance("militar", 40, 20)

# TF-IDF
texts = [t for t in text.split('\n\n') if t and len(t) > 1]
print(f"Número de textos en el corpus: {len(texts)}")

# Inicializar TF-IDF
tfidf = TfidfVectorizer(analyzer='word', sublinear_tf=True, max_features=500, tokenizer=word_tokenize)
tdidf = tfidf.fit(texts)

# Obtener términos con mayor IDF
inds = np.argsort(tfidf.idf_)[::-1][:10]
top_IDF_tokens = [list(tfidf.vocabulary_)[ind] for ind in inds]
print("Términos con mayor IDF:", top_IDF_tokens)

# Cerrar el archivo de salida
sys.stdout.close()
