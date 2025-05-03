from typing import Any

import openseespy.opensees as ops

from .._BaseHandler import SubBaseHandler


class OtherUpHandler(SubBaseHandler):
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

        # ndm for 2D/3D if needed
        ndm = ops.getNDM()[0]
        assert len(ops.getNDM()) == 1, f"Invalid length of ndm, expected 1, got {len(ops.getNDM()) =}"  # noqa: S101

        # 添加不同元素类型的规则
        if ndm == 2:
            rules["SSPquadUP"] = {
                "positional": ["eleType", "eleTag", "eleNodes*4", "matTag", "thick", "fBulk", "fDen", "k1", "k2", "void", "alpha", "b1?", "b2?"],
            }
        elif ndm == 3:
            rules["SSPbrickUP"] = {
                "positional": ["eleType", "eleTag", "eleNodes*8", "matTag", "fBulk", "fDen", "k1", "k2", "k3", "void", "alpha", "b1?", "b2?", "b3?"],
            }
        else:
            raise NotImplementedError(f"Invalid {ndm =} for `SSPquadUP` or `SSPbrickUP`")

        return {"element": rules}

    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return [
            "SSPquadUP", "SSPbrickUP"
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "SSPquadUP": self._handle_SSPquadUP,
            "SSPbrickUP": self._handle_SSPbrickUP,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_SSPquadUP(self, *args, **kwargs) -> dict[str, Any]:
        """处理 SSPquadUP 元素"""
        # 解析命令参数
        arg_map = self._parse("element", *args, **kwargs)

        # 获取元素标签
        eleTag = arg_map.get("eleTag")

        # 创建元素信息字典
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "matTag": arg_map.get("matTag"),
            "thick": arg_map.get("thick"),
            "fBulk": arg_map.get("fBulk"),
            "fDen": arg_map.get("fDen"),
            "k1": arg_map.get("k1"),
            "k2": arg_map.get("k2"),
            "void": arg_map.get("void"),
            "alpha": arg_map.get("alpha"),
        }

        # 处理可选参数
        if 'b1' in arg_map:
            eleinfo['b1'] = arg_map.get('b1', 0.0)
        else:
            eleinfo['b1'] = 0.0

        if 'b2' in arg_map:
            eleinfo['b2'] = arg_map.get('b2', 0.0)
        else:
            eleinfo['b2'] = 0.0

        # 将元素信息存储到元素字典中
        self.elements[eleTag] = eleinfo

        return eleinfo

    def _handle_SSPbrickUP(self, *args, **kwargs) -> dict[str, Any]:
        """处理 SSPbrickUP 元素"""
        # 解析命令参数
        arg_map = self._parse("element", *args, **kwargs)

        # 获取元素标签
        eleTag = arg_map.get("eleTag")

        # 创建元素信息字典
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "matTag": arg_map.get("matTag"),
            "fBulk": arg_map.get("fBulk"),
            "fDen": arg_map.get("fDen"),
            "k1": arg_map.get("k1"),
            "k2": arg_map.get("k2"),
            "k3": arg_map.get("k3"),
            "void": arg_map.get("void"),
            "alpha": arg_map.get("alpha"),
        }

        # 处理可选参数
        if 'b1' in arg_map:
            eleinfo['b1'] = arg_map.get('b1', 0.0)
        else:
            eleinfo['b1'] = 0.0

        if 'b2' in arg_map:
            eleinfo['b2'] = arg_map.get('b2', 0.0)
        else:
            eleinfo['b2'] = 0.0

        if 'b3' in arg_map:
            eleinfo['b3'] = arg_map.get('b3', 0.0)
        else:
            eleinfo['b3'] = 0.0

        # 将元素信息存储到元素字典中
        self.elements[eleTag] = eleinfo

        return eleinfo

    def _unknown(self, *args, **kwargs):
        # 永远不应使用此函数, 而应使用 ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()
