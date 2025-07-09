# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

from dataclasses import dataclass
from typing import Mapping, Optional, Type

from frogger2.constants import FAIR_DATASET_DOWNLOAD, NAME, PRIMARY_COLUMN, SCHEMA
from frogger2.types import Application, DatasetPrimaryPurpose


########################################
# Define the LoggerConfig schema here  #
########################################


"""
Add schema below, ensuring to extend the `Application` base type
"""


@dataclass
class FAIRDataset(Application):
    dataset_name: Optional[str] = None
    description: Optional[str] = None
    primary_purpose: DatasetPrimaryPurpose = DatasetPrimaryPurpose.EXPLORATION
    url: Optional[str] = None
    file_names: Optional[list[str]] = None
    download_temp_destination: Optional[str] = None
    download_perm_destination: Optional[str] = None
    oncall: Optional[str] = None


"""
Enumerate the application in this mapping
Expected format:
```
    name: {
        schema: Application,
        name: <LoggerConfig name>,
        primary_column: <main required input>,
    }
```
"""
APPLICATIONS: Mapping[str, Mapping[str, str | Type[Application]]] = {
    FAIR_DATASET_DOWNLOAD: {
        SCHEMA: FAIRDataset,
        NAME: "FAIRDatasetDownloadLoggerConfig",
        PRIMARY_COLUMN: "dataset_name",
    }
    # add yours below ...
}
