from typing import Any

import openseespy.opensees as ops

from .._BaseHandler import BaseHandler


class UCSDUpHandler(BaseHandler):
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
            # 四节点四边形u-p元素 - 平面应变
            rules["quadUP"] = {
                "positional": ["eleType", "eleTag", "eleNodes*4", "thick", "matTag", "bulk", "fmass", "hPerm", "vPerm", "b1?", "b2?", "t?"],
            }
            # bbar四边形u-p元素 - 平面应变
            rules["bbarQuadUP"] = {
                "positional": ["eleType", "eleTag", "eleNodes*4", "thick", "matTag", "bulk", "fmass", "hPerm", "vPerm", "b1?", "b2?", "t?"],
            }
            # 九四节点四边形u-p元素 - 平面应变 (9个节点，其中4个角节点有3个DOF，其余5个节点有2个DOF)
            rules["9_4_QuadUP"] = {
                "positional": ["eleType", "eleTag", "eleNodes*9", "thick", "matTag", "bulk", "fmass", "hPerm", "vPerm", "b1?", "b2?"],
            }
        elif ndm == 3:
            # 八节点六面体u-p元素
            rules["brickUP"] = {
                "positional": ["eleType", "eleTag", "eleNodes*8", "matTag", "bulk", "fmass", "permX", "permY", "permZ", "bX?", "bY?", "bZ?"],
            }
            # bbar砖u-p元素
            rules["bbarBrickUP"] = {
                "positional": ["eleType", "eleTag", "eleNodes*8", "matTag", "bulk", "fmass", "permX", "permY", "permZ", "bX?", "bY?", "bZ?"],
            }
            # 二十八节点砖u-p元素 (20个节点，其中8个角节点有4个DOF，其余节点有3个DOF)
            rules["20_8_BrickUP"] = {
                "positional": ["eleType", "eleTag", "eleNodes*20", "matTag", "bulk", "fmass", "permX", "permY", "permZ", "bX?", "bY?", "bZ?"],
            }
        else:
            raise NotImplementedError(f"Invalid {ndm =} for UCSD UP elements")
        return {"element": rules}

    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return [
            "quadUP", "brickUP", "bbarQuadUP", "bbarBrickUP", "9_4_QuadUP", "20_8_BrickUP"
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "quadUP": self._handle_quadUP,
            "brickUP": self._handle_brickUP,
            "bbarQuadUP": self._handle_bbarQuadUP,
            "bbarBrickUP": self._handle_bbarBrickUP,
            "9_4_QuadUP": self._handle_9_4_QuadUP,
            "20_8_BrickUP": self._handle_20_8_BrickUP
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_quadUP(self, *args, **kwargs) -> dict[str, Any]:
        """处理四节点四边形u-p元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "thick": arg_map.get("thick"),
            "matTag": arg_map.get("matTag"),
            "bulk": arg_map.get("bulk"),
            "fmass": arg_map.get("fmass"),
            "hPerm": arg_map.get("hPerm"),
            "vPerm": arg_map.get("vPerm")
        }

        # 处理可选参数
        if 'b1' in arg_map:
            eleinfo['b1'] = arg_map.get('b1', 0.0)

        if 'b2' in arg_map:
            eleinfo['b2'] = arg_map.get('b2', 0.0)

        if 't' in arg_map:
            eleinfo['t'] = arg_map.get('t', 0.0)

        self.elements[eleTag] = eleinfo

    def _handle_brickUP(self, *args, **kwargs) -> dict[str, Any]:
        """处理八节点六面体u-p元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "matTag": arg_map.get("matTag"),
            "bulk": arg_map.get("bulk"),
            "fmass": arg_map.get("fmass"),
            "permX": arg_map.get("permX"),
            "permY": arg_map.get("permY"),
            "permZ": arg_map.get("permZ")
        }

        # 处理可选参数
        if 'bX' in arg_map:
            eleinfo['bX'] = arg_map.get('bX', 0.0)

        if 'bY' in arg_map:
            eleinfo['bY'] = arg_map.get('bY', 0.0)

        if 'bZ' in arg_map:
            eleinfo['bZ'] = arg_map.get('bZ', 0.0)

        self.elements[eleTag] = eleinfo

    def _handle_bbarQuadUP(self, *args, **kwargs) -> dict[str, Any]:
        """处理bbar四边形u-p元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "thick": arg_map.get("thick"),
            "matTag": arg_map.get("matTag"),
            "bulk": arg_map.get("bulk"),
            "fmass": arg_map.get("fmass"),
            "hPerm": arg_map.get("hPerm"),
            "vPerm": arg_map.get("vPerm")
        }

        # 处理可选参数
        if 'b1' in arg_map:
            eleinfo['b1'] = arg_map.get('b1', 0.0)

        if 'b2' in arg_map:
            eleinfo['b2'] = arg_map.get('b2', 0.0)

        if 't' in arg_map:
            eleinfo['t'] = arg_map.get('t', 0.0)

        self.elements[eleTag] = eleinfo

    def _handle_bbarBrickUP(self, *args, **kwargs) -> dict[str, Any]:
        """处理bbar砖u-p元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "matTag": arg_map.get("matTag"),
            "bulk": arg_map.get("bulk"),
            "fmass": arg_map.get("fmass"),
            "permX": arg_map.get("permX"),
            "permY": arg_map.get("permY"),
            "permZ": arg_map.get("permZ")
        }

        # 处理可选参数
        if 'bX' in arg_map:
            eleinfo['bX'] = arg_map.get('bX', 0.0)

        if 'bY' in arg_map:
            eleinfo['bY'] = arg_map.get('bY', 0.0)

        if 'bZ' in arg_map:
            eleinfo['bZ'] = arg_map.get('bZ', 0.0)

        self.elements[eleTag] = eleinfo

    def _handle_9_4_QuadUP(self, *args, **kwargs) -> dict[str, Any]:
        """处理九四节点四边形u-p元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "thick": arg_map.get("thick"),
            "matTag": arg_map.get("matTag"),
            "bulk": arg_map.get("bulk"),
            "fmass": arg_map.get("fmass"),
            "hPerm": arg_map.get("hPerm"),
            "vPerm": arg_map.get("vPerm")
        }

        # 处理可选参数
        if 'b1' in arg_map:
            eleinfo['b1'] = arg_map.get('b1', 0.0)

        if 'b2' in arg_map:
            eleinfo['b2'] = arg_map.get('b2', 0.0)

        self.elements[eleTag] = eleinfo

    def _handle_20_8_BrickUP(self, *args, **kwargs) -> dict[str, Any]:
        """处理二十八节点砖u-p元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")
        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "matTag": arg_map.get("matTag"),
            "bulk": arg_map.get("bulk"),
            "fmass": arg_map.get("fmass"),
            "permX": arg_map.get("permX"),
            "permY": arg_map.get("permY"),
            "permZ": arg_map.get("permZ")
        }

        # 处理可选参数
        if 'bX' in arg_map:
            eleinfo['bX'] = arg_map.get('bX', 0.0)

        if 'bY' in arg_map:
            eleinfo['bY'] = arg_map.get('bY', 0.0)

        if 'bZ' in arg_map:
            eleinfo['bZ'] = arg_map.get('bZ', 0.0)

        self.elements[eleTag] = eleinfo

    def _unknown(self, *args, **kwargs):
        # should never use this function but use ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()
