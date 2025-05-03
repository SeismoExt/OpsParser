from typing import Any

import openseespy.opensees as ops

from .._BaseHandler import BaseHandler


class ZeroLengthHandler(BaseHandler):
    def __init__(self, registry: dict[str, dict], element_store: dict[int, dict]):
        """
        registry: eleType → handler  的全局映射 (供 manager 生成)
        element_store: ElementManager.elements 共享引用
        """
        self.elements = element_store
        self._register(registry)

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        rules = {"alternative":True}

        # ndm for vector if needed
        ndm = ops.getNDM()[0]
        assert len(ops.getNDM()) == 1, f"Invalid length of ndm, expected 1, got {len(ops.getNDM()) =}"  # noqa: S101

        # add rule for different element types
        rules["zeroLength"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2"],
            "options": {
                "-mat": "matTags*",
                "-dir": "dirs*",
                "-doRayleigh": "rFlag",
                "-orient?": [f"vecx*{ndm}",f"vecyp*{ndm}"],      # vecx and vecyp
            }
        }
        rules["zeroLengthND"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "matTag", "uniTag?"],
            "options": {
                "-orient": [f"vecx*{ndm}",f"vecyp*{ndm}"],      # vecx and vecyp
            }
        }

        rules["zeroLengthSection"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "secTag"],
            "options": {
                "-orient": [f"vecx*{ndm}",f"vecyp*{ndm}"],      # vecx and vecyp
                "-doRayleigh": "rFlag"
            }
        }

        rules["CoupledZeroLength"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "dirn1", "dirn2", "matTag", "rFlag?"],
        }

        rules["zeroLengthContact2D"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "Kn", "Kt", "mu"],
            "options": {
                "-normal": ["Nx", "Ny"]
            }
        }

        rules["zeroLengthContact3D"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "Kn", "Kt", "mu", "c", "dir"],
        }

        rules["zeroLengthContactNTS2D"] = {
            "positional": ["eleType"],
            "options": {
                "-sNdNum": "sNdNum",
                "-mNdNum": "mNdNum",
                "-Nodes": "NodesTags*",
                "kn": "kn",
                "kt": "kt",
                "phi": "phi"
            }
        }

        rules["zeroLengthInterface2D"] = {
            "positional": ["eleType"],
            "options": {
                "-sNdNum": "sNdNum",
                "-mNdNum": "mNdNum",
                "-dof": ["sdof", "mdof"],
                "-Nodes": "NodesTags*",
                "kn": "kn",
                "kt": "kt",
                "phi": "phi"
            }
        }

        rules["zeroLengthImpact3D"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "direction", "initGap", "frictionRatio",
                          "Kt", "Kn", "Kn2", "Delta_y", "cohesion"],
        }
        return {"element": rules}

    # ---------- eleType to handle ----------
    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return [
            "zeroLength", "zeroLengthND", "zeroLengthSection",
            "CoupledZeroLength", "zeroLengthContact2D",
            "zeroLengthContact3D", "zeroLengthContactNTS2D",
            "zeroLengthInterface2D", "zeroLengthImpact3D",
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "zeroLength": self._handle_zeroLength,
            "zeroLengthND": self._handle_zerolengthND,
            "zeroLengthSection": self._handle_zeroLengthSection,
            "CoupledZeroLength": self._handle_CoupledZeroLength,
            "zeroLengthContact2D": self._handle_zeroLengthContact2D,
            "zeroLengthContact3D": self._handle_zeroLengthContact3D,
            "zeroLengthContactNTS2D": self._handle_zeroLengthContactNTS2D,
            "zeroLengthInterface2D": self._handle_zeroLengthInterface2D,
            "zeroLengthImpact3D": self._handle_zeroLengthImpact3D,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_zeroLength(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `zeroLength` element

        rule = {
            "positional": ["eleType", "eleTag", "eleNodes*2"],
            "options": {
                "-mat": "matTags*",
                "-dir": "dirs*",
                "doRayleigh": "rFlag",
                "-orient?": [f"vecx*{ndm}",f"vecyp*{ndm}"],      # vecx and vecyp
            }
        }
        """
        arg_map = self._parse("element", *args, **kwargs)

        # positional arguments
        eleType = arg_map.get("eleType")
        eleTag = arg_map.get("eleTag")
        eleNodes = arg_map.get("eleNodes")

        # optional arguments
        matTags = arg_map.get("matTags", [])
        direction = arg_map.get("dirs", [])
        rFlag = arg_map.get("rFlag", 0)
        vecx = arg_map.get("vecx", [])
        vecyp = arg_map.get("vecyp", [])

        # 保存零长度单元信息
        eleinfo = {
            "eleType": eleType,
            "eleTag": eleTag,
            "eleNodes": eleNodes,
            "matTags": matTags,
            "dirs": direction,
            "rFlag": rFlag,
            "vecx": vecx,
            "vecyp": vecyp,
        }
        self.elements[eleTag] = eleinfo

    def _handle_zerolengthND(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `zeroLengthND` element

        element('zeroLengthND', eleTag, *eleNodes, matTag, <uniTag>, <'-orient', *vecx, vecyp>)

        rule = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "matTag", "uniTag?"],
            "options": {
                "-orient": [f"vecx*{ndm}",f"vecyp*{ndm}"],      # vecx and vecyp
            }
        }
        """
        arg_map = self._parse("element", *args, **kwargs)

        # positional arguments
        eleType = arg_map.get("eleType")
        eleTag = arg_map.get("eleTag")
        eleNodes = arg_map.get("eleNodes")
        matTag = arg_map.get("matTag")
        uniTag = arg_map.get("uniTag", None)

        # optional arguments
        vecx = arg_map.get("vecx", [])
        vecyp = arg_map.get("vecyp", [])

        # 保存zeroLengthND单元信息
        eleinfo = {
            "eleType": eleType,
            "eleTag": eleTag,
            "eleNodes": eleNodes,
            "matTag": matTag,
            "uniTag": uniTag,
            "vecx": vecx,
            "vecyp": vecyp,
        }
        self.elements[eleTag] = eleinfo

    def _handle_zeroLengthSection(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `zeroLengthSection` element

        element('zeroLengthSection', eleTag, *eleNodes, secTag, <'-orient', *vecx, *vecyp>, <'-doRayleigh', rFlag>)

        rule = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "secTag"],
            "options": {
                "-orient": [f"vecx*{ndm}",f"vecyp*{ndm}"],      # vecx and vecyp
                "-doRayleigh": "rFlag"
            }
        }
        """
        arg_map = self._parse("element", *args, **kwargs)

        # positional arguments
        eleType = arg_map.get("eleType")
        eleTag = arg_map.get("eleTag")
        eleNodes = arg_map.get("eleNodes")
        secTag = arg_map.get("secTag")

        # optional arguments
        vecx = arg_map.get("vecx", [])
        vecyp = arg_map.get("vecyp", [])
        rFlag = arg_map.get("rFlag", 0)

        # 保存zeroLengthSection单元信息
        eleinfo = {
            "eleType": eleType,
            "eleTag": eleTag,
            "eleNodes": eleNodes,
            "secTag": secTag,
            "vecx": vecx,
            "vecyp": vecyp,
            "rFlag": rFlag,
        }
        self.elements[eleTag] = eleinfo

    def _handle_CoupledZeroLength(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `CoupledZeroLength` element

        element('CoupledZeroLength', eleTag, *eleNodes, dirn1, dirn2, matTag, <rFlag=1>)

        rule = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "dirn1", "dirn2", "matTag", "rFlag?"],
        }
        """
        arg_map = self._parse("element", *args, **kwargs)

        # positional arguments
        eleType = arg_map.get("eleType")
        eleTag = arg_map.get("eleTag")
        eleNodes = arg_map.get("eleNodes")
        dirn1 = arg_map.get("dirn1")
        dirn2 = arg_map.get("dirn2")
        matTag = arg_map.get("matTag")
        rFlag = arg_map.get("rFlag", 0)

        # 保存CoupledZeroLength单元信息
        eleinfo = {
            "eleType": eleType,
            "eleTag": eleTag,
            "eleNodes": eleNodes,
            "dirn1": dirn1,
            "dirn2": dirn2,
            "matTag": matTag,
            "rFlag": rFlag,
        }
        self.elements[eleTag] = eleinfo

    def _handle_zeroLengthContact2D(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `zeroLengthContact2D` element

        element('zeroLengthContact2D', eleTag, *eleNodes, Kn, Kt, mu, '-normal', Nx, Ny)

        rule = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "Kn", "Kt", "mu"],
            "options": {
                "-normal": ["Nx", "Ny"]
            }
        }
        """
        arg_map = self._parse("element", *args, **kwargs)

        # positional arguments
        eleType = arg_map.get("eleType")
        eleTag = arg_map.get("eleTag")
        eleNodes = arg_map.get("eleNodes")
        Kn = arg_map.get("Kn")
        Kt = arg_map.get("Kt")
        mu = arg_map.get("mu")

        # optional arguments
        Nx = arg_map.get("Nx", 0)
        Ny = arg_map.get("Ny", 0)

        # 保存接触单元信息
        eleinfo = {
            "eleType": eleType,
            "eleTag": eleTag,
            "eleNodes": eleNodes,
            "Kn": Kn,
            "Kt": Kt,
            "mu": mu,
            "Nx": Nx,
            "Ny": Ny,
        }
        self.elements[eleTag] = eleinfo

    def _handle_zeroLengthContact3D(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `zeroLengthContact3D` element

        element('zeroLengthContact3D', eleTag, *eleNodes, Kn, Kt, mu, c, dir)

        rule = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "Kn", "Kt", "mu", "c", "dir"],
        }
        """
        arg_map = self._parse("element", *args, **kwargs)

        # positional arguments
        eleType = arg_map.get("eleType")
        eleTag = arg_map.get("eleTag")
        eleNodes = arg_map.get("eleNodes")
        Kn = arg_map.get("Kn")
        Kt = arg_map.get("Kt")
        mu = arg_map.get("mu")
        c = arg_map.get("c")
        dir_val = arg_map.get("dir")  # 重命名为dir_val避免与内置函数冲突

        # 保存接触单元信息
        eleinfo = {
            "eleType": eleType,
            "eleTag": eleTag,
            "eleNodes": eleNodes,
            "Kn": Kn,
            "Kt": Kt,
            "mu": mu,
            "c": c,
            "dir": dir_val,
        }
        self.elements[eleTag] = eleinfo

    def _handle_zeroLengthContactNTS2D(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `zeroLengthContactNTS2D` element

        element('zeroLengthContactNTS2D', eleTag, '-sNdNum', sNdNum, '-mNdNum', mNdNum, '-Nodes', *NodesTags, kn, kt, phi)

        rule = {
            "positional": ["eleType"],
            "options": {
                "-sNdNum": "sNdNum",
                "-mNdNum": "mNdNum",
                "-Nodes": "NodesTags*",
                "kn": "kn",
                "kt": "kt",
                "phi": "phi"
            }
        }
        """
        arg_map = self._parse("element", *args, **kwargs)

        # positional arguments
        eleType = arg_map.get("eleType")
        eleTag = int(args[1]) if len(args) > 1 else None  # 从原始参数获取标签

        # options
        sNdNum = arg_map.get("sNdNum")
        mNdNum = arg_map.get("mNdNum")
        NodesTags = arg_map.get("NodesTags", [])
        kn = arg_map.get("kn")
        kt = arg_map.get("kt")
        phi = arg_map.get("phi")

        # 保存接触单元信息
        eleinfo = {
            "eleType": eleType,
            "eleTag": eleTag,
            "sNdNum": sNdNum,
            "mNdNum": mNdNum,
            "NodesTags": NodesTags,
            "kn": kn,
            "kt": kt,
            "phi": phi,
        }
        self.elements[eleTag] = eleinfo

    def _handle_zeroLengthInterface2D(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `zeroLengthInterface2D` element

        element('zeroLengthInterface2D', eleTag, '-sNdNum', sNdNum, '-mNdNum', mNdNum, '-dof', sdof, mdof, '-Nodes', *NodesTags, kn, kt, phi)

        rule = {
            "positional": ["eleType"],
            "options": {
                "-sNdNum": "sNdNum",
                "-mNdNum": "mNdNum",
                "-dof": ["sdof", "mdof"],
                "-Nodes": "NodesTags*",
                "kn": "kn",
                "kt": "kt",
                "phi": "phi"
            }
        }
        """
        arg_map = self._parse("element", *args, **kwargs)

        # positional arguments
        eleType = arg_map.get("eleType")
        eleTag = int(args[1]) if len(args) > 1 else None  # 从原始参数获取标签

        # options
        sNdNum = arg_map.get("sNdNum")
        mNdNum = arg_map.get("mNdNum")
        sdof = arg_map.get("sdof")
        mdof = arg_map.get("mdof")
        NodesTags = arg_map.get("NodesTags", [])
        kn = arg_map.get("kn")
        kt = arg_map.get("kt")
        phi = arg_map.get("phi")

        # 保存接触单元信息
        eleinfo = {
            "eleType": eleType,
            "eleTag": eleTag,
            "sNdNum": sNdNum,
            "mNdNum": mNdNum,
            "sdof": sdof,
            "mdof": mdof,
            "NodesTags": NodesTags,
            "kn": kn,
            "kt": kt,
            "phi": phi,
        }
        self.elements[eleTag] = eleinfo

    def _handle_zeroLengthImpact3D(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `zeroLengthImpact3D` element

        element('zeroLengthImpact3D', eleTag, *eleNodes, direction, initGap, frictionRatio, Kt, Kn, Kn2, Delta_y, cohesion)

        rule = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "direction", "initGap", "frictionRatio",
                          "Kt", "Kn", "Kn2", "Delta_y", "cohesion"],
        }
        """
        arg_map = self._parse("element", *args, **kwargs)

        # positional arguments
        eleType = arg_map.get("eleType")
        eleTag = arg_map.get("eleTag")
        eleNodes = arg_map.get("eleNodes")
        direction = arg_map.get("direction")
        initGap = arg_map.get("initGap")
        frictionRatio = arg_map.get("frictionRatio")
        Kt = arg_map.get("Kt")
        Kn = arg_map.get("Kn")
        Kn2 = arg_map.get("Kn2")
        Delta_y = arg_map.get("Delta_y")
        cohesion = arg_map.get("cohesion")

        # 保存接触单元信息
        eleinfo = {
            "eleType": eleType,
            "eleTag": eleTag,
            "eleNodes": eleNodes,
            "direction": direction,
            "initGap": initGap,
            "frictionRatio": frictionRatio,
            "Kt": Kt,
            "Kn": Kn,
            "Kn2": Kn2,
            "Delta_y": Delta_y,
            "cohesion": cohesion,
        }
        self.elements[eleTag] = eleinfo

    def _unknown(self, *args, **kwargs):
        # should never use this function but use ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()
