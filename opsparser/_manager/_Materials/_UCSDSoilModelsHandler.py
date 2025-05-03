from typing import Any

from .._BaseHandler import SubBaseHandler


class UCSDSoilModelsHandler(SubBaseHandler):
    def __init__(self, registry: dict[str, dict], materials_store: dict[int, dict]):
        """
        registry: matType → handler 的全局映射 (供 manager 生成)
        materials_store: MaterialManager.materials 共享引用
        """
        self.materials = materials_store
        self._register(registry)

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        return {
            "nDMaterial": {
                "alternative": True,
                "PressureIndependMultiYield": {
                    "positional": ["matType", "matTag", "nd", "rho", "refShearModul", "refBulkModul",
                                  "cohesi", "peakShearStra", "frictionAng?", "refPress?", "pressDependCoe?",
                                  "noYieldSurf?", "yieldSurf?"]
                },
                "PressureDependMultiYield": {
                    "positional": ["matType", "matTag", "nd", "rho", "refShearModul", "refBulkModul",
                                  "frictionAng", "peakShearStra", "refPress", "pressDependCoe", "PTAng",
                                  "contrac", "dilat", "liquefac", "noYieldSurf?", "yieldSurf?", "e?", "params?", "c?"]
                },
                "PressureDependMultiYield02": {
                    "positional": ["matType", "matTag", "nd", "rho", "refShearModul", "refBulkModul",
                                  "frictionAng", "peakShearStra", "refPress", "pressDependCoe", "PTAng",
                                  "contrac1", "contrac3", "dilat1", "dilat3", "noYieldSurf?", "yieldSurf?",
                                  "contrac2?", "dilat2?", "liquefac?", "e?", "params?", "c?"]
                },
                "PressureDependMultiYield03": {
                    "positional": ["matType", "matTag", "nd", "rho", "refShearModul", "refBulkModul",
                                  "frictionAng", "peakShearStra", "refPress", "pressDependCoe", "PTAng",
                                  "ca", "cb", "cc", "cd", "ce", "da", "db", "dc", "noYieldSurf?",
                                  "yieldSurf?", "liquefac1?", "liquefac2?", "pa?", "s0?"]
                }
            }
        }

    # ---------- matType to handle ----------
    @staticmethod
    def handles() -> list[str]:
        return ["nDMaterial"]

    @staticmethod
    def types() -> list[str]:
        return ["PressureIndependMultiYield", "PressureDependMultiYield",
                "PressureDependMultiYield02", "PressureDependMultiYield03"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        matType = args[0]
        handler_method = getattr(self, f"_handle_{matType}", self._unknown)
        return handler_method(*args, **kwargs)

    def _handle_PressureIndependMultiYield(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `PressureIndependMultiYield` Material

        nDMaterial('PressureIndependMultiYield', matTag, nd, rho, refShearModul, refBulkModul, cohesi, peakShearStra, frictionAng=0., refPress=100., pressDependCoe=0., noYieldSurf=20, *yieldSurf)

        rule = {
            "positional": ["matType", "matTag", "nd", "rho", "refShearModul", "refBulkModul", "cohesi", "peakShearStra", "frictionAng?", "refPress?", "pressDependCoe?", "noYieldSurf?", "yieldSurf*"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "nd": arg_map.get("nd"),
            "rho": arg_map.get("rho"),
            "refShearModul": arg_map.get("refShearModul"),
            "refBulkModul": arg_map.get("refBulkModul"),
            "cohesi": arg_map.get("cohesi"),
            "peakShearStra": arg_map.get("peakShearStra"),
            "materialCommandType": "nDMaterial"
        }

        # 添加可选参数
        optional_params = ["frictionAng", "refPress", "pressDependCoe", "noYieldSurf"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param)

        # 处理可变参数 yieldSurf
        if "yieldSurf" in arg_map:
            material_info["yieldSurf"] = arg_map.get("yieldSurf")

        self.materials[matTag] = material_info
        return material_info

    def _handle_PressureDependMultiYield(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `PressureDependMultiYield` Material

        nDMaterial('PressureDependMultiYield', matTag, nd, rho, refShearModul, refBulkModul, frictionAng, peakShearStra, refPress, pressDependCoe, PTAng, contrac, *dilat, *liquefac, noYieldSurf=20.0, *yieldSurf=[], e=0.6, *params=[0.9, 0.02, 0.7, 101.0], c=0.3)

        rule = {
            "positional": ["matType", "matTag", "nd", "rho", "refShearModul", "refBulkModul", "frictionAng", "peakShearStra", "refPress", "pressDependCoe", "PTAng", "contrac", "dilat*", "liquefac*", "noYieldSurf?", "yieldSurf*", "e?", "params*", "c?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "nd": arg_map.get("nd"),
            "rho": arg_map.get("rho"),
            "refShearModul": arg_map.get("refShearModul"),
            "refBulkModul": arg_map.get("refBulkModul"),
            "frictionAng": arg_map.get("frictionAng"),
            "peakShearStra": arg_map.get("peakShearStra"),
            "refPress": arg_map.get("refPress"),
            "pressDependCoe": arg_map.get("pressDependCoe"),
            "PTAng": arg_map.get("PTAng"),
            "contrac": arg_map.get("contrac"),
            "materialCommandType": "nDMaterial"
        }

        # 处理可变参数
        if "dilat" in arg_map:
            material_info["dilat"] = arg_map.get("dilat")
        if "liquefac" in arg_map:
            material_info["liquefac"] = arg_map.get("liquefac")
        if "yieldSurf" in arg_map:
            material_info["yieldSurf"] = arg_map.get("yieldSurf")
        if "params" in arg_map:
            material_info["params"] = arg_map.get("params")

        # 添加可选参数
        optional_params = ["noYieldSurf", "e", "c"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info
        return material_info

    def _handle_PressureDependMultiYield02(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `PressureDependMultiYield02` Material

        nDMaterial('PressureDependMultiYield02', matTag, nd, rho, refShearModul, refBulkModul, frictionAng, peakShearStra, refPress, pressDependCoe, PTAng, contrac[0], contrac[2], dilat[0], dilat[2], noYieldSurf=20.0, *yieldSurf=[], contrac[1]=5.0, dilat[1]=3.0, *liquefac=[1.0,0.0],e=0.6, *params=[0.9, 0.02, 0.7, 101.0], c=0.1)

        rule = {
            "positional": ["matType", "matTag", "nd", "rho", "refShearModul", "refBulkModul", "frictionAng", "peakShearStra", "refPress", "pressDependCoe", "PTAng", "contrac1", "contrac3", "dilat1", "dilat3", "noYieldSurf?", "yieldSurf*", "contrac2?", "dilat2?", "liquefac*", "e?", "params*", "c?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "nd": arg_map.get("nd"),
            "rho": arg_map.get("rho"),
            "refShearModul": arg_map.get("refShearModul"),
            "refBulkModul": arg_map.get("refBulkModul"),
            "frictionAng": arg_map.get("frictionAng"),
            "peakShearStra": arg_map.get("peakShearStra"),
            "refPress": arg_map.get("refPress"),
            "pressDependCoe": arg_map.get("pressDependCoe"),
            "PTAng": arg_map.get("PTAng"),
            "contrac1": arg_map.get("contrac1"),
            "contrac3": arg_map.get("contrac3"),
            "dilat1": arg_map.get("dilat1"),
            "dilat3": arg_map.get("dilat3"),
            "materialCommandType": "nDMaterial"
        }

        # 添加可选参数
        optional_params = ["noYieldSurf", "contrac2", "dilat2", "e", "c"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param)

        # 处理可变参数
        if "yieldSurf" in arg_map:
            material_info["yieldSurf"] = arg_map.get("yieldSurf")
        if "liquefac" in arg_map:
            material_info["liquefac"] = arg_map.get("liquefac")
        if "params" in arg_map:
            material_info["params"] = arg_map.get("params")

        self.materials[matTag] = material_info
        return material_info

    def _handle_PressureDependMultiYield03(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `PressureDependMultiYield03` Material

        nDMaterial('PressureDependMultiYield03', matTag, nd, rho, refShearModul, refBulkModul, frictionAng, peakShearStra, refPress, pressDependCoe, PTAng, ca, cb, cc, cd, ce, da, db, dc, noYieldSurf=20.0, *yieldSurf=[], liquefac1=1, liquefac2=0., pa=101, s0=1.73)

        rule = {
            "positional": ["matType", "matTag", "nd", "rho", "refShearModul", "refBulkModul", "frictionAng", "peakShearStra", "refPress", "pressDependCoe", "PTAng", "ca", "cb", "cc", "cd", "ce", "da", "db", "dc", "noYieldSurf?", "yieldSurf*", "liquefac1?", "liquefac2?", "pa?", "s0?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "nd": arg_map.get("nd"),
            "rho": arg_map.get("rho"),
            "refShearModul": arg_map.get("refShearModul"),
            "refBulkModul": arg_map.get("refBulkModul"),
            "frictionAng": arg_map.get("frictionAng"),
            "peakShearStra": arg_map.get("peakShearStra"),
            "refPress": arg_map.get("refPress"),
            "pressDependCoe": arg_map.get("pressDependCoe"),
            "PTAng": arg_map.get("PTAng"),
            "ca": arg_map.get("ca"),
            "cb": arg_map.get("cb"),
            "cc": arg_map.get("cc"),
            "cd": arg_map.get("cd"),
            "ce": arg_map.get("ce"),
            "da": arg_map.get("da"),
            "db": arg_map.get("db"),
            "dc": arg_map.get("dc"),
            "materialCommandType": "nDMaterial"
        }

        # 添加可选参数
        optional_params = ["noYieldSurf", "liquefac1", "liquefac2", "pa", "s0"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param)

        # 处理可变参数 yieldSurf
        if "yieldSurf" in arg_map:
            material_info["yieldSurf"] = arg_map.get("yieldSurf")

        self.materials[matTag] = material_info
        return material_info

    def _unknown(self, *args, **kwargs):
        # should never use this function but use MaterialManager.handle_unknown_material()
        raise NotImplementedError

    def clear(self):
        self.materials.clear()
