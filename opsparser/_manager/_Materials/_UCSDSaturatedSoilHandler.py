from typing import Any

from .._BaseHandler import SubBaseHandler


class UCSDSaturatedSoilHandler(SubBaseHandler):
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
                "FluidSolidPorous": {
                    "positional": ["matType", "matTag", "nd", "soilMatTag", "combinedBulkModul", "pa?"]
                }
            }
        }

    # ---------- matType to handle ----------
    @staticmethod
    def handles() -> list[str]:
        return ["nDMaterial"]

    @staticmethod
    def types() -> list[str]:
        return ["FluidSolidPorous"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        matType = args[0]
        handler_method = getattr(self, f"_handle_{matType}", self._unknown)
        return handler_method(*args, **kwargs)

    def _handle_FluidSolidPorous(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `FluidSolidPorous` Material

        nDMaterial('FluidSolidPorous', matTag, nd, soilMatTag, combinedBulkModul, pa=101.0)

        rule = {
            "positional": ["matType", "matTag", "nd", "soilMatTag", "combinedBulkModul", "pa?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "nd": arg_map.get("nd"),
            "soilMatTag": arg_map.get("soilMatTag"),
            "combinedBulkModul": arg_map.get("combinedBulkModul"),
            "materialCommandType": "nDMaterial"
        }

        # 添加可选参数
        if "pa" in arg_map:
            material_info["pa"] = arg_map.get("pa")

        self.materials[matTag] = material_info
        return material_info

    def _unknown(self, *args, **kwargs):
        # should never use this function but use MaterialManager.handle_unknown_material()
        raise NotImplementedError

    def clear(self):
        self.materials.clear()
