"""
The ``tools`` module contains a collection of helper functions used in the
windpowerlib.

"""


__copyright__ = "Copyright oemof developer group"
__license__ = "GPLv3"

import numpy as np


def linear_interpolation_extrapolation(df, target_height):
    r"""
    Inter- or extrapolates between the values of a data frame.

    This function can be used for the inter-/extrapolation of a parameter
    (e.g wind speed) available at two or more different heights, to approximate
    the value at hub height. The function is carried out when the parameter
    `wind_speed_model`, `density_model` or `temperature_model` of an
    instance of the :class:`~.modelchain.ModelChain` class is
    'interpolation_extrapolation'.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with time series for parameter that is to be interpolated or
        extrapolated. The columns of the DataFrame are the different heights
        for which the parameter is available. If more than two heights are
        given, the two closest heights are used. See example below on how the
        DataFrame should look like and how the function can be used.
    target_height : float
        Height for which the parameter is approximated (e.g. hub height).

    Returns
    -------
    pandas.Series
        Result of the inter-/extrapolation (e.g. wind speed at hub height).

    Notes
    -----

    For the inter- and extrapolation the following equation is used:

    .. math:: f(x) = \frac{(f(x_2) - f(x_1))}{(x_2 - x_1)} \cdot (x - x_1) + f(x_1)

    Examples
    ---------
    >>> import numpy as np
    >>> import pandas as pd
    >>> wind_speed_10m = np.array([[3], [4]])
    >>> wind_speed_80m = np.array([[6], [6]])
    >>> weather_df = pd.DataFrame(np.hstack((wind_speed_10m,
    ...                                      wind_speed_80m)),
    ...                           index=pd.date_range('1/1/2012',
    ...                                               periods=2,
    ...                                               freq='H'),
    ...                           columns=[np.array(['wind_speed',
    ...                                              'wind_speed']),
    ...                                    np.array([10, 80])])
    >>> linear_interpolation_extrapolation(
    ...     weather_df['wind_speed'], 100)[0]
    6.8571428571428577

    """
    # find closest heights
    heights_sorted = df.columns[
        sorted(range(len(df.columns)),
               key=lambda i: abs(df.columns[i] - target_height))]
    return ((df[heights_sorted[1]] - df[heights_sorted[0]]) /
            (heights_sorted[1] - heights_sorted[0]) *
            (target_height - heights_sorted[0]) + df[heights_sorted[0]])


def gaussian_distribution(function_variable, standard_deviation, mean=0):
    r"""
    Normal distribution or gaussian distribution.

    Parameters
    ----------
    function_variable : Float
        Variable of the gaussian distribution.
    standard_deviation : Float
        Standard deviation of the gaussian distribution.
    mean : Float
        Defines the offset of the gaussian distribution function. Default: 0.

    Returns
    -------
    pandas.Series or numpy.array
        Wind speed at hub height. Data type depends on type of `wind_speed`.

    Notes
    -----
    The following equation is used [1]_:

    .. math:: f(x) = \frac{1}{\sigma \sqrt{2 \pi}} exp
                     \left[ -\frac{(x-\mu)^2}{2 \sigma^2}  \right]

    with:
        # TODO: add variables

    References
    ----------
    .. [1] Berendsen, H.: "A Student's Guide to Data and Error Analysis".
             New York, Cambridge University Press, 2011, p. 37
    
    # TODO: add references

    """
    return (1 / (standard_deviation * np.sqrt(2 * np.pi)) *
            np.exp(-(function_variable - mean)**2 /
                   (2 * standard_deviation**2)))
