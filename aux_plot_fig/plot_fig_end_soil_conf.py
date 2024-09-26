# Importando pacotes

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from functions import *

# Parâmetros de Entrada

# Nome do arquivo CSV
csvfile_name_bot = r"input_files\Teste_1_CorteTopo_v1b_sem_elemento_Case05_001_Linebot_DeformedConfig.csv"

# Timestamps a plotar (se existirem no arquivo)
timestamps = ['200.0']

# Nome do arquivo PNG final
pngfile_name = "Modelo1_SoilConf"

# Limites do gráfico
xlim = [0, 700]
ylim = [-800, -100]

TDPx = 850.636
TDPy = -451.944

TopConx = 3.386
TopCony = -1.454

Depth = 1943

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Plotar figuras
# -------------------------------------------------------------------------------------------------------------------------------------------------

plot_soil_conf(csvfile_name_bot, pngfile_name, timestamps, TDPx, TDPy, TopConx, TopCony, Depth, xlim, ylim)