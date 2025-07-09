# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

from typing import Sequence

from opentelemetry.sdk._logs._internal import LogData
from opentelemetry.sdk._logs.export import (
    LogExporter,
    LogExportResult,
)


class TeeLogExporter(LogExporter):
    """Exporter that writes to multiple exporters."""

    def __init__(
        self,
        exporters: list[LogExporter],
    ):
        self._exporters = exporters

    def export(self, batch: Sequence[LogData]):
        for e in self._exporters:
            e.export(batch)
        return LogExportResult.SUCCESS

    def shutdown(self):
        for e in self._exporters:
            e.shutdown()
