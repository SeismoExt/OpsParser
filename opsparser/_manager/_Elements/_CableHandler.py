from typing import Any

from .._BaseHandler import SubBaseHandler


class CableHandler(SubBaseHandler):
    def __init__(self, registry: dict[str, dict], element_store: dict[int, dict]):
        """
        registry: eleType → handler 的全局映射 (供 manager 生成)
        element_store: ElementManager.elements 共享引用
        """
        self.elements = element_store
        self._register(registry)

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        rules = {"alternative": True}

        # 添加 CatenaryCable 元素类型规则
        rules["CatenaryCable"] = {
            "positional": ["eleType", "eleTag", "iNode", "jNode", "weight", "E", "A", "L0",
                           "alpha", "temperature_change", "rho", "errorTol", "Nsubsteps", "massType"],
        }

        return {"element": rules}

    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return [
            "CatenaryCable"
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "CatenaryCable": self._handle_CatenaryCable,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_CatenaryCable(self, *args, **kwargs) -> dict[str, Any]:
        """处理 CatenaryCable 元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "iNode": arg_map.get("iNode"),
            "jNode": arg_map.get("jNode"),
            "weight": arg_map.get("weight"),
            "E": arg_map.get("E"),
            "A": arg_map.get("A"),
            "L0": arg_map.get("L0"),
            "alpha": arg_map.get("alpha"),
            "temperature_change": arg_map.get("temperature_change"),
            "rho": arg_map.get("rho"),
            "errorTol": arg_map.get("errorTol"),
            "Nsubsteps": arg_map.get("Nsubsteps"),
            "massType": arg_map.get("massType"),
        }

        self.elements[eleTag] = eleinfo

    def _unknown(self, *args, **kwargs):
        # 永远不应该使用此函数，而应该使用 ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()
