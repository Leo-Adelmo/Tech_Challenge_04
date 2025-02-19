from datetime import datetime

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from web_scraping import web_scraping_dados_ipea


def tratando_base_dados(df: pd.DataFrame)-> pd.DataFrame:
    
    df['Data'] = pd.to_datetime(df["Data"],format="%d/%m/%Y",errors='coerce')

    # # Substituir vírgula por ponto para converter em float
    df["Preço_Brent"] = df.iloc[:, 1].replace({',': '.'}, regex=True).astype(float)
    # Ordenar os dados por data
    df = df.sort_values(by="Data").reset_index(drop=True)

    # Criar feature de defasagem (lag) para previsão do próximo dia
    df["Preço_Anterior"] = df["Preço_Brent"].shift(1)

    # Remover valores NaN gerados pelo shift
    df = df.dropna()

    return df


class ModeloPrevisao:
    def __init__(self, df):
        self.df = df
        self.model = None
        self.X_train_scaled = None
        self.X_test_scaled = None
        self.y_train = None
        self.y_test = None
        self.mae = None
        self.rmse = None
        self.r2 = None

        """Prepara os dados para treinamento e teste."""
        # Definir features (X) e target (y)
        X = self.df[["Preço_Anterior"]]
        y = self.df["Preço_Brent"]

        # Dividir os dados em treino (80%) e teste (20%)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

        # Normalizar as features
        scaler = StandardScaler()
        self.X_train_scaled = scaler.fit_transform(self.X_train)
        self.X_test_scaled = scaler.transform(self.X_test)

        self.model = LinearRegression()
        self.model.fit(self.X_train_scaled, self.y_train)

    def avaliar_modelo(self):
        """Avalia o modelo utilizando MAE, RMSE e R² Score."""
        y_pred = self.model.predict(self.X_test_scaled)

        self.mae = mean_absolute_error(self.y_test, y_pred)
        self.rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))
        self.r2 = r2_score(self.y_test, y_pred)

        return self.mae, self.rmse, self.r2


    def prever_valor_para_data_especifica(self, data_especifica:datetime):
        """Faz a previsão para uma data específica do conjunto de teste."""
        # Localize o índice correspondente à data específica
        idx_data = self.df[self.df['Data'] == data_especifica].index[0] - 1


        # Verifique se a data existe no conjunto de teste (y_test ou X_test)
        if idx_data >= len(self.X_train):  # Garantindo que a data está no conjunto de teste
            idx_test = idx_data - len(self.X_train)  # Ajuste do índice para o conjunto de teste
        else:
            raise ValueError("A data especificada não está no conjunto de teste!")

        # Pegue o exemplo de teste correspondente
        X_novo = self.X_test_scaled[idx_test].reshape(1, -1)
        y_real = self.y_test.iloc[idx_test]

        # Fazer a previsão
        y_pred_novo = self.model.predict(X_novo)[0]
        data_escolhida = self.df["Data"].iloc[idx_data].strftime("%d/%m/%Y")
        valor_real = self.df["Preço_Brent"].iloc[idx_data]

        # Exibir os resultados
        return data_escolhida, y_pred_novo, valor_real
                


