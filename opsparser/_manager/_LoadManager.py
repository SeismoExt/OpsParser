from ._BaseHandler import BaseHandler
from typing import Any, Optional


class LoadManager(BaseHandler):
    def __init__(self):
        self.patterns = {}  # 荷载模式: tag -> {type, tsTag, ...}
        self.node_loads = {}  # 节点荷载: (patternTag, nodeTag) -> values
        self.ele_loads = {}  # 单元荷载: (patternTag, eleTag) -> values
        self.current_pattern = None  # 当前荷载模式

    def handles(self):
        return ["pattern", "load", "eleLoad"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        if func_name == "pattern":
            self._handle_pattern(arg_map)
        elif func_name == "load":
            self._handle_load(arg_map)
        elif func_name == "eleLoad":
            self._handle_eleLoad(arg_map)

    def _handle_pattern(self, arg_map: dict[str, Any]):
        """处理荷载模式命令"""
        # pattern patternType? patternTag tsTag <-factor factor>?
        pattern_type = arg_map.get("typeName", "")
        tag = arg_map.get("tag", 0)
        args = arg_map.get("args", [])

        if not pattern_type or tag == 0 or not args:
            return

        # 第一个参数通常是时程标签
        ts_tag = int(args[0])

        pattern_info = {"type": pattern_type, "tsTag": ts_tag}

        # 检查是否有factor选项
        if "-factor" in args and args.index("-factor") + 1 < len(args):
            factor_idx = args.index("-factor") + 1
            pattern_info["factor"] = float(args[factor_idx])

        self.patterns[tag] = pattern_info
        # 更新当前荷载模式
        self.current_pattern = tag

    def _handle_load(self, arg_map: dict[str, Any]):
        """处理节点荷载命令"""
        # load nodeTag? <Fx Fy Fz Mx My Mz>?
        tag = arg_map.get("tag")  # 节点标签
        args = arg_map.get("args", [])  # 荷载分量

        if tag is None or not args:
            return

        # 使用当前荷载模式
        pattern_tag = self.current_pattern
        if pattern_tag is None:
            return

        # 存储节点荷载，键为(荷载模式标签, 节点标签)元组
        load_key = (pattern_tag, tag)
        self.node_loads[load_key] = args

    def _handle_eleLoad(self, arg_map: dict[str, Any]):
        """处理单元荷载命令"""
        # eleLoad -ele eleTag1 eleTag2 ... -type -beamUniform Wy <Wz> ...
        # 或 eleLoad -range startEleTag endEleTag -type -beamUniform ...
        args = arg_map.get("args", [])

        # 获取荷载类型
        load_type = ""
        if "-type" in args and args.index("-type") + 1 < len(args):
            type_idx = args.index("-type") + 1
            load_type = args[type_idx]

        # 提取单元标签列表
        ele_tags = []

        # 检查是否有-ele选项
        if "-ele" in args:
            ele_idx = args.index("-ele") + 1
            while ele_idx < len(args) and not args[ele_idx].startswith("-"):
                try:
                    ele_tags.append(int(args[ele_idx]))
                    ele_idx += 1
                except (ValueError, TypeError):
                    break

        # 检查是否有-range选项
        if "-range" in args and args.index("-range") + 2 < len(args):
            range_idx = args.index("-range")
            start_tag = int(args[range_idx + 1])
            end_tag = int(args[range_idx + 2])
            ele_tags.extend(range(start_tag, end_tag + 1))

        # 提取荷载分量值
        load_values = []

        # 对于-beamUniform类型的荷载
        if load_type == "-beamUniform" and "-beamUniform" in args:
            beam_idx = args.index("-beamUniform") + 1
            while beam_idx < len(args) and not args[beam_idx].startswith("-"):
                try:
                    load_values.append(float(args[beam_idx]))
                    beam_idx += 1
                except (ValueError, TypeError):
                    break

        # 使用当前荷载模式
        pattern_tag = self.current_pattern
        if pattern_tag is None:
            return

        # 存储每个单元的荷载
        for ele_tag in ele_tags:
            load_key = (pattern_tag, ele_tag)
            self.ele_loads[load_key] = {"type": load_type, "values": load_values}

    def get_pattern(self, tag: int) -> Optional[dict]:
        """获取指定标签的荷载模式"""
        return self.patterns.get(tag)

    def get_node_load(self, pattern_tag: int, node_tag: int) -> list[float]:
        """获取指定荷载模式下节点的荷载"""
        return self.node_loads.get((pattern_tag, node_tag), [])

    def get_ele_load(self, pattern_tag: int, ele_tag: int) -> dict:
        """获取指定荷载模式下单元的荷载"""
        return self.ele_loads.get((pattern_tag, ele_tag), {})

    def get_patterns_by_time_series(self, ts_tag: int) -> list[int]:
        """获取使用特定时程的所有荷载模式"""
        return [tag for tag, info in self.patterns.items() if info.get("tsTag") == ts_tag]

    def clear(self):
        """清除所有数据"""
        self.patterns.clear()
        self.node_loads.clear()
        self.ele_loads.clear()
        self.current_pattern = None
