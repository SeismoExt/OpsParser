from typing import Any

import openseespy.opensees as ops

from .._BaseHandler import SubBaseHandler


class QuadrilateralHandler(SubBaseHandler):
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

        # 添加四边形单元类型的规则
        if ndm == 2:
            # 四节点四边形单元
            rules["quad"] = {
                "positional": ["eleType", "eleTag", "eleNodes*4", "thick", "type", "matTag"],
                "options": {
                    "pressure?": "pressure",
                    "rho?": "rho",
                    "b1?": "b1",
                    "b2?": "b2",
                }
            }

            # 带B-bar的平面应变四边形单元
            rules["bbarQuad"] = {
                "positional": ["eleType", "eleTag", "eleNodes*4", "thick", "matTag"],
                "options": {}
            }

            # 增强应变四边形单元
            rules["enhancedQuad"] = {
                "positional": ["eleType", "eleTag", "eleNodes*4", "thick", "type", "matTag"],
                "options": {}
            }

            # 稳定单点积分四边形元素
            rules["SSPquad"] = {
                "positional": ["eleType", "eleTag", "eleNodes*4", "matTag", "type", "thick"],
                "options": {
                    "b1?": "b1",
                    "b2?": "b2",
                }
            }

        # 3D空间壳单元
        if ndm == 3:
            # MITC4壳单元
            rules["ShellMITC4"] = {
                "positional": ["eleType", "eleTag", "eleNodes*4", "secTag"],
                "options": {}
            }

            # DKGQ壳单元
            rules["ShellDKGQ"] = {
                "positional": ["eleType", "eleTag", "eleNodes*4", "secTag"],
                "options": {}
            }

            # DKGT壳单元
            rules["ShellDKGT"] = {
                "positional": ["eleType", "eleTag", "eleNodes*3", "secTag"],
                "options": {}
            }

            # 非线性DKGQ壳单元
            rules["ShellNLDKGQ"] = {
                "positional": ["eleType", "eleTag", "eleNodes*4", "secTag"],
                "options": {}
            }

            # 非线性DKGT壳单元
            rules["ShellNLDKGT"] = {
                "positional": ["eleType", "eleTag", "eleNodes*3", "secTag"],
                "options": {}
            }

            # 非线性ShellNL壳单元
            rules["ShellNL"] = {
                "positional": ["eleType", "eleTag", "eleNodes*9", "secTag"],
                "options": {}
            }

            # 3D MVLEM元素
            rules["MVLEM_3D"] = {
                "positional": ["eleType", "eleTag", "eleNodes*4", "m"],
                "options": {
                    "-thick?": "thick*",
                    "-width?": "widths*",
                    "-rho?": "rho*",
                    "-matConcrete?": "matConcreteTags*",
                    "-matSteel?": "matSteelTags*",
                    "-matShear?": "matShearTag",
                    "-CoR?": "c",
                    "-ThickMod?": "tMod",
                    "-Poisson?": "Nu",
                    "-Density?": "Dens",
                }
            }

            # 3D SFI_MVLEM元素
            rules["SFI_MVLEM_3D"] = {
                "positional": ["eleType", "eleTag", "eleNodes*4", "m"],
                "options": {
                    "-thick?": "thicks*",
                    "-width?": "widths*",
                    "-mat?": "matTags*",
                    "-CoR?": "c",
                    "-ThickMod?": "tMod",
                    "-Poisson?": "Nu",
                    "-Density?": "Dens",
                }
            }

        return {"element": rules}

    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return [
            "quad", "ShellMITC4", "ShellDKGQ", "ShellDKGT",
            "ShellNLDKGQ", "ShellNLDKGT", "ShellNL",
            "bbarQuad", "enhancedQuad", "SSPquad",
            "MVLEM_3D", "SFI_MVLEM_3D"
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "quad": self._handle_quad,
            "ShellMITC4": self._handle_ShellMITC4,
            "ShellDKGQ": self._handle_ShellDKGQ,
            "ShellDKGT": self._handle_ShellDKGT,
            "ShellNLDKGQ": self._handle_ShellNLDKGQ,
            "ShellNLDKGT": self._handle_ShellNLDKGT,
            "ShellNL": self._handle_ShellNL,
            "bbarQuad": self._handle_bbarQuad,
            "enhancedQuad": self._handle_enhancedQuad,
            "SSPquad": self._handle_SSPquad,
            "MVLEM_3D": self._handle_MVLEM_3D,
            "SFI_MVLEM_3D": self._handle_SFI_MVLEM_3D,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_quad(self, *args, **kwargs) -> dict[str, Any]:
        """处理四节点四边形单元"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "thick": arg_map.get("thick"),
            "type": arg_map.get("type"),  # PlaneStrain 或 PlaneStress
            "matTag": arg_map.get("matTag"),
        }

        # 处理可选参数
        if "pressure" in arg_map:
            eleinfo["pressure"] = arg_map.get("pressure", 0.0)

        if "rho" in arg_map:
            eleinfo["rho"] = arg_map.get("rho", 0.0)

        if "b1" in arg_map:
            eleinfo["b1"] = arg_map.get("b1", 0.0)

        if "b2" in arg_map:
            eleinfo["b2"] = arg_map.get("b2", 0.0)

        self.elements[eleTag] = eleinfo

    def _handle_ShellMITC4(self, *args, **kwargs) -> dict[str, Any]:
        """处理MITC4壳单元"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "secTag": arg_map.get("secTag"),
        }

        self.elements[eleTag] = eleinfo

    def _handle_ShellDKGQ(self, *args, **kwargs) -> dict[str, Any]:
        """处理DKGQ壳单元"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "secTag": arg_map.get("secTag"),
        }

        self.elements[eleTag] = eleinfo

    def _handle_ShellDKGT(self, *args, **kwargs) -> dict[str, Any]:
        """处理DKGT三角形壳单元"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "secTag": arg_map.get("secTag"),
        }

        self.elements[eleTag] = eleinfo

    def _handle_ShellNLDKGQ(self, *args, **kwargs) -> dict[str, Any]:
        """处理非线性DKGQ壳单元"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "secTag": arg_map.get("secTag"),
        }

        self.elements[eleTag] = eleinfo

    def _handle_ShellNLDKGT(self, *args, **kwargs) -> dict[str, Any]:
        """处理非线性DKGT三角形壳单元"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "secTag": arg_map.get("secTag"),
        }

        self.elements[eleTag] = eleinfo

    def _handle_ShellNL(self, *args, **kwargs) -> dict[str, Any]:
        """处理非线性ShellNL壳单元"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "secTag": arg_map.get("secTag"),
        }

        self.elements[eleTag] = eleinfo

    def _handle_bbarQuad(self, *args, **kwargs) -> dict[str, Any]:
        """处理带B-bar的平面应变四边形单元"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "thick": arg_map.get("thick"),
            "matTag": arg_map.get("matTag"),
        }

        self.elements[eleTag] = eleinfo

    def _handle_enhancedQuad(self, *args, **kwargs) -> dict[str, Any]:
        """处理增强应变四边形单元"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "thick": arg_map.get("thick"),
            "type": arg_map.get("type"),  # PlaneStrain 或 PlaneStress
            "matTag": arg_map.get("matTag"),
        }

        self.elements[eleTag] = eleinfo

    def _handle_SSPquad(self, *args, **kwargs) -> dict[str, Any]:
        """处理稳定单点积分四边形元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "matTag": arg_map.get("matTag"),
            "type": arg_map.get("type"),  # PlaneStrain 或 PlaneStress
            "thick": arg_map.get("thick"),
        }

        # 处理可选参数
        if "b1" in arg_map:
            eleinfo["b1"] = arg_map.get("b1", 0.0)

        if "b2" in arg_map:
            eleinfo["b2"] = arg_map.get("b2", 0.0)

        self.elements[eleTag] = eleinfo

    def _handle_MVLEM_3D(self, *args, **kwargs) -> dict[str, Any]:
        """处理3D多竖直线元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "m": arg_map.get("m"),
        }

        # 处理必要的数组参数
        if "thick" in arg_map:
            eleinfo["thick"] = arg_map.get("thick")

        if "widths" in arg_map:
            eleinfo["widths"] = arg_map.get("widths")

        if "rho" in arg_map:
            eleinfo["rho"] = arg_map.get("rho")

        if "matConcreteTags" in arg_map:
            eleinfo["matConcreteTags"] = arg_map.get("matConcreteTags")

        if "matSteelTags" in arg_map:
            eleinfo["matSteelTags"] = arg_map.get("matSteelTags")

        if "matShearTag" in arg_map:
            eleinfo["matShearTag"] = arg_map.get("matShearTag")

        # 处理可选参数
        if "c" in arg_map:
            eleinfo["c"] = arg_map.get("c", 0.4)

        if "tMod" in arg_map:
            eleinfo["tMod"] = arg_map.get("tMod", 0.63)

        if "Nu" in arg_map:
            eleinfo["Nu"] = arg_map.get("Nu", 0.25)

        if "Dens" in arg_map:
            eleinfo["Dens"] = arg_map.get("Dens", 0.0)

        self.elements[eleTag] = eleinfo

    def _handle_SFI_MVLEM_3D(self, *args, **kwargs) -> dict[str, Any]:
        """处理3D剪切-弯曲相互作用元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "m": arg_map.get("m"),
        }

        # 处理必要的数组参数
        if "thicks" in arg_map:
            eleinfo["thicks"] = arg_map.get("thicks")

        if "widths" in arg_map:
            eleinfo["widths"] = arg_map.get("widths")

        if "matTags" in arg_map:
            eleinfo["matTags"] = arg_map.get("matTags")

        # 处理可选参数
        if "c" in arg_map:
            eleinfo["c"] = arg_map.get("c", 0.4)

        if "tMod" in arg_map:
            eleinfo["tMod"] = arg_map.get("tMod", 0.63)

        if "Nu" in arg_map:
            eleinfo["Nu"] = arg_map.get("Nu", 0.25)

        if "Dens" in arg_map:
            eleinfo["Dens"] = arg_map.get("Dens", 0.0)

        self.elements[eleTag] = eleinfo

    def _unknown(self, *args, **kwargs):
        # should never use this function but use ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()
