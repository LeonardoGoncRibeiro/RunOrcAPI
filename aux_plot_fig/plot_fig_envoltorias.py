# Importando pacotes

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from functions import *

# Parâmetros de Entrada

# Nome do arquivo CSV
csvfile_name_top = r"input_files\01_A2M5_N_1_Linetop_Envoltorias.csv"
csvfile_name_bot = r"input_files\01_A2M5_N_1_Linebot_Envoltorias.csv"
csvfile_name_cab = r"input_files\01_A2M5_N_1_Cabo_Envoltorias.csv"

# Indicador de ruptura no topo
in_rupt_top = 0

# Indicador de existência de cabo
in_cabo = 1

# Nome do arquivo PNG final
pngfile_name = "A2M5/Envoltorias"

ylims_B = [0.1, 1000000]
ylims_T = []
ylims_V = []

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Plotar figuras
# -------------------------------------------------------------------------------------------------------------------------------------------------

plot_envoltorias(csvfile_name_bot, pngfile_name + "_BOT", ylims_B, ylims_T, ylims_V)

if in_rupt_top == 0:

    plot_envoltorias(csvfile_name_top, pngfile_name + "_TOP", ylims_B, ylims_T, ylims_V)

if in_cabo == 1:

    plot_envoltorias(csvfile_name_cab, pngfile_name + "_CAB", ylims_B, ylims_T, ylims_V)