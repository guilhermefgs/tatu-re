import numpy as np

from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

from model.data_processing import IndicatorsTransformer

def linear_regression_pipeline():

    pipe = Pipeline([
        ('indicators', IndicatorsTransformer())
        ('simple_imputer', SimpleImputer(missing_values=np.nan, strategy='mean') ), 
        ('scaler', StandardScaler()), 
        ('polinomial_features', PolynomialFeatures())
        ('linear_regression', LinearRegression())
    ])

    return pipe

