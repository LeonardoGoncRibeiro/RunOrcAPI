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

    sns.lineplot(x = "X", y = "value", data = df, hue = 'variable')

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

    sns.lineplot(x = "X", y = "value", data = df, hue = 'variable')

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

    for ts in timestamps:
        x = df[f"X_{ts}"]
        y = df[f"Y_{ts}"]
        z = df[f"Z_{ts}"]

        LayAzRad = LayAz/180*np.pi

        x_new = x*np.cos(LayAzRad) + y*np.sin(LayAzRad)

        plt.plot(x_new, z, label = f"{ts} s")

    plt.legend()

    if xlim != []:
        plt.xlim(xlim)

    if ylim != []:
        plt.ylim(ylim)

    plt.xlabel("X'")
    plt.ylabel("Z")

    plt.savefig(f"aux_plot_fig/PNG/{name_png}.png", format = "png")

def plot_soil_conf(name_csv_bot, name_png, times_required, xlim = [], ylim = []):

    list_cols = [*[f"X_{ts}" for ts in times_required], *[f"Y_{ts}" for ts in times_required], *[f"Z_{ts}" for ts in times_required]]

    df = pd.read_csv(name_csv_bot)[list_cols]

    cols = df.columns

    timestamps = sorted(list(set([float(col.split("_")[-1]) for col in df.columns if col != "X"])))

    fig, ax = plt.subplots()

    for ts in timestamps:
        x = df[f"X_{ts}"]
        y = df[f"Y_{ts}"]
        z = df[f"Z_{ts}"]

        plt.plot(x, y, label = f"{ts} s")

    if xlim != []:
        plt.xlim(xlim)

    if ylim != []:
        plt.ylim(ylim)

    plt.xlabel("X")
    plt.ylabel("Y")

    plt.savefig(f"aux_plot_fig/PNG/{name_png}.png", format = "png")

