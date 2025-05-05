from collections import defaultdict
from copy import deepcopy
from typing import Any, Literal, Optional

from ._BaseHandler import BaseHandler
from ._Elements import (
    ZeroLengthHandler,
    TrussHandler,
    BeamColumnHandler,
    JointHandler,
    LinkHandler,
    BearingHandler,
    QuadrilateralHandler,
    TriangularHandler,
    BrickHandler,
    TetrahedronHandler,
    UCSDUpHandler,
    OtherUpHandler,
    ContactHandler,
    CableHandler,
    PFEMHandler,
    MiscHandler
)


class ElementManager(BaseHandler):
    def __init__(self):
        # 统一数据仓库
        self.elements: dict[int, dict] = {}

        # 构建 “命令 -> {eleType -> handler}” 映射
        self._command2typehandler: dict[str, dict[str, BaseHandler]] = defaultdict(dict)
        handler_classes = [
            ZeroLengthHandler,
            TrussHandler,
            BeamColumnHandler,
            JointHandler,
            LinkHandler,
            BearingHandler,
            QuadrilateralHandler,
            TriangularHandler,
            BrickHandler,
            TetrahedronHandler,
            UCSDUpHandler,
            OtherUpHandler,
            ContactHandler,
            CableHandler,
            PFEMHandler,
            MiscHandler
        ]
        for cls in handler_classes:
            cmd = cls.handles()[0]
            for typ in cls.types():
                self._command2typehandler[cmd][typ] = cls(self._command2typehandler[cmd], self.elements)

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        """聚合各子 Handler 的 rule"""
        merged: defaultdict[str, dict[str, Any]] = defaultdict(lambda: defaultdict(lambda: deepcopy({"positional": ["eleType", "eleTag", "args*"]})))
        for t2h in self._command2typehandler.values():
            for h in set(t2h.values()):
                for k, v in h._COMMAND_RULES.items():
                    merged[k].update(v)
        return merged

    @staticmethod
    def handles():
        return ["element"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        eleType = arg_map["args"][0]
        registry = self._command2typehandler.get(func_name, {})
        handler = registry.get(eleType)
        if handler:
            handler.handle(func_name, arg_map)
        else:
            self.handle_unknown_element(*arg_map["args"], **arg_map["kwargs"])

    def handle_unknown_element(self, *args, **kwargs):
        """Handle unknown elements"""
        arg_map = self._parse("element", *args, **kwargs)

        eleType = arg_map.get("eleType")
        eleTag = arg_map.get("eleTag")
        args = arg_map.get("args",[])
        eleinfo = {
            "eleType": eleType,
            "eleTag": eleTag,
            "args": args,
        }
        self.elements[eleTag] = eleinfo

    def get_element(self, eleTag: int) -> Optional[dict]:
        """Get element information by tag"""
        return self.elements.get(eleTag)

    def get_element_nodes(self, eleTag: int) -> list[int]:
        """Get nodes connected to the specified element"""
        return self.elements.get(eleTag).get("eleNodes",[])

    def get_elements_by_nodes(self, node_tags: list[int]) -> list[int]:
        """Get all elements connected to the specified nodes"""
        result = []
        for elem_tag, info in self.elements.items():
            if all(node in info["eleNodes"] for node in node_tags):
                result.append(elem_tag)
        return result

    def get_elements_by_type(self, eleType: str) -> list[int]:
        """Get all elements of the specified type"""
        return [tag for tag, data in self.elements.items() if data.get("eleType", "").lower() == eleType.lower()]

    def get_elements(
            self,
            Type: Optional[Literal[
                "zerolength", "truss", "beamcolumn", "joint", "link",
                "bearing", "quadrilateral", "triangular", "brick",
                "tetrahedron", "ucsd_up", "other_up", "contact",
                "cable", "pfem", "misc"]] = None
        ):
        """Get elements by type"""
        if Type is None:
            return self.elements

        element_types = {
            "zerolength": ZeroLengthHandler.types(),
            "truss": TrussHandler.types(),
            "beamcolumn": BeamColumnHandler.types(),
            "joint": JointHandler.types(),
            "link": LinkHandler.types(),
            "bearing": BearingHandler.types(),
            "quadrilateral": QuadrilateralHandler.types(),
            "triangular": TriangularHandler.types(),
            "brick": BrickHandler.types(),
            "tetrahedron": TetrahedronHandler.types(),
            "ucsd_up": UCSDUpHandler.types(),
            "other_up": OtherUpHandler.types(),
            "contact": ContactHandler.types(),
            "cable": CableHandler.types(),
            "pfem": PFEMHandler.types(),
            "misc": MiscHandler.types()
        }

        element_list = []
        for eleType in element_types[Type]:
            element_list.extend([tag for tag, data in self.elements.items() if data.get("eleType", "") == eleType])

        return element_list

    def clear(self):
        self.elements.clear()
