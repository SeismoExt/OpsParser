from typing import Any

import openseespy.opensees as ops

from .._BaseHandler import SubBaseHandler


class TetrahedronHandler(SubBaseHandler):
    def __init__(self, registry: dict[str, dict], element_store: dict[int, dict]):
        """
        registry: eleType → handler  的全局映射 (供 manager 生成)
        element_store: ElementManager.elements 共享引用
        """
        self.elements = element_store
        self._register(registry)

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        rules = {"alternative": True}

        # 添加不同元素类型的规则
        rules["FourNodeTetrahedron"] = {
            "positional": ["eleType", "eleTag", "eleNodes*4", "matTag", "b1?", "b2?", "b3?"],
        }

        return {"element": rules}

    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return [
            "FourNodeTetrahedron"
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "FourNodeTetrahedron": self._handle_FourNodeTetrahedron,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _unknown(self, *args, **kwargs):
        # should never use this function but use ElementManager.handle_unknown_element()
        raise NotImplementedError

    def _handle_FourNodeTetrahedron(self, *args, **kwargs) -> dict[str, Any]:
        """Handle FourNodeTetrahedron element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "matTag": arg_map.get("matTag"),
        }

        # 处理可选体力参数
        if "b1" in arg_map:
            eleinfo["b1"] = arg_map.get("b1")
        if "b2" in arg_map:
            eleinfo["b2"] = arg_map.get("b2")
        if "b3" in arg_map:
            eleinfo["b3"] = arg_map.get("b3")

        self.elements[eleTag] = eleinfo

    def clear(self):
        self.elements.clear()
