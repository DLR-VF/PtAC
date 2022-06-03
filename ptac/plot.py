from matplotlib import pyplot as plt
import numpy as np


def plot_something(df):
    plt.figure(figsize=(10, 5))
    plt.hist(df["distance_pt"], density=True, histtype='stepfilled', bins=1000, cumulative=True,
             color="lightgrey")
    plt.vlines(x=500, ymin=0, ymax=0.985, color='orange', linestyle='--')
    plt.hlines(y=0.985, xmin=0, xmax=500, color='orange', linestyle='--')
    plt.show()



    # getting data of the histogram
    count, bins_count = np.histogram(df["distance_pt"].values, bins=10)

    # finding the PDF of the histogram using count values
    pdf = count / sum(count)

    # using numpy np.cumsum to calculate the CDF
    # We can also find using the PDF values by looping and adding
    cdf = np.cumsum(pdf)

    # plotting PDF and CDF
    plt.plot(bins_count[1:], pdf, color="red", label="PDF")
    plt.plot(bins_count[1:], cdf, label="CDF")
    plt.legend()
