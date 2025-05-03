from typing import Any

import openseespy.opensees as ops

from .._BaseHandler import SubBaseHandler


class MiscHandler(SubBaseHandler):
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

        # SurfaceLoad元素只适用于3D模型
        if ndm == 3:
            rules["SurfaceLoad"] = {
                "positional": ["eleType", "eleTag", "eleNodes*4", "p"],
            }

        # VS3D4 - 四节点3D粘弹性边界四边形元素
        rules["VS3D4"] = {
            "positional": ["eleType", "eleTag", "eleNodes*4", "E", "G", "rho", "R", "alphaN", "alphaT"],
        }

        # AC3D8 - 八节点3D声学砖元素
        rules["AC3D8"] = {
            "positional": ["eleType", "eleTag", "eleNodes*8", "matTag"],
        }

        # ASI3D8 - 八节点零厚度3D声学-结构接口元素
        rules["ASI3D8"] = {
            "positional": ["eleType", "eleTag", "eleNodes1*4", "eleNodes2*4"],
        }

        # AV3D4 - 四节点3D声学粘性边界元素
        rules["AV3D4"] = {
            "positional": ["eleType", "eleTag", "eleNodes*4", "matTag"],
        }

        # MasonPan12 - 12节点砌体面板元素
        rules["MasonPan12"] = {
            "positional": ["eleType", "eleTag", "eleNodes*12", "mat_1", "mat_2", "thick", "w_tot", "w_1"],
        }
        return {"element": rules}

    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return [
            "SurfaceLoad", "VS3D4", "AC3D8", "ASI3D8", "AV3D4", "MasonPan12"
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "SurfaceLoad": self._handle_SurfaceLoad,
            "VS3D4": self._handle_VS3D4,
            "AC3D8": self._handle_AC3D8,
            "ASI3D8": self._handle_ASI3D8,
            "AV3D4": self._handle_AV3D4,
            "MasonPan12": self._handle_MasonPan12,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_SurfaceLoad(self, *args, **kwargs) -> dict[str, Any]:
        """处理SurfaceLoad元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "p": arg_map.get("p"),
        }

        self.elements[eleTag] = eleinfo

    def _handle_VS3D4(self, *args, **kwargs) -> dict[str, Any]:
        """处理VS3D4元素 - 四节点3D粘弹性边界四边形元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "E": arg_map.get("E"),
            "G": arg_map.get("G"),
            "rho": arg_map.get("rho"),
            "R": arg_map.get("R"),
            "alphaN": arg_map.get("alphaN"),
            "alphaT": arg_map.get("alphaT"),
        }

        self.elements[eleTag] = eleinfo

    def _handle_AC3D8(self, *args, **kwargs) -> dict[str, Any]:
        """处理AC3D8元素 - 八节点3D声学砖元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "matTag": arg_map.get("matTag"),
        }

        self.elements[eleTag] = eleinfo

    def _handle_ASI3D8(self, *args, **kwargs) -> dict[str, Any]:
        """处理ASI3D8元素 - 八节点零厚度3D声学-结构接口元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes1": arg_map.get("eleNodes1", []),
            "eleNodes2": arg_map.get("eleNodes2", []),
        }

        self.elements[eleTag] = eleinfo

    def _handle_AV3D4(self, *args, **kwargs) -> dict[str, Any]:
        """处理AV3D4元素 - 四节点3D声学粘性边界元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "matTag": arg_map.get("matTag"),
        }

        self.elements[eleTag] = eleinfo

    def _handle_MasonPan12(self, *args, **kwargs) -> dict[str, Any]:
        """处理MasonPan12元素 - 12节点砌体面板元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "mat_1": arg_map.get("mat_1"),
            "mat_2": arg_map.get("mat_2"),
            "thick": arg_map.get("thick"),
            "w_tot": arg_map.get("w_tot"),
            "w_1": arg_map.get("w_1"),
        }

        self.elements[eleTag] = eleinfo

    def _unknown(self, *args, **kwargs):
        # should never use this function but use ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()
