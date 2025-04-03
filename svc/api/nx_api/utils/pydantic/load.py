from typing import Sequence, Type, get_args, get_origin

from pydantic._internal._model_construction import ModelMetaclass
from sqlalchemy import orm
from sqlalchemy.orm import DeclarativeBase, Relationship
from sqlalchemy.orm.interfaces import ORMOption


class LoadOptions:
    def __init__(self, model) -> None:
        self._model = model
        self._override: dict[Relationship, ORMOption] = {}

    @staticmethod
    def extract_ann(ann):
        is_seq = False
        pd_type = None

        def recursive(ann):
            nonlocal pd_type, is_seq

            origin = get_origin(ann)
            if origin and isinstance(origin, type) and issubclass(origin, Sequence):
                is_seq = True

            if isinstance(ann, ModelMetaclass):
                pd_type = ann
                return

            args = get_args(ann)

            for arg in args:
                recursive(arg)

        recursive(ann)

        return pd_type, is_seq

    @staticmethod
    def get_sa_type(pd_type):
        return getattr(getattr(pd_type, "_model", None), "default", None)

    def __call__(self):
        visited = set()

        def get_opts(from_pd, exec=None):
            options = ()

            from_sa = self.get_sa_type(from_pd)
            if from_sa is not None:
                for fname, finfo in from_pd.model_fields.items():
                    to_pd, is_seq = self.extract_ann(finfo.annotation)
                    if not to_pd:
                        continue

                    to_sa = self.get_sa_type(to_pd)
                    if to_sa is None:
                        continue

                    rel = getattr(from_sa, fname)
                    if rel in visited:
                        continue
                    visited.add(rel)

                    loader = orm.selectinload if is_seq else orm.joinedload

                    load_opt = self._override.get(rel) or loader(rel)
                    options += (get_opts(to_pd, load_opt),)

            return exec.options(*options) if exec else options

        return get_opts(self._model)

    def __setitem__(self, rel, opt):
        self._override[rel] = opt


class LoadOptsMixin:
    _model: Type[DeclarativeBase]

    @classmethod
    def load_opts(cls) -> LoadOptions:
        return LoadOptions(cls)
