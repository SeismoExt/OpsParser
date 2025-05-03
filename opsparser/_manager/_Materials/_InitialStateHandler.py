from typing import Any

from .._BaseHandler import SubBaseHandler


class InitialStateHandler(SubBaseHandler):
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
                "InitialStateAnalysisWrapper": {
                    "positional": ["matType", "matTag", "nDMatTag", "nDim"]
                },
                "InitStressNDMaterial": {
                    "positional": ["matType", "matTag", "otherTag", "initStress", "nDim"]
                },
                "InitStrainNDMaterial": {
                    "positional": ["matType", "matTag", "otherTag", "initStrain", "nDim"]
                }
            }
        }

    # ---------- matType to handle ----------
    @staticmethod
    def handles() -> list[str]:
        return ["nDMaterial"]

    @staticmethod
    def types() -> list[str]:
        return ["InitialStateAnalysisWrapper", "InitStressNDMaterial", "InitStrainNDMaterial"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        matType = args[0]
        handler_method = getattr(self, f"_handle_{matType}", self._unknown)
        return handler_method(*args, **kwargs)

    def _handle_InitialStateAnalysisWrapper(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `InitialStateAnalysisWrapper` Material

        nDMaterial('InitialStateAnalysisWrapper', matTag, nDMatTag, nDim)

        rule = {
            "positional": ["matType", "matTag", "nDMatTag", "nDim"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "nDMatTag": arg_map.get("nDMatTag"),
            "nDim": arg_map.get("nDim"),
            "materialCommandType": "nDMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_InitStressNDMaterial(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `InitStressNDMaterial` Material

        nDMaterial('InitStressNDMaterial', matTag, otherTag, initStress, nDim)

        rule = {
            "positional": ["matType", "matTag", "otherTag", "initStress", "nDim"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "otherTag": arg_map.get("otherTag"),
            "initStress": arg_map.get("initStress"),
            "nDim": arg_map.get("nDim"),
            "materialCommandType": "nDMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_InitStrainNDMaterial(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `InitStrainNDMaterial` Material

        nDMaterial('InitStrainNDMaterial', matTag, otherTag, initStrain, nDim)

        rule = {
            "positional": ["matType", "matTag", "otherTag", "initStrain", "nDim"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "otherTag": arg_map.get("otherTag"),
            "initStrain": arg_map.get("initStrain"),
            "nDim": arg_map.get("nDim"),
            "materialCommandType": "nDMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _unknown(self, *args, **kwargs):
        # should never use this function but use MaterialManager.handle_unknown_material()
        raise NotImplementedError

    def clear(self):
        self.materials.clear()
