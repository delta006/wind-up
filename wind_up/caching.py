import pickle
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pandas as pd


def with_parquet_cache(fp: Path, *, use_cache: bool = True) -> Callable:
    def wrap(func: Callable[..., pd.DataFrame]) -> Callable[..., pd.DataFrame]:
        def wrapped_f(*a: Any, **kw: Any) -> pd.DataFrame:  # noqa
            if not Path(fp).is_file() or not use_cache:
                func(*a, **kw).to_parquet(fp)
            return pd.read_parquet(fp)

        return wrapped_f

    return wrap


def with_pickle_cache(fp: Path, *, use_cache: bool = True) -> Callable:
    def wrap(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapped_f(*a: Any, **kw: Any) -> Any:  # noqa
            if not Path(fp).is_file() or not use_cache:
                with Path.open(fp, "wb") as f:
                    pickle.dump(func(*a, **kw), f)
            with Path.open(fp, "rb") as f:
                return pickle.load(f)

        return wrapped_f

    return wrap
