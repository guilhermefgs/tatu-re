import numpy as np

from sklearn.preprocessing import PolynomialFeatures
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from hmmlearn.hmm import GaussianHMM

from tatu_re.model.data_processing import IndicatorsTransformer

def hmm_pipeline():

    pipe = Pipeline([
        ('indicators', IndicatorsTransformer()),
        ('simple_imputer', SimpleImputer(missing_values=np.nan, strategy='mean') ), 
        ('polinomial_features', PolynomialFeatures()),
        ('hmm', GaussianHMM()),
    ])

    return pipe
