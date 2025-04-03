import pydantic as pd

from nx_api.utils.pydantic.load import LoadOptsMixin


class BaseModel(pd.BaseModel, LoadOptsMixin):
    model_config = pd.ConfigDict(from_attributes=True)
