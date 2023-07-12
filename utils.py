from collections.abc import Iterable
from pathlib import Path
from typing import Any

import pandas as pd


def save_jsonl(data: pd.DataFrame | Iterable[dict] | dict[Any, Iterable], path: Path | str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if type(data) != pd.DataFrame:
        data = pd.DataFrame(data)
    data.to_json(
        path,
        orient="records",
        lines=True,
        force_ascii=False,
    )


def load_jsonl(path: Path | str) -> list[dict]:
    path = Path(path)
    if not path.exists():
        return []
    return pd.read_json(path, lines=True).to_dict(orient="records")
