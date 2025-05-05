from typing import Any, Optional, Literal

from ._BaseHandler import BaseHandler


class NodeManager(BaseHandler):
    def __init__(self):
        self.nodes = {}  # tag -> {coords: [], mass: [], ndf: int}
        self.ndm = 0  # 模型维度
        self.ndf = 0  # 节点自由度数

    @property
    def newtag(self) -> int:
        """return a new tag that is unused"""
        return self.get_new_tags(1)[0]
    
    @property
    def newtag_upper(self):
        """return a new tag that is max of all tags + 1"""
        return max(self.nodes)+1
    
    def get_new_tags(self, num: int, start: int = 1) -> list[int]:
        """Generate a list of 'num' new node tags starting from at least 'start'"""
        if not self.nodes:
            return list(range(start, start + num))
        
        sorted_tags = sorted(self.nodes.keys())
        # Compute the first candidate tag: at least `start`, and after the smallest existing tag
        candidate = max(start, sorted_tags[0] + 1)
        if candidate>=sorted_tags[-1]:
            candidate = max(start, sorted_tags[-1] + 1)
            return list(range(candidate, candidate + num))

        for tag in sorted_tags:
            # If the gap before the current tag is large enough, use it
            if tag - candidate >= num:
                return list(range(candidate, candidate + num))
            # Otherwise, move the candidate just after this tag (skip used tags)
            if tag >= candidate:
                candidate = tag + 1

        # If no suitable gap was found inside existing tags, allocate tags after the last one
        return list(range(candidate, candidate + num))
    
    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        return {
            # node(nodeTag, *crds, '-ndf', ndf, '-mass', *mass, '-disp', ...)
            "node": {
                "positional": ["tag", "coords*"],
                "options": {
                    "-ndf?": "ndf",
                    "-mass?": "mass*",
                    "-disp?": "disp*",
                    "-vel?": "vel*",
                    "-accel?": "accel*",
                },
            },
            # mass(nodeTag, *massValues)
            "mass": {
                "positional": ["tag", "mass*"],
            },
            # model(type, *args)
            "model": {
                "positional": ["type"],
                "options": {
                    "-ndm": "ndm",
                    "-ndf?": "ndf",
                },
            },
        }

    def handles(self):
        return ["node", "mass", "model"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args,kwargs = arg_map.get("args"),arg_map.get("kwargs")
        if func_name == "node":
            self._handle_node(*args,**kwargs)
        elif func_name == "mass":
            self._handle_mass(*args,**kwargs)
        elif func_name == "model":
            self._handle_model(*args,**kwargs)

    def _handle_node(self, *args: Any, **kwargs: Any):
        arg_map = self._parse("node", *args, **kwargs)

        # 使用_parse处理的结果
        tag = arg_map.get("tag")
        if not tag:
            return

        coords = arg_map.get("coords", [])
        ndm = arg_map.get("ndm", self.ndm)
        ndf = arg_map.get("ndf", self.ndf)
        mass = arg_map.get("mass", [])
        disp = arg_map.get("disp", [])
        vel = arg_map.get("vel", [])
        accel = arg_map.get("accel", [])

        # 保存节点信息
        node_info = {"coords": coords, "ndm": ndm, "ndf": ndf}

        # 如果有质量信息, 也保存下来
        if mass and len(mass) == ndf:
            node_info["mass"] = mass

        if disp and len(disp) == ndf:
            node_info["disp"] = disp

        if vel and len(vel) == ndf:
            node_info["vel"] = vel

        if accel and len(accel) == ndf:
            node_info["accel"] = accel

        self.nodes[tag] = node_info

    def _handle_mass(self, *args: Any, **kwargs: Any):
        arg_map = self._parse("mass", *args, **kwargs)
        tag = arg_map.get("tag")
        if not tag:
            return

        mass_values = arg_map.get("mass", [])
        if not mass_values:
            return

        # 更新节点质量信息
        node_info = self.nodes.get(tag, {})
        node_info["mass"] = mass_values
        self.nodes[tag] = node_info

    def _handle_model(self, *args: Any, **kwargs: Any):
        arg_map = self._parse("model", *args, **kwargs)
        # 处理模型维度和自由度设置
        args = arg_map.get("args", [])

        # 检查是否有维度参数
        self.ndm = arg_map["ndm"]

        # 检查是否有自由度参数
        if "ndf" in arg_map:
            self.ndf = arg_map["ndf"]
        else:
            self.ndf = self.ndm*(self.ndm+1)/2

    def get_node_coords(self, tag: int) -> list[float]:
        """获取节点坐标"""
        node = self.nodes.get(tag, {})
        return node.get("coords", [])

    def get_node_mass(self, tag: int) -> list[float]:
        """获取节点质量"""
        node = self.nodes.get(tag, {})
        return node.get("mass", [])

    def get_nodes_by_coords(
        self, x: Optional[float] = None, y: Optional[float] = None, z: Optional[float] = None
    ) -> list[int]:
        """根据坐标查找节点"""
        result = []
        for tag, node in self.nodes.items():
            coords = node.get("coords", [])
            if len(coords) < 1:
                continue

            match = True
            if x is not None and (len(coords) < 1 or abs(coords[0] - x) > 1e-6):
                match = False
            if y is not None and (len(coords) < 2 or abs(coords[1] - y) > 1e-6):
                match = False
            if z is not None and (len(coords) < 3 or abs(coords[2] - z) > 1e-6):
                match = False

            if match:
                result.append(tag)

        return result

    def clear(self):
        self.nodes.clear()
        self.ndm = 0
        self.ndf = 0
