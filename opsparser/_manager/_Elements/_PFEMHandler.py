from typing import Any

import openseespy.opensees as ops

from .._BaseHandler import SubBaseHandler


class PFEMHandler(SubBaseHandler):
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
            rules["PFEMElementBubble"] = {
                "positional": ["eleType", "eleTag", "eleNodes*3", "rho", "mu", "b1", "b2", "thickness", "kappa?"],
            }
            rules["PFEMElementCompressible"] = {
                "positional": ["eleType", "eleTag", "eleNodes*4", "rho", "mu", "b1", "b2", "thickness?", "kappa?"],
            }
        elif ndm == 3:
            rules["PFEMElementBubble"] = {
                "positional": ["eleType", "eleTag", "eleNodes*4", "rho", "mu", "b1", "b2", "b3", "kappa?"],
            }
            # PFEMElementCompressible仅支持2D模式, 3D模式下没有定义

        return {"element": rules}

    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return [
            "PFEMElementBubble", "PFEMElementCompressible"
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "PFEMElementBubble": self._handle_PFEMElementBubble,
            "PFEMElementCompressible": self._handle_PFEMElementCompressible,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_PFEMElementBubble(self, *args, **kwargs) -> dict[str, Any]:
        """处理PFEMElementBubble元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        ndm = ops.getNDM()[0]

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "rho": arg_map.get("rho"),
            "mu": arg_map.get("mu"),
            "b1": arg_map.get("b1"),
            "b2": arg_map.get("b2"),
        }

        # 根据维度添加额外参数
        if ndm == 2:
            eleinfo["thickness"] = arg_map.get("thickness")
        elif ndm == 3:
            eleinfo["b3"] = arg_map.get("b3")

        # 可选参数kappa
        if arg_map.get("kappa"):
            eleinfo["kappa"] = arg_map.get("kappa")

        self.elements[eleTag] = eleinfo

    def _handle_PFEMElementCompressible(self, *args, **kwargs) -> dict[str, Any]:
        """处理PFEMElementCompressible元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        ndm = ops.getNDM()[0]

        # PFEMElementCompressible只支持2D
        if ndm != 2:
            raise NotImplementedError(f"PFEMElementCompressible only supports 2D, got ndm={ndm}")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "rho": arg_map.get("rho"),
            "mu": arg_map.get("mu"),
            "b1": arg_map.get("b1"),
            "b2": arg_map.get("b2"),
        }

        # 可选参数
        if arg_map.get("thickness"):
            eleinfo["thickness"] = arg_map.get("thickness")

        if arg_map.get("kappa"):
            eleinfo["kappa"] = arg_map.get("kappa")

        self.elements[eleTag] = eleinfo

    def _unknown(self, *args, **kwargs):
        # should never use this function but use ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()
