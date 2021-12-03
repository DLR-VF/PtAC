from matplotlib import pyplot as plt


def plot_something(df):
    plt.figure(figsize=(10, 5))
    plt.hist(df["distance_pt"], density=True, histtype='stepfilled', bins=1000, cumulative=True,
             color="lightgrey")
    plt.vlines(x=500, ymin=0, ymax=0.985, color='orange', linestyle='--')
    plt.hlines(y=0.985, xmin=0, xmax=500, color='orange', linestyle='--')
    plt.show()