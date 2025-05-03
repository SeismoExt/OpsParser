from typing import Any

from .._BaseHandler import SubBaseHandler


class TrussHandler(SubBaseHandler):
    def __init__(self, registry: dict[str, dict], element_store: dict[int, dict]):
        """
        registry: eleType → handler 的全局映射 (供 manager 生成)
        element_store: ElementManager.elements 共享引用
        """
        self.elements = element_store
        self._register(registry)

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        rules = {"alternative":True}

        # 普通桁架元素规则
        rules["Truss"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "A", "matTag"],
            "options": {
                "-rho": "rho",
                "-cMass": "cFlag",
                "-doRayleigh": "rFlag",
            }
        }

        # TrussSection元素规则
        rules["TrussSection"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "secTag"],
            "options": {
                "-rho": "rho",
                "-cMass": "cFlag",
                "-doRayleigh": "rFlag",
            }
        }

        # 协旋转桁架元素规则
        rules["corotTruss"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "A", "matTag"],
            "options": {
                "-rho": "rho",
                "-cMass": "cFlag",
                "-doRayleigh": "rFlag",
            }
        }

        # 协旋转桁架截面元素规则
        rules["corotTrussSection"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "secTag"],
            "options": {
                "-rho": "rho",
                "-cMass": "cFlag",
                "-doRayleigh": "rFlag",
            }
        }

        return {"element": rules}

    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return ["Truss", "TrussSection", "corotTruss", "corotTrussSection"]


    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "Truss": self._handle_Truss,
            "TrussSection": self._handle_TrussSection,
            "corotTruss": self._handle_corotTruss,
            "corotTrussSection": self._handle_corotTrussSection,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_Truss(self, *args, **kwargs) -> dict[str, Any]:
        """
        处理标准桁架元素

        element('Truss', eleTag, *eleNodes, A, matTag, <'-rho', rho>, <'-cMass', cFlag>, <'-doRayleigh', rFlag>)

        rule = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "A", "matTag"],
            "options": {
                "-rho": "rho",
                "-cMass": "cFlag",
                "-doRayleigh": "rFlag",
            }
        }
        """
        arg_map = self._parse("element", *args, **kwargs)

        # 位置参数
        eleType = arg_map.get("eleType")
        eleTag = arg_map.get("eleTag")
        eleNodes = arg_map.get("eleNodes")
        A = arg_map.get("A")
        matTag = arg_map.get("matTag")

        # 可选参数
        rho = arg_map.get("rho", 0.0)
        cFlag = arg_map.get("cFlag", 0)
        rFlag = arg_map.get("rFlag", 0)

        # 保存桁架单元信息
        eleinfo = {
            "eleType": eleType,
            "eleTag": eleTag,
            "eleNodes": eleNodes,
            "A": A,
            "matTag": matTag,
            "rho": rho,
            "cFlag": cFlag,
            "rFlag": rFlag,
        }
        self.elements[eleTag] = eleinfo

    def _handle_TrussSection(self, *args, **kwargs) -> dict[str, Any]:
        """
        处理带有截面的桁架元素

        element('TrussSection', eleTag, *eleNodes, secTag, <'-rho', rho>, <'-cMass', cFlag>, <'-doRayleigh', rFlag>)

        rule = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "secTag"],
            "options": {
                "-rho": "rho",
                "-cMass": "cFlag",
                "-doRayleigh": "rFlag",
            }
        }
        """
        arg_map = self._parse("element", *args, **kwargs)

        # 位置参数
        eleType = arg_map.get("eleType")
        eleTag = arg_map.get("eleTag")
        eleNodes = arg_map.get("eleNodes")
        secTag = arg_map.get("secTag")

        # 可选参数
        rho = arg_map.get("rho", 0.0)
        cFlag = arg_map.get("cFlag", 0)
        rFlag = arg_map.get("rFlag", 0)

        # 保存桁架单元信息
        eleinfo = {
            "eleType": eleType,
            "eleTag": eleTag,
            "eleNodes": eleNodes,
            "secTag": secTag,
            "rho": rho,
            "cFlag": cFlag,
            "rFlag": rFlag,
        }
        self.elements[eleTag] = eleinfo

    def _handle_corotTruss(self, *args, **kwargs) -> dict[str, Any]:
        """
        处理协旋转桁架元素

        element('corotTruss', eleTag, *eleNodes, A, matTag, <'-rho', rho>, <'-cMass', cFlag>, <'-doRayleigh', rFlag>)

        rule = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "A", "matTag"],
            "options": {
                "-rho": "rho",
                "-cMass": "cFlag",
                "-doRayleigh": "rFlag",
            }
        }
        """
        arg_map = self._parse("element", *args, **kwargs)

        # 位置参数
        eleType = arg_map.get("eleType")
        eleTag = arg_map.get("eleTag")
        eleNodes = arg_map.get("eleNodes")
        A = arg_map.get("A")
        matTag = arg_map.get("matTag")

        # 可选参数
        rho = arg_map.get("rho", 0.0)
        cFlag = arg_map.get("cFlag", 0)
        rFlag = arg_map.get("rFlag", 0)

        # 保存桁架单元信息
        eleinfo = {
            "eleType": eleType,
            "eleTag": eleTag,
            "eleNodes": eleNodes,
            "A": A,
            "matTag": matTag,
            "rho": rho,
            "cFlag": cFlag,
            "rFlag": rFlag,
        }
        self.elements[eleTag] = eleinfo

    def _handle_corotTrussSection(self, *args, **kwargs) -> dict[str, Any]:
        """
        处理协旋转带有截面的桁架元素

        element('corotTrussSection', eleTag, *eleNodes, secTag, <'-rho', rho>, <'-cMass', cFlag>, <'-doRayleigh', rFlag>)

        rule = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "secTag"],
            "options": {
                "-rho": "rho",
                "-cMass": "cFlag",
                "-doRayleigh": "rFlag",
            }
        }
        """
        arg_map = self._parse("element", *args, **kwargs)

        # 位置参数
        eleType = arg_map.get("eleType")
        eleTag = arg_map.get("eleTag")
        eleNodes = arg_map.get("eleNodes")
        secTag = arg_map.get("secTag")

        # 可选参数
        rho = arg_map.get("rho", 0.0)
        cFlag = arg_map.get("cFlag", 0)
        rFlag = arg_map.get("rFlag", 0)

        # 保存桁架单元信息
        eleinfo = {
            "eleType": eleType,
            "eleTag": eleTag,
            "eleNodes": eleNodes,
            "secTag": secTag,
            "rho": rho,
            "cFlag": cFlag,
            "rFlag": rFlag,
        }
        self.elements[eleTag] = eleinfo

    def _unknown(self, *args, **kwargs):
        # should never use this function but use ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()