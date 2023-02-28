import numpy as np
def escalar_datos(data,a=2,b=1):
    data_min = np.min(data)
    data_max = np.max(data)
    return a*(data - data_min) / (data_max - data_min)-b
