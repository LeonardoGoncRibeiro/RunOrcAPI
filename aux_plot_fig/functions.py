import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_eff_tensions(name_csv, name_png, times_required):

    list_cols = ['X', *[f"EffTens_{ts}" for ts in times_required]]

    df = pd.read_csv(name_csv)[list_cols]

    cols = df.columns

    timestamps = [float(col.split("_")[-1]) for col in df.columns if col != "X"]
    df.columns = ['X', *[f"{ts} s" for ts in timestamps]]

    df = df.melt(id_vars = 'X')

    fig, ax = plt.subplots()

    palette = ["#1B9E77", # Verde escuro
               "#D95F02", # Laranja
               "#7570B3", # Roxo
               "#E7298A", # Rosa
               "#66A61E", # Verde claro
               "#E6AB02", # Amarelo
               "#A6761D", # Marrom
               "#666666"  # Cinza
              ]
    
    num_vars = len(df['variable'].unique())

    sns.lineplot(x = "X", y = "value", data = df, hue = 'variable', palette=palette[:num_vars])

    plt.legend()
    
    plt.xlabel("Comprimento do Riser (m)")
    plt.ylabel("Tensão Efetiva (kN)")

    plt.savefig(f"aux_plot_fig/PNG/{name_png}.png", format = "png")

def plot_curvature(name_csv, name_png, times_required):

    list_cols = ['X', *[f"Curv_{ts}" for ts in times_required]]

    df = pd.read_csv(name_csv)[list_cols]

    cols = df.columns

    timestamps = [float(col.split("_")[-1]) for col in df.columns if col != "X"]
    df.columns = ['X', *[f"{ts} s" for ts in timestamps]]

    df = df.melt(id_vars = 'X')

    fig, ax = plt.subplots()

    palette = ["#1B9E77", # Verde escuro
               "#D95F02", # Laranja
               "#7570B3", # Roxo
               "#E7298A", # Rosa
               "#66A61E", # Verde claro
               "#E6AB02", # Amarelo
               "#A6761D", # Marrom
               "#666666"  # Cinza
              ]
    
    num_vars = len(df['variable'].unique())

    sns.lineplot(x = "X", y = "value", data = df, hue = 'variable', palette = palette[:num_vars])

    plt.legend()
    
    plt.xlabel("Comprimento do Riser (m)")
    plt.ylabel("Curvatura (1/m)")

    plt.savefig(f"aux_plot_fig/PNG/{name_png}.png", format = "png")

def plot_deformed_conf(name_csv_bot, name_csv_top, in_rupt_top, name_png, times_required, xlim = [], ylim = [], LayAz = 0):

    list_cols = [*[f"X_{ts}" for ts in times_required], *[f"Y_{ts}" for ts in times_required], *[f"Z_{ts}" for ts in times_required]]

    df = pd.read_csv(name_csv_bot)[list_cols]

    cols = df.columns

    timestamps = sorted(list(set([float(col.split("_")[-1]) for col in df.columns if col != "X"])))

    fig, ax = plt.subplots()

    palette = ["#1B9E77", # Verde escuro
               "#D95F02", # Laranja
               "#7570B3", # Roxo
               "#E7298A", # Rosa
               "#66A61E", # Verde claro
               "#E6AB02", # Amarelo
               "#A6761D", # Marrom
               "#666666"  # Cinza
              ]

    for i, ts in enumerate(timestamps):
        x = df[f"X_{ts}"]
        y = df[f"Y_{ts}"]
        z = df[f"Z_{ts}"]

        LayAzRad = LayAz/180*np.pi

        x_new = x*np.cos(LayAzRad) + y*np.sin(LayAzRad)

        plt.plot(x_new, z, label = f"{ts} s", color = palette[i])

    plt.legend()

    if xlim != []:
        plt.xlim(xlim)

    if ylim != []:
        plt.ylim(ylim)

    plt.xlabel("X'")
    plt.ylabel("Z")

    plt.savefig(f"aux_plot_fig/PNG/{name_png}.png", format = "png")

