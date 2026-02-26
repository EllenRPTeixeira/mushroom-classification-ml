# -*- coding: utf-8 -*-
"""
Projeto: Classificação de Cogumelos (Mushroom Classification)
Data Original: 2023 | Refatoração: 2026
Autora: Ellen Ponijaleki
Descrição: Modelo de Machine Learning para identificação de cogumelos venenosos.
Versão: 2.1 (Remoção de dependências externas para máxima compatibilidade)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

def carregar_dados():
    """Carrega o dataset diretamente de uma fonte pública (UCI Repository)."""
    url = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/mushrooms.csv"
    try:
        df = pd.read_csv(url)
        print("✅ Dados carregados com sucesso!")
        return df
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return None

def treinar_e_avaliar(df):
    """Executa o pipeline de pré-processamento e treinamento."""
    
    # 1. Codificação de variáveis categóricas
    le = LabelEncoder()
    for col in df.columns:
        df[col] = le.fit_transform(df[col])
    
    # 2. Divisão entre atributos (X) e alvo (y)
    X = df.drop('class', axis=1)
    y = df['class']
    
    # 3. Split Treino/Teste (70/30) com semente fixa para reprodutibilidade
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # 4. Modelo Random Forest (Robusto para dados categóricos)
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)
    
    # 5. Predições e Métricas
    y_pred = modelo.predict(X_test)
    
    print("\n" + "="*50)
    print("RELATÓRIO TÉCNICO DE PERFORMANCE")
    print("="*50)
    print(classification_report(y_test, y_pred))
    
    # 6. Visualização da Matriz de Confusão (Usando apenas Matplotlib)
    cm = confusion_matrix(y_test, y_pred)
    
    fig, ax = plt.subplots(figsize=(6, 6))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Greens)
    ax.figure.colorbar(im, ax=ax)
    
    # Configuração de eixos e rótulos
    classes = ['Comestível', 'Venenoso']
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=classes, yticklabels=classes,
           title='Matriz de Confusão',
           ylabel='Valor Real',
           xlabel='Predição do Modelo')

    # Adicionar os números dentro da matriz
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], 'd'),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    dataset = carregar_dados()
    if dataset is not None:
        treinar_e_avaliar(dataset)
