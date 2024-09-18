# Importando pacotes

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from functions import *

# Parâmetros de Entrada

# Nome do arquivo CSV
csvfile_name_top = r"input_files\Teste_2_CorteTopo_v1b_sem_elemento_Vrs02_Case03_001_Linetop_Envoltorias.csv"
csvfile_name_bot = r"input_files\Teste_2_CorteTopo_v1b_sem_elemento_Vrs02_Case03_001_Linebot_Envoltorias.csv"

# Indicador de ruptura no topo
in_rupt_top = 0

# Nome do arquivo PNG final
pngfile_name = "Alternativa2Modelo3_Envoltorias"

ylims_B = [0.1, 1e6]
ylims_T = []
ylims_V = []

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Plotar figuras
# -------------------------------------------------------------------------------------------------------------------------------------------------

plot_envoltorias(csvfile_name_bot, pngfile_name + "_BOT", ylims_B, ylims_T, ylims_V)

if in_rupt_top == 0:

    plot_envoltorias(csvfile_name_top, pngfile_name + "_TOP", ylims_B, ylims_T, ylims_V)

