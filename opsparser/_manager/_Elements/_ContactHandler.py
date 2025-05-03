from typing import Any

from .._BaseHandler import SubBaseHandler


class ContactHandler(SubBaseHandler):
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

        # 添加不同接触元素类型的规则
        rules["SimpleContact2D"] = {
            "positional": ["eleType", "eleTag", "iNode", "jNode", "cNode", "lNode", "matTag", "gTol", "fTol"],
            "options": {}
        }

        rules["SimpleContact3D"] = {
            "positional": ["eleType", "eleTag", "iNode", "jNode", "kNode", "lNode", "cNode", "lagr_node", "matTag", "gTol", "fTol"],
            "options": {}
        }

        rules["BeamContact2D"] = {
            "positional": ["eleType", "eleTag", "iNode", "jNode", "sNode", "lNode", "matTag", "width", "gTol", "fTol", "cFlag?"],
        }

        rules["BeamContact3D"] = {
            "positional": ["eleType", "eleTag", "iNode", "jNode", "cNode", "lNode", "radius", "crdTransf", "matTag", "gTol", "fTol", "cFlag?"],
        }

        rules["BeamEndContact3D"] = {
            "positional": ["eleType", "eleTag", "iNode", "jNode", "cNode", "lNode", "radius", "gTol", "fTol", "cFlag?"],
        }
        return {"element": rules}

    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return [
            "SimpleContact2D", "SimpleContact3D", "BeamContact2D", "BeamContact3D", "BeamEndContact3D"
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "SimpleContact2D": self._handle_SimpleContact2D,
            "SimpleContact3D": self._handle_SimpleContact3D,
            "BeamContact2D": self._handle_BeamContact2D,
            "BeamContact3D": self._handle_BeamContact3D,
            "BeamEndContact3D": self._handle_BeamEndContact3D,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_SimpleContact2D(self, *args, **kwargs) -> dict[str, Any]:
        """处理 SimpleContact2D 元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "iNode": arg_map.get("iNode"),
            "jNode": arg_map.get("jNode"),
            "cNode": arg_map.get("cNode"),
            "lNode": arg_map.get("lNode"),
            "matTag": arg_map.get("matTag"),
            "gTol": arg_map.get("gTol"),
            "fTol": arg_map.get("fTol")
        }

        self.elements[eleTag] = eleinfo

    def _handle_SimpleContact3D(self, *args, **kwargs) -> dict[str, Any]:
        """处理 SimpleContact3D 元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "iNode": arg_map.get("iNode"),
            "jNode": arg_map.get("jNode"),
            "kNode": arg_map.get("kNode"),
            "lNode": arg_map.get("lNode"),
            "cNode": arg_map.get("cNode"),
            "lagr_node": arg_map.get("lagr_node"),
            "matTag": arg_map.get("matTag"),
            "gTol": arg_map.get("gTol"),
            "fTol": arg_map.get("fTol")
        }

        self.elements[eleTag] = eleinfo

    def _handle_BeamContact2D(self, *args, **kwargs) -> dict[str, Any]:
        """处理 BeamContact2D 元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "iNode": arg_map.get("iNode"),
            "jNode": arg_map.get("jNode"),
            "sNode": arg_map.get("sNode"),
            "lNode": arg_map.get("lNode"),
            "matTag": arg_map.get("matTag"),
            "width": arg_map.get("width"),
            "gTol": arg_map.get("gTol"),
            "fTol": arg_map.get("fTol")
        }

        # 处理可选参数
        if 'cFlag' in arg_map:
            eleinfo['cFlag'] = arg_map.get('cFlag', 0)

        self.elements[eleTag] = eleinfo

    def _handle_BeamContact3D(self, *args, **kwargs) -> dict[str, Any]:
        """处理 BeamContact3D 元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "iNode": arg_map.get("iNode"),
            "jNode": arg_map.get("jNode"),
            "cNode": arg_map.get("cNode"),
            "lNode": arg_map.get("lNode"),
            "radius": arg_map.get("radius"),
            "crdTransf": arg_map.get("crdTransf"),
            "matTag": arg_map.get("matTag"),
            "gTol": arg_map.get("gTol"),
            "fTol": arg_map.get("fTol")
        }

        # 处理可选参数
        if 'cFlag' in arg_map:
            eleinfo['cFlag'] = arg_map.get('cFlag', 0)

        self.elements[eleTag] = eleinfo

    def _handle_BeamEndContact3D(self, *args, **kwargs) -> dict[str, Any]:
        """处理 BeamEndContact3D 元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "iNode": arg_map.get("iNode"),
            "jNode": arg_map.get("jNode"),
            "cNode": arg_map.get("cNode"),
            "lNode": arg_map.get("lNode"),
            "radius": arg_map.get("radius"),
            "gTol": arg_map.get("gTol"),
            "fTol": arg_map.get("fTol")
        }

        # 处理可选参数
        if 'cFlag' in arg_map:
            eleinfo['cFlag'] = arg_map.get('cFlag', 0)

        self.elements[eleTag] = eleinfo

    def _unknown(self, *args, **kwargs):
        # should never use this function but use ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()
