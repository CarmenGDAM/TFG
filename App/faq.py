from sentence_transformers import SentenceTransformer
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score
import os

model_binary_name = "faq.json"
mapping_file_name = "inverseIntValues.json"
csv_file_name = "faq.csv"

# Definir los modelos que vamos a usar (xgboost para el clasificador y sentencetransformer para el embedding)
model = xgb.XGBClassifier()
embed = SentenceTransformer('hiiamsid/sentence_similarity_spanish_es')

# Variable global para almacenar el mapeo de valores numéricos a respuestas
inverseIntValues = {}

if not os.path.exists(model_binary_name):
    df = pd.read_csv(csv_file_name, delimiter=";")

    sentences = df['pregunta'].tolist()

    # Obtener los valores únicos de la columna
    targets = df['respuesta'].unique()

    # Crear un diccionario que mapee cada valor único a un número
    intValues = {valor: indice for indice, valor in enumerate(targets)}
    inverseIntValues = {indice: valor for valor, indice in intValues.items()}

    # Crear la nueva columna asignando los valores numéricos
    df['target'] = df['respuesta'].map(intValues)

    embeddings = embed.encode(sentences)

    # Calcular los embeddings que van a servir como características
    df_embeddings = pd.DataFrame(embeddings)
    print(df_embeddings.head())

    # Separar características (X) y columna objetivo (y)
    X = df_embeddings  # características
    y = df['target']  # columna objetivo

    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar el modelo
    model.fit(X_train, y_train)

    # Hacer predicciones en los datos de prueba
    y_pred = model.predict(X_test)

    # Evaluar el modelo
    accuracy = accuracy_score(y_test, y_pred)
    print("Precisión del modelo:", accuracy)

    # Salvar el modelo y el mapeo
    model.save_model(model_binary_name)
    pd.Series(inverseIntValues).to_json(mapping_file_name)

else:
    model.load_model(model_binary_name)
    inverseIntValues = pd.read_json(mapping_file_name, typ='series').to_dict()
    print("model loaded")


def response(question):
    # Codificar la pregunta usando el modelo de embeddings
    question_embedding = embed.encode([question])
    
    # Predecir la respuesta usando el modelo XGBoost
    response_index = model.predict(question_embedding)
    
    # Obtener la respuesta correspondiente al índice predicho
    response_text = inverseIntValues.get(response_index[0], "Lo siento no tengo la información suficiente para poder responderte.")
    return response_text



