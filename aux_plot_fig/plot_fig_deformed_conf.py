# Importando pacotes

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from functions import *

# Parâmetros de Entrada

# Nome do arquivo CSV
csvfile_name_top = r"input_files\Teste_2_CorteTopo_v1b_sem_elemento_Vrs02_Case04_Linetop_DeformedConfig.csv"
csvfile_name_bot = r"input_files\Teste_2_CorteTopo_v1b_sem_elemento_Vrs02_Case04_Linebot_DeformedConfig.csv"
csvfile_name_cab = r"input_files\Teste_2_CorteTopo_v1b_sem_elemento_Vrs02_Case04_Cabo_DeformedConfig.csv"

# Indicador de ruptura no topo
in_rupt_top = 0

# Timestamps a plotar (se existirem no arquivo)
timestamps = ['0.0', '5.0', '10.0', '15.0', '20.0']

# Nome do arquivo PNG final
pngfile_name = "Alternativa2Modelo4_DeformedConfig_Timestamps"

# Limites do gráfico
xlim = [0, 600]
ylim = [-1200, -600]

# Definindo lay-azimuth, para plotar no plano do riser (se não for necessário, colocar 0)
LayAzimuth = 332

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Plotar figuras
# -------------------------------------------------------------------------------------------------------------------------------------------------

plot_deformed_conf(csvfile_name_bot, csvfile_name_top, in_rupt_top, pngfile_name, timestamps, xlim, ylim, LayAzimuth)