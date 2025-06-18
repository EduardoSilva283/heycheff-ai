import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Exemplo de dataset de ingredientes rotulados
# Em produção, use um dataset maior e real
DATA = [
    {"ingrediente": "trigo", "alergenico": 1},
    {"ingrediente": "farinha de trigo", "alergenico": 1},
    {"ingrediente": "cevada", "alergenico": 1},
    {"ingrediente": "gluten", "alergenico": 1},
    {"ingrediente": "açúcar", "alergenico": 0},
    {"ingrediente": "arroz", "alergenico": 0},
    {"ingrediente": "farinha de arroz", "alergenico": 0},
    {"ingrediente": "polvilho", "alergenico": 0},
    {"ingrediente": "xilitol", "alergenico": 0},
    {"ingrediente": "stevia", "alergenico": 0},
]

def train_allergen_classifier():
    df = pd.DataFrame(DATA)
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    X = model.encode(df['ingrediente'].tolist())
    y = df['alergenico']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred))
    return clf, model

# Exemplo de uso:
# clf, bert_model = train_allergen_classifier()
# pred = clf.predict(bert_model.encode(["farinha de trigo"]))
# print(pred)  # 1 = alergênico, 0 = seguro
