# Importando pacotes

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from functions import *

# Parâmetros de Entrada

# Nome do arquivo CSV
csvfile_name_top = r"input_files\Teste_1_CorteTopo_v1b_sem_elemento_001_Linetop_DeformedConfig.csv"
csvfile_name_bot = r"input_files\Teste_1_CorteTopo_v1b_sem_elemento_001_Linebot_DeformedConfig.csv"

# Indicador de ruptura no topo
in_rupt_top = 0

# Timestamps a plotar (se existirem no arquivo)
timestamps = ['0.0', '40.0', '80.0', '120.0', '160.0']

# Nome do arquivo PNG final
pngfile_name = "Modelo1_DeformedConfig_Timestamps"

# Limites do gráfico
xlim = [0, 2000]
ylim = [-2000, 0]

# Definindo lay-azimuth, para plotar no plano do riser (se não for necessário, colocar 0)
LayAzimuth = 332

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Plotar figuras
# -------------------------------------------------------------------------------------------------------------------------------------------------

plot_deformed_conf(csvfile_name_bot, csvfile_name_top, in_rupt_top, pngfile_name, timestamps, xlim, ylim, LayAzimuth)