from typing import Any

import openseespy.opensees as ops

from .._BaseHandler import SubBaseHandler


class TriangularHandler(SubBaseHandler):
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

        rules["Tri31"] = {
            "positional": ["eleType", "eleTag", "eleNodes*3", "thick", "type", "matTag"],
            "options": {
                "pressure?": "pressure",
                "rho?": "rho",
                "b1?": "b1",
                "b2?": "b2"
            }
        }
        return {"element": rules}

    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return [
            "Tri31"
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "Tri31": self._handle_Tri31,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)


    def _handle_Tri31(self, *args, **kwargs) -> dict[str, Any]:
        """Handle Tri31 triangular element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "thick": arg_map.get("thick"),
            "type": arg_map.get("type"),
            "matTag": arg_map.get("matTag")
        }

        # 处理可选参数
        if 'pressure' in arg_map:
            eleinfo['pressure'] = arg_map.get('pressure', 0.0)

        if 'rho' in arg_map:
            eleinfo['rho'] = arg_map.get('rho', 0.0)

        if 'b1' in arg_map:
            eleinfo['b1'] = arg_map.get('b1', 0.0)

        if 'b2' in arg_map:
            eleinfo['b2'] = arg_map.get('b2', 0.0)

        self.elements[eleTag] = eleinfo

    def _unknown(self, *args, **kwargs):
        # should never use this function but use ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()
