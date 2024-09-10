import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

    plt.savefig(f"aux_plot_fig/PNG/{name_png}.png", format = "png")