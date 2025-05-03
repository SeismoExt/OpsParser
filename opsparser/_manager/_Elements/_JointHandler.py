from collections import defaultdict
from copy import deepcopy
from typing import Any

from .._BaseHandler import SubBaseHandler


class JointHandler(SubBaseHandler):
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

        # 添加不同节点元素类型的规则
        rules["beamColumnJoint"] = {
            "positional": ["eleType", "eleTag", "eleNodes*4", "Mat1Tag", "Mat2Tag", "Mat3Tag", "Mat4Tag", "Mat5Tag",
                          "Mat6Tag", "Mat7Tag", "Mat8Tag", "Mat9Tag", "Mat10Tag", "Mat11Tag", "Mat12Tag", "Mat13Tag","eleHeightFac?","eleWidthFac?"],
        }

        rules["ElasticTubularJoint"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "Brace_Diameter", "Brace_Angle", "E",
                          "Chord_Diameter", "Chord_Thickness", "Chord_Angle"],
        }

        rules["Joint2D"] = {
            "positional": ["eleType", "eleTag", "eleNodes*5", "MatC", "LrgDspTag"],
            "options": {
                "-damage?": ["DmgTag", "Dmg1?", "Dmg2?", "Dmg3?", "Dmg4?", "DmgC?"],
            }
        }

        return {"element": rules}

    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return [
            "beamColumnJoint", "ElasticTubularJoint", "Joint2D",
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "beamColumnJoint": self._handle_beamColumnJoint,
            "ElasticTubularJoint": self._handle_ElasticTubularJoint,
            "Joint2D": self._handle_Joint2D,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_beamColumnJoint(self, *args, **kwargs) -> dict[str, Any]:
        """处理 beamColumnJoint 元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "Mat1Tag": arg_map.get("Mat1Tag"),
            "Mat2Tag": arg_map.get("Mat2Tag"),
            "Mat3Tag": arg_map.get("Mat3Tag"),
            "Mat4Tag": arg_map.get("Mat4Tag"),
            "Mat5Tag": arg_map.get("Mat5Tag"),
            "Mat6Tag": arg_map.get("Mat6Tag"),
            "Mat7Tag": arg_map.get("Mat7Tag"),
            "Mat8Tag": arg_map.get("Mat8Tag"),
            "Mat9Tag": arg_map.get("Mat9Tag"),
            "Mat10Tag": arg_map.get("Mat10Tag"),
            "Mat11Tag": arg_map.get("Mat11Tag"),
            "Mat12Tag": arg_map.get("Mat12Tag"),
            "Mat13Tag": arg_map.get("Mat13Tag"),
        }

        # 处理可选参数
        if 'eleHeightFac' in arg_map:
            eleinfo['eleHeightFac'] = arg_map.get('eleHeightFac', 1.0)

        if 'eleWidthFac' in arg_map:
            eleinfo['eleWidthFac'] = arg_map.get('eleWidthFac', 1.0)

        self.elements[eleTag] = eleinfo

    def _handle_ElasticTubularJoint(self, *args, **kwargs) -> dict[str, Any]:
        """处理 ElasticTubularJoint 元素"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "Brace_Diameter": arg_map.get("Brace_Diameter"),
            "Brace_Angle": arg_map.get("Brace_Angle"),
            "E": arg_map.get("E"),
            "Chord_Diameter": arg_map.get("Chord_Diameter"),
            "Chord_Thickness": arg_map.get("Chord_Thickness"),
            "Chord_Angle": arg_map.get("Chord_Angle"),
        }

        self.elements[eleTag] = eleinfo

    def _handle_Joint2D(self, *args, **kwargs) -> dict[str, Any]:
        """处理 Joint2D 元素"""
        # not use _parse directedly beacuse rule for Joint2D is too complex
        arg_map = self._parse("element", *args, **kwargs)

        # so we meed to create the rule and parse it again manually anyway
        rule = {}
        n_damage = 0
        if "-damage" in args:
            n_damage = len(self._extract_args_by_str(args[args.index("-damage"):], "-damage"))
        damage_optopns = {"-damage?": "DmgTag?" if n_damage < 4 else ["Dmg1?", "Dmg2?", "Dmg3?", "Dmg4?", "DmgC?"]}
        if len(args) - n_damage - 1 > 9:
            # Check if there are unparsed positional args, if yes, it means we should use the second format
            command_type = 2
            rule["positional"] = ["eleType", "eleTag", "eleNodes*5", "Mat1", "Mat2", "Mat3", "Mat4", "MatC", "LrgDspTag"]
            rule = {
                "positional": ["eleType", "eleTag", "eleNodes*5", "Mat1", "Mat2", "Mat3", "Mat4", "MatC", "LrgDspTag"],
                "options": damage_optopns
            }
        else:
            # parse again manually anyway
            command_type = 1
            rule = {
                "positional": ["eleType", "eleTag", "eleNodes*5", "MatC", "LrgDspTag"],
                "options": damage_optopns
            }

        # Parse with the rule directly
        arg_map = self._parse_rule_based_command(rule, *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "MatC": arg_map.get("MatC"),
            "LrgDspTag": arg_map.get("LrgDspTag"),
        }

        # 处理可选的接口转动弹簧材料
        if command_type == 2:
            eleinfo.update({f"Mat{i}": arg_map.get(f"Mat{i}") for i in range(1, 5) if f"Mat{i}" in arg_map})

        # 处理损伤模型参数
        if n_damage == 1:
            eleinfo['DmgTag'] = arg_map.get('DmgTag')

        # 处理详细的损伤模型参数
        if n_damage>1:
            eleinfo.update({f"Dmg{i}": arg_map.get(f"Dmg{i}") for i in range(1, 5) if f"Dmg{i}" in arg_map})

        if 'DmgC' in arg_map:
            eleinfo['DmgC'] = arg_map.get('DmgC')

        self.elements[eleTag] = eleinfo

    def _unknown(self, *args, **kwargs):
        # should never use this function but use ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()
