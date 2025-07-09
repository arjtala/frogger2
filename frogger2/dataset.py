# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import logging
import os
from typing import Optional, Type

from frogger2.applications import APPLICATIONS, Application
from frogger2.constants import FAIR_DATASET_DOWNLOAD, NAME, PRIMARY_COLUMN, SCHEMA
from frogger2.types import Application, DatasetPrimaryPurpose
from frogger2.utilities import TeeLogExporter

from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import (
    LoggerProvider,
    LoggingHandler,
)
from opentelemetry.sdk._logs.export import (
    BatchLogRecordProcessor,
    ConsoleLogExporter,
)
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

logger: logging.Logger = logging.getLogger(__name__)

def log_dataset(
    dataset_name: Optional[str] = None,
    description: Optional[str] = None,
    primary_purpose: Optional[str] = "exploration",
    url: Optional[str] = None,
    file_names: Optional[list[str]] = None,
    download_temp_destination: Optional[str] = None,
    download_perm_destination: Optional[str] = None,
    oncall: Optional[str] = None,
    gateway: Optional[str] = None,
):
    OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "")
    logger.debug(f"OTel Endpoint: {OTEL_EXPORTER_OTLP_ENDPOINT}")

    _primary_purpose: DatasetPrimaryPurpose = DatasetPrimaryPurpose.EXPLORATION
    try:
        _primary_purpose = DatasetPrimaryPurpose[primary_purpose]
    except Exception as e:
        logger.warning(
            f"Unable to infer dataset purpose (`{primary_purpose}`), "
            + f"defaulting to {DatasetPrimaryPurpose.EXPLORATION.name}`"
        )
    app: Type[Application] = APPLICATIONS[FAIR_DATASET_DOWNLOAD][SCHEMA]
    name: str = APPLICATIONS[FAIR_DATASET_DOWNLOAD][NAME]
    primary_column: str = APPLICATIONS[FAIR_DATASET_DOWNLOAD].get(PRIMARY_COLUMN, "")
    payload = app(
        dataset_name=dataset_name,
        description=description,
        primary_purpose=_primary_purpose,
        url=url,
        file_names=file_names,
        download_temp_destination=download_temp_destination,
        download_perm_destination=download_perm_destination,
        oncall=oncall,
    ).to_dict(primary_column)

    resource = Resource(
        attributes={
            SERVICE_NAME: FAIR_DATASET_DOWNLOAD,
            "fb.logs.structuredapi.loggerconfig": name,
            "fb.logs.structuredapi.log_body_column": "dataset",
        }
    )
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)
    exporter = TeeLogExporter(
        exporters=[
            ConsoleLogExporter(),
            OTLPLogExporter(
                endpoint=OTEL_EXPORTER_OTLP_ENDPOINT,
                timeout=5,
            ),
        ],
    )
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

    logging.getLogger().setLevel(logging.NOTSET)

    # Attach OTLP handler to root logger
    logging.getLogger().addHandler(handler)
    otel_logger = logging.getLogger("fair_dataset_download")
    otel_logger.info(dataset_name, extra=payload)
    logger_provider.shutdown()
