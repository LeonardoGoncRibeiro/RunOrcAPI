# Importando pacotes

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from functions import *

# Parâmetros de Entrada

# Nome do arquivo CSV
csvfile_name_bot = r"input_files\Teste_1_CorteTopo_v1b_sem_elemento_001_Linebot_DeformedConfig.csv"

# Timestamps a plotar (se existirem no arquivo)
timestamps = ['200.0']

# Nome do arquivo PNG final
pngfile_name = "Modelo1_SoilConf"

# Limites do gráfico
xlim = [300, 500]
ylim = [-400, -200]

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Plotar figuras
# -------------------------------------------------------------------------------------------------------------------------------------------------

plot_soil_conf(csvfile_name_bot, pngfile_name, timestamps, xlim, ylim)