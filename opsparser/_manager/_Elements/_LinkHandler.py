from typing import Any

import openseespy.opensees as ops

from .._BaseHandler import SubBaseHandler


class LinkHandler(SubBaseHandler):
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

        # 添加不同节点元素类型的规则
        rules["twoNodeLink"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2"],
            "options": {
                "-mat": "matTags*",
                "-dir": "dirs*",
                "-orient?": [f"vecx*{ndm}", f"vecyp*{ndm}"],
                "-pDelta?": "pDeltaVals*",
                "-shearDist?": "sDratios*",
                "-doRayleigh?*0": "doRayleigh",
                "-mass?": "mass"
            }
        }

        return {"element": rules}

    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return [
            "twoNodeLink"
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "twoNodeLink": self._handle_twoNodeLink,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)


    def _handle_twoNodeLink(self, *args, **kwargs) -> dict[str, Any]:
        """处理 twoNodeLink 元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "matTags": arg_map.get("matTags", []),
            "dirs": arg_map.get("dirs", [])
        }

        # 处理可选参数
        if "vecx" in arg_map:
            eleinfo["vecx"] = arg_map.get("vecx")
        if "vecyp" in arg_map:
            eleinfo["vecyp"] = arg_map.get("vecyp")
        if "pDeltaVals" in arg_map:
            eleinfo["pDeltaVals"] = arg_map.get("pDeltaVals")
        if "sDratios" in arg_map:
            eleinfo["sDratios"] = arg_map.get("sDratios")
        if "-doRayleigh" in args:
            eleinfo["doRayleigh"] = True
        if "mass" in arg_map:
            eleinfo["mass"] = arg_map.get("mass")

        self.elements[eleTag] = eleinfo

    def _unknown(self, *args, **kwargs):
        # should never use this function but use ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()
