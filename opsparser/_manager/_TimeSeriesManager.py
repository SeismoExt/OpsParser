from ._BaseHandler import BaseHandler
from typing import Any


class TimeSeriesManager(BaseHandler):
    def __init__(self):
        self.time_series = {}

    def handles(self):
        return ["timeSeries"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        if func_name == "timeSeries":
            self._handle_time_series(arg_map)

    def _handle_time_series(self, arg_map: dict[str, Any]):
        tag = arg_map.get("tag")
        if not tag:
            return

        series_type = arg_map.get("type")
        if not series_type:
            return

        series_values = arg_map.get("values", [])
        if not series_values:
            return

        # 保存时间序列信息
        self.time_series[tag] = {"type": series_type, "values": series_values}
