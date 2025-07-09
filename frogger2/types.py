# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Mapping, Optional


@dataclass
class Application:
    def to_dict(self, exclude_key: Optional[str] = "") -> Mapping[str, Any]:
        def _dict_factory(data, exclude_key: Optional[str] = ""):
            return {k: v for k, v in data if k != exclude_key}

        asdict(self, dict_factory=_dict_factory)


class DatasetPrimaryPurpose(Enum):
    TRAINING = 1
    BENCHMARKING = 2
    EVALUATION = 3
    FINE_TUNING = 4
    EXPLORATION = 5
    MULTI_PURPOSE = 6
    OTHER = 7
    TEST = 8
