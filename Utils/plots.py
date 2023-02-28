import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings

warnings.filterwarnings("ignore")

def plot_time_series(series, title='', in_title='16/02/2021 al 13/02/2023', ytitle='Cierre', xtitle='Dia', figsize=(10, 8),lag1=None,lag2=None,ts_title=['']):
    print('Imagen')
    colors = []
    for i in range(len(series)):
        color = tuple(np.random.rand(3))
        colors.append(color)
        
    fig = plt.figure(figsize=figsize)
    fig.suptitle(title, fontsize=20)

    plt.subplots_adjust(wspace= 0.25, hspace= 0.5)

    sub1 = fig.add_subplot(2,2,(1,2))# two rows, two columns, fist cell
    for i,serie in enumerate(series):
        sub1.plot(serie,color=colors[i],label=ts_title[i])
    sub1.set_title(in_title, fontsize=14)
    sub1.legend()
    sub1.set_ylabel(ytitle, fontsize=12)
    sub1.set_xlabel(xtitle, fontsize=12)
    
    # Establecer el espaciado de las fechas en el eje x
    sub1.xaxis.set_major_locator(mdates.AutoDateLocator())

     # Rotar las etiquetas del eje x para una mejor visualización
    plt.setp(sub1.xaxis.get_majorticklabels(), rotation=45)

    # Create second axes, the top-left plot with orange plot
    sub2 = fig.add_subplot(2,2,3)
    for i,serie in enumerate(series):
        if lag1 is None:
            plot_acf(serie, ax=sub2,color=colors[i])
        else:
            plot_acf(serie, ax=sub2,lags=lag1,color=colors[i])
    sub2.set_xlabel('Lags', fontsize=12)
    sub2.set_ylabel('Autocorrelacion', fontsize=12)

    # Create third axes, a combination of third and fourth cell
    sub3 = fig.add_subplot(2,2,4)
    for i,serie in enumerate(series):
        if lag2 is None:
            plot_pacf(serie, ax=sub3,color=color,method='ywmle')
        else:
            plot_pacf(serie,lags=lag2, ax=sub3,color=colors[i],method='ywmle')
    sub3.set_xlabel('Lags', fontsize=12)
    sub2.set_ylabel('Autocorrelacion Parcial', fontsize=12)