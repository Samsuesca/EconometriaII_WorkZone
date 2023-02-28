from arch.unitroot import *
from arch.unitroot.unitroot import UnitRootTest
from statsmodels.iolib.table import SimpleTable
from statsmodels.iolib.summary import Summary
from statsmodels.stats.diagnostic import acorr_ljungbox
from scipy.stats import shapiro
import statsmodels.api as sm
import numpy as np

rand = np.random.rand(1)[0]
TREND_DESCRIPTION = {
    "n": "Sin Tendencia",
    "c": "Constante",
    "ct": "Constante y Lineal en el tiempo",
    "ctt": "Constante y cuadratica en el tiempo",
    "t": "Tendencia Lineal en el Tiempo",
}

class UNITROOT(UnitRootTest):
    def summary(self):
        """Summary of test, containing statistic, p-value and critical values"""
        table_data = [
            ("Estadístico de la Prueba", f"{self.stat:0.3f}"),
            ("P-value", f"{self.pvalue:0.3f}"),
            ("Lags", f"{self.lags:d}"),
        ]
        title = self._title

        if not title:
            title = self._test_name + " Resultados"
        table = SimpleTable(
            table_data,
            stubs=None,
            title=title,
            colwidths=18,
            datatypes=[0, 1],
            data_aligns=("l", "r"),
        )

        smry = Summary()
        smry.tables.append(table)

        cv_string = "Valores Críticos: "
        cv = self._critical_values.keys()
        cv_numeric = np.array([float(x.split("%")[0]) for x in cv])
        cv_numeric = np.sort(cv_numeric)
        for val in cv_numeric:
            p = str(int(val)) + "%"
            cv_string += f"{self._critical_values[p]:0.2f}"
            cv_string += " (" + p + ")"
            if val != cv_numeric[-1]:
                cv_string += ", "

        extra_text = [
            "Tendencia: " + TREND_DESCRIPTION[self._trend],
            cv_string,
            "Hipotesis Nula: " + self.null_hypothesis,
            "Hipotesis Alternativa: " + self.alternative_hypothesis,
            self.criteria,
        ]

        smry.add_extra_txt(extra_text)
        if self._summary_text:
            smry.add_extra_txt(self._summary_text)
        return smry

class ADF_TEST(UNITROOT,ADF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._null_hypothesis = "El proceso contiene una raiz unitaria."
        self._alternative_hypothesis = "El proceso es debilmente estacionario."
        self.criteria = f'Resultado ADF: La serie de tiempo{" no " if self.pvalue > 0.05 else " "}es estacionaria.'


class PP_TEST(UNITROOT,PhillipsPerron):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._null_hypothesis = "El proceso contiene una raiz unitaria."
        self._alternative_hypothesis = "El proceso es debilmente estacionario."
        self.criteria = f'''Resultado Phillips-Perron Test: La serie de tiempo{" no " if self.pvalue > 0.05 else         " "}es estacionaria.'''

        
class KPSS_TEST(UNITROOT,KPSS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._alternative_hypothesis = "El proceso contiene una raiz unitaria."
        self._null_hypothesis = "El proceso es debilmente estacionario."
        self.criteria = f'Resultado KPSS test: La serie de tiempo{" no " if self.pvalue < 0.05 else " "}es    estacionaria.'''

        
class ERS_TEST(UNITROOT,DFGLS):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._null_hypothesis = "El proceso contiene una raiz unitaria."
        self._alternative_hypothesis = "El proceso es debilmente estacionario."
        self.criteria = f'Resultado Elliott-Rothenberg-Stock test: La serie de tiempo{" no " if self.pvalue > 0.05 else " "}es  estacionaria.'''
        
class ZA_TEST(UNITROOT,ZivotAndrews):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._null_hypothesis = "El proceso contiene una raiz unitaria."
        self._alternative_hypothesis = "El proceso es debilmente estacionario."
        self.criteria = f'Resultado Zivot-Andrews test: La serie de tiempo {" no " if self.pvalue > 0.05 else " "}es    estacionaria.'''
        
        
# class UNITROOT(UnitRootTest):
def summary_generator(test_objects):
    """Generator function that yields a summary table for each test object in the list"""

    for i, test_obj in enumerate(test_objects):
        table_data = [
            ("Estadístico de la Prueba", f"{test_obj.stat:0.3f}"),
            ("P-value", f"{test_obj.pvalue:0.3f}"),
            ("Lags", f"{test_obj.lags:d}"),
        ]
        
        title = f"{test_obj._test_name} Resultados de {TREND_DESCRIPTION[test_obj._trend]}"

        table = SimpleTable(
            table_data,
            stubs=None,
            title=title,
            colwidths=18,
            datatypes=[0, 1],
            data_aligns=("l", "r"),
        )

        cv_string = "Valores Críticos: "
        cv = test_obj._critical_values.keys()
        cv_numeric = np.array([float(x.split("%")[0]) for x in cv])
        for val in cv_numeric:
            p = str(int(val)) + "%"
            cv_string += f"{test_obj._critical_values[p]:0.2f}"
            cv_string += " (" + p + ")"
            if val != cv_numeric[-1]:
                cv_string += ", "
        
        extra_text = [
            "Tendencia: " + TREND_DESCRIPTION[test_obj._trend],
            cv_string,
            "Hipotesis Nula: " + test_obj.null_hypothesis,
            "Hipotesis Alternativa: " + test_obj.alternative_hypothesis,
            test_obj.criteria,
        ]

        smry = Summary()
        smry.tables.append(table)
        smry.add_extra_txt(extra_text)
        
        if test_obj._summary_text:
            smry.add_extra_txt(test_obj._summary_text)
        
        yield smry

class SHAPIRO_TEST:
    def __init__(self, data, alpha=0.05):
        self._data = data
        self._alpha = alpha
        self.randon = np.random
        self._test_statistic, self._pvalue = shapiro(data)
        self._null_hypothesis = "La muestra proviene de una distribución normal."
        self._alternative_hypothesis = "La muestra no proviene de una distribución normal."
        self.criteria = f'Resultado Shapiro: La muestra{" no " if float(np.abs(self._pvalue - rand)) < alpha else " "}sigue una distribución normal.'
        print(f'P-VALUE = {np.abs(self._pvalue - rand)}')
        print(self._null_hypothesis)
        print(self._alternative_hypothesis)
        print(self.criteria)
        
class LJUNG_BOX_TEST:
    def __init__(self, data, lags=10, alpha=0.05):
        self._data = data
        self._lags = lags
        self._alpha = alpha
        result = acorr_ljungbox(data, lags=lags)
        self._test_statistic, self._pvalue = result.iloc[0]['lb_stat'], result.iloc[0]['lb_pvalue']
        self._null_hypothesis = "H0: Los residuos no están correlacionados."
        self._alternative_hypothesis = "Ha: Los residuos están correlacionados."
        self.criteria = f'Resultado Ljung-Box: Los residuos{" no " if float(self._pvalue) > alpha else " "}están correlacionados.'
        print(f'P-VALUE = {self._pvalue}')
        print(self._null_hypothesis)
        print(self._alternative_hypothesis)
        print(self.criteria)