def plot_soil_conf(name_csv_bot, name_png, times_required, TDPx, TDPy, Conx, Cony, Depth, xlim = [], ylim = []):

    list_cols = [*[f"X_{ts}" for ts in times_required], *[f"Y_{ts}" for ts in times_required], *[f"Z_{ts}" for ts in times_required]]

    df = pd.read_csv(name_csv_bot)[list_cols]

    cols = df.columns

    timestamps = sorted(list(set([float(col.split("_")[-1]) for col in df.columns if col != "X"])))

    fig, ax = plt.subplots()

    for ts in timestamps:
        x = df[f"X_{ts}"]
        y = df[f"Y_{ts}"]
        z = df[f"Z_{ts}"]

        plt.plot(x, y)

        df2 = df[df[f"Z_{ts}"] > -Depth+1]

        x = df2[f"X_{ts}"]
        y = df2[f"Y_{ts}"]
        z = df2[f"Z_{ts}"]

        plt.plot(x, y, color = 'r')

    if xlim != []:
        plt.xlim(xlim)

    if ylim != []:
        plt.ylim(ylim)

    plt.xlabel("X")
    plt.ylabel("Y")

    plt.plot([TDPx, Conx], [TDPy, Cony], color = 'k', linestyle = '--')

    plt.plot(TDPx, TDPy, color = 'k', marker = 'x', markersize = 10, label = "TDP", markeredgewidth = 3)

    plt.legend()

    plt.savefig(f"aux_plot_fig/PNG/{name_png}.png", format = "png")

def plot_envoltorias(name_csv, name_png, ylims_B, ylims_T, ylims_V):

    df = pd.read_csv(name_csv)

    fig, ax = plt.subplots()

    plt.plot(df['X'], df['Bmax'], color = 'r', label = 'Máximo')
    plt.plot(df['X'], df['Bmin'], color = 'b', label = 'Mínimo')

    ax.set_yscale('log')
        
    if ylims_B != []:
        plt.ylim(ylims_B)

    plt.xlabel("X")
    plt.ylabel("Raio de Curvatura (m)")

    plt.legend()

    plt.savefig(f"aux_plot_fig/PNG/{name_png}_BendRad.png", format = "png")

    fig, ax = plt.subplots()

    plt.plot(df['X'], df['Tmax'], color = 'r', label = 'Máximo')
    plt.plot(df['X'], df['Tmin'], color = 'b', label = 'Mínimo')
        
    if ylims_T != []:
        plt.ylim(ylims_T)

    plt.xlabel("X")
    plt.ylabel("Tração (kN)")

    plt.legend()

    plt.savefig(f"aux_plot_fig/PNG/{name_png}_EffTens.png", format = "png")

    fig, ax = plt.subplots()

    plt.plot(df['X'], df['Vmax'], color = 'r', label = 'Máximo')
    plt.plot(df['X'], df['Vmin'], color = 'b', label = 'Mínimo')
        
    if ylims_T != []:
        plt.ylim(ylims_T)

    plt.xlabel("X")
    plt.ylabel("Velocidade (m/s)")

    plt.legend()

    plt.savefig(f"aux_plot_fig/PNG/{name_png}_Velocity.png", format = "png")

def plot_esforcos(name_csv_bot, name_png):

    df = pd.read_csv(name_csv_bot)

    fig, ax = plt.subplots()

    cols = df.columns[1:]

    palette = ["#1B9E77", # Verde escuro
               "#D95F02", # Laranja
               "#7570B3", # Roxo
               "#E7298A", # Rosa
               "#66A61E", # Verde claro
               "#E6AB02", # Amarelo
               "#A6761D", # Marrom
               "#666666"  # Cinza
              ]

    for var in cols:

        plt.figure()

        x = df["Time"]
        y = df[var]

        if 'EffTens' in var:
            color = "#1B9E77"
            ylabel = 'Tração (kN)'
        elif 'BendMom' in var:
            color = "#D95F02"
            ylabel = 'Momento Fletor (kNm)'
        elif 'ShearFc' in var:
            color = "#7570B3"
            ylabel = 'Cortante (kN)'

        plt.plot(x, y, color = color)

        plt.xlabel("Tempo (s)")
        plt.ylabel(ylabel)

        plt.savefig(f"aux_plot_fig/PNG/{name_png}_{var}.png", format = "png")
