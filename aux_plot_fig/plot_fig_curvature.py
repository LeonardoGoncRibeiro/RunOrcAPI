# Importando pacotes

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from functions import *

# Parâmetros de Entrada

# Nome do arquivo CSV
csvfile_name_top = r"input_files\Teste_1_CorteTopo_v1b_sem_elemento_001_Linetop_Curvature.csv"
csvfile_name_bot = r"input_files\Teste_1_CorteTopo_v1b_sem_elemento_001_Linebot_Curvature.csv"

# Indicador de ruptura no topo
in_rupt_top = 0

# Timestamps a plotar (se existirem no arquivo)
timestamps = ['0.0', '0.6', '1.2']

# Nome do arquivo PNG final
pngfile_name = "Modelo1_Curvature_Timestamps_Init"

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Plotar figuras
# -------------------------------------------------------------------------------------------------------------------------------------------------

plot_curvature(csvfile_name_bot, pngfile_name + "_BOT", timestamps)

if in_rupt_top == 0:

    plot_curvature(csvfile_name_top, pngfile_name + "_TOP", timestamps)

