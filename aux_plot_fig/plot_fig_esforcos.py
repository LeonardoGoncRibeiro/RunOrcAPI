# Importando pacotes

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from functions import *

# Parâmetros de Entrada

# Nome do arquivo CSV
csvfile_name = r"input_files\01_A2M5_N_1_Esforcos.csv"

# Nome do arquivo PNG final
pngfile_name = r"A2M5\Esforcos"

# -------------------------------------------------------------------------------------------------------------------------------------------------
# Plotar figuras
# -------------------------------------------------------------------------------------------------------------------------------------------------

plot_esforcos(csvfile_name, pngfile_name)