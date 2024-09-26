# Importando pacotes

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from functions import *

# Parâmetros de Entrada

# Nome do arquivo CSV
csvfile_name_top = r"input_files\Teste_2_CorteTopo_v1b_sem_elemento_Vrs02_Case04_Linebot_EffectiveTension.csv"
csvfile_name_bot = r"input_files\Teste_2_CorteTopo_v1b_sem_elemento_Vrs02_Case04_Linetop_EffectiveTension.csv"
csvfile_name_cab = r"input_files\Teste_2_CorteTopo_v1b_sem_elemento_Vrs02_Case04_Cabo_EffectiveTension.csv"

# Indicador de ruptura no topo
in_rupt_top = 0

# Indicador de cabo
in_cabo = 1

# Timestamps a plotar (se existirem no arquivo)
timestamps = ['0.0', '2.4', '3.0', '3.6']

# Nome do arquivo PNG final
pngfile_name = "Alternativa2Modelo4_EffectiveTension_Timestamps_End"

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Plotar figuras
# -------------------------------------------------------------------------------------------------------------------------------------------------

plot_eff_tensions(csvfile_name_bot, pngfile_name + "_BOT", timestamps)

if in_rupt_top == 0:

    plot_eff_tensions(csvfile_name_top, pngfile_name + "_TOP", timestamps)

if in_cabo == 1:

    plot_eff_tensions(csvfile_name_cab, pngfile_name + "_CABO", timestamps)

