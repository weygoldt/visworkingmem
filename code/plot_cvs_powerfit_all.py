import os
from pathlib import Path

import cmocean.cm as cmo
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plottools.colors as clrs
import seaborn as sns
from matplotlib.pyplot import cm
from scipy.optimize import curve_fit
from scipy.stats import wilcoxon

from cvs_preprocessing import dataimport
from modules.functions import bound_logistic
from modules.plotstyle import PlotStyle

colors = mcolors.TABLEAU_COLORS

def mean_sem(df):
    # means and sem for trial duration
    names = np.unique(df.subj).tolist()
    n = df.shape[1] / len(names)
    means = np.array(df.tpertrial.groupby(df.subj).mean())
    sems = np.array(df.tpertrial.groupby(df.subj).std()) / np.sqrt(n)

    # put to dataframe
    df_all = pd.DataFrame(
        list(zip(names, means, sems)),
        columns=("names", "tpertrial_means", "tpertrial_sems"),
    )

    # means and sems for no of switches
    means = np.array(df.switches.groupby(df.subj).mean())
    sems = np.array(df.switches.groupby(df.subj).std()) / np.sqrt(n)
    df_all["switches_means"] = means
    df_all["switches_sems"] = sems

    return df_all


def func_powerlaw(x, m, c, c0):
    return c0 + x**m * c


def fit_power(x, y):
    
    popt, pcov = curve_fit(func_powerlaw, x, y, method="trf", maxfev=50000)
    return popt, pcov
    

def plot_errorbars(df_all, ax):

    for name, color in zip(df_all.names, colors):
        minidf = df_all[df_all.names == name]
        ax.errorbar(
            minidf.switches_means,
            minidf.tpertrial_means,
            xerr=minidf.switches_sems,
            yerr=minidf.tpertrial_sems,
            fmt="bo",
            label=name,
            color=color,
        )

def plot_powerfit_1(df): 
    
    df_all = mean_sem(df)
    print(df_all)
    popt, pcov = fit_power(df_all.switches_means, df_all.tpertrial_means)
    fig, ax = plt.subplots(1,2, figsize=(24*ps.cm, 12*ps.cm), constrained_layout=True)
   
    for i in range(len(ax)):
        plot_errorbars(df_all, ax[i])

    x = np.linspace(df_all.switches_means.min()-0.2, df_all.switches_means.max()+2, 1000)

    ax[1].plot(x, func_powerlaw(x, *popt))
    ax[0].plot(x, func_powerlaw(x, *popt))
    ax[1].set_ylim(0, 6)

    fig.supxlabel('Number of switches', fontsize=14)
    fig.supylabel('Time per trial', fontsize=14)
    
    plt.show()

if __name__ == "__main__":
    
    # init standardized plotstyle
    ps = PlotStyle()

    # import the data
    dataroot = Path("../data/cvs")
    processed_dataroot = Path("../data_processed")
    df = dataimport(dataroot, processed_dataroot)
    
    plot_powerfit_1(df)

"""

def plot_errorbars2(df_all, ax, color):
    for name, _ in zip(df_all.names, colors):
        minidf = df_all[df_all.names == name]
        ax.errorbar(
            minidf.switches_means,
            minidf.tpertrial_means,
            xerr=minidf.switches_sems,
            yerr=minidf.tpertrial_sems,
            fmt="bo",
            label=name,
            color=color,
        )

# sort dataset by delay condition
df_0 = df[df.delay == 0]
df_2 = df[df.delay == 1.5]

ms_0 = mean_sem(df_0)
ms_2 = mean_sem(df_2)

popt0, pcov = curve_fit(func_powerlaw, ms_0.switches_means, ms_0.tpertrial_means, method="trf", maxfev=50000)
popt2, pcov = curve_fit(func_powerlaw, ms_2.switches_means, ms_2.tpertrial_means, method="trf", maxfev=50000)

fig, ax = plt.subplots()
plot_errorbars2(ms_0, ax, color='red')
plot_errorbars2(ms_2, ax, color='blue')

ax.plot(x, func_powerlaw(x, *popt0))
ax.plot(x, func_powerlaw(x, *popt2))

plt.show()

# sort dataset by delay condition
df_0 = df[df.cpd == 2]
df_2 = df[df.cpd == 8]

ms_0 = mean_sem(df_0)
ms_2 = mean_sem(df_2)

popt0, pcov = curve_fit(func_powerlaw, ms_0.switches_means, ms_0.tpertrial_means, method="trf", maxfev=50000)
popt2, pcov = curve_fit(func_powerlaw, ms_2.switches_means, ms_2.tpertrial_means, method="trf", maxfev=50000)

fig, ax = plt.subplots()
plot_errorbars(ms_0, ax)
plot_errorbars(ms_2, ax)

ax.plot(x, func_powerlaw(x, *popt0))
ax.plot(x, func_powerlaw(x, *popt2))

plt.show()


def getindex(df):

    mean = []
    sem = []
    names = []
    for name in np.unique(df.subj):
        print(np.min(df.strat_idx[df.subj==name]))
        print(np.max(df.strat_idx[df.subj==name]))
        mean.append(np.mean(df.strat_idx[df.subj==name]))
        sem.append(np.std(df.strat_idx[df.subj==name]))
        names.append(name)

    return mean, sem, names

mean, sem, names = getindex(df)

fig, ax = plt.subplots()

for i, name in enumerate(names):
    plt.errorbar(mean[i], i, xerr=sem[i], fmt='bo')

ax.set_xlim(0,1)

plt.show()

# repeat for two categories
fig, ax = plt.subplots()

mean, sem, names = getindex(df[df.delay==0])

for i, name in enumerate(names):
    plt.errorbar(mean[i], i, xerr=sem[i], fmt='bo')


mean, sem, names = getindex(df[df.delay==1.5])

for i, name in enumerate(names):
    plt.errorbar(mean[i], i+0.2, xerr=sem[i], fmt='ro')

ax.set_xlim(0,1)

plt.show()
"""