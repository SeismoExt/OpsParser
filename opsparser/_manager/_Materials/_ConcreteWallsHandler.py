from typing import Any

from .._BaseHandler import SubBaseHandler


class ConcreteWallsHandler(SubBaseHandler):
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
                "PlateFromPlaneStress": {
                    "positional": ["matType", "matTag", "pre_def_matTag", "OutofPlaneModulus"]
                },
                "PlateRebar": {
                    "positional": ["matType", "matTag", "pre_def_matTag", "sita"]
                },
                "PlasticDamageConcretePlaneStress": {
                    "positional": ["matType", "matTag", "E", "nu", "ft", "fc", "beta?", "Ap?", "An?", "Bn?"]
                }
            }
        }

    # ---------- matType to handle ----------
    @staticmethod
    def handles() -> list[str]:
        return ["nDMaterial"]

    @staticmethod
    def types() -> list[str]:
        return ["PlateFromPlaneStress", "PlateRebar", "PlasticDamageConcretePlaneStress"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        matType = args[0]
        handler_method = getattr(self, f"_handle_{matType}", self._unknown)
        return handler_method(*args, **kwargs)

    def _handle_PlateFromPlaneStress(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `PlateFromPlaneStress` Material

        nDMaterial('PlateFromPlaneStress', matTag, pre_def_matTag, OutofPlaneModulus)

        rule = {
            "positional": ["matType", "matTag", "pre_def_matTag", "OutofPlaneModulus"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "pre_def_matTag": arg_map.get("pre_def_matTag"),
            "OutofPlaneModulus": arg_map.get("OutofPlaneModulus"),
            "materialCommandType": "nDMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_PlateRebar(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `PlateRebar` Material

        nDMaterial('PlateRebar', matTag, pre_def_matTag, sita)

        rule = {
            "positional": ["matType", "matTag", "pre_def_matTag", "sita"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "pre_def_matTag": arg_map.get("pre_def_matTag"),
            "sita": arg_map.get("sita"),
            "materialCommandType": "nDMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_PlasticDamageConcretePlaneStress(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `PlasticDamageConcretePlaneStress` Material

        nDMaterial('PlasticDamageConcretePlaneStress', matTag, E, nu, ft, fc, <beta, Ap, An, Bn>)

        rule = {
            "positional": ["matType", "matTag", "E", "nu", "ft", "fc", "beta?", "Ap?", "An?", "Bn?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "E": arg_map.get("E"),
            "nu": arg_map.get("nu"),
            "ft": arg_map.get("ft"),
            "fc": arg_map.get("fc"),
            "materialCommandType": "nDMaterial"
        }

        # 添加可选参数
        optional_params = ["beta", "Ap", "An", "Bn"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info
        return material_info

    def _unknown(self, *args, **kwargs):
        # should never use this function but use MaterialManager.handle_unknown_material()
        raise NotImplementedError

    def clear(self):
        self.materials.clear()
