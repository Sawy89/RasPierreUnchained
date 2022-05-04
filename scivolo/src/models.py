import datetime
from pydantic import BaseModel
from typing import List


class ForecastData(BaseModel):
    x_train: List[List[float]]
    y_train: List[float]
    x_test: List[List[float]]
