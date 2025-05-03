from typing import Any

from .._BaseHandler import SubBaseHandler


class ContactMaterialsHandler(SubBaseHandler):
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
                "ContactMaterial2D": {
                    "positional": ["matType", "matTag", "mu", "G", "c", "t"]
                },
                "ContactMaterial3D": {
                    "positional": ["matType", "matTag", "mu", "G", "c", "t"]
                }
            }
        }

    # ---------- matType to handle ----------
    @staticmethod
    def handles() -> list[str]:
        return ["nDMaterial"]

    @staticmethod
    def types() -> list[str]:
        return ["ContactMaterial2D", "ContactMaterial3D"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        matType = args[0]
        handler_method = getattr(self, f"_handle_{matType}", self._unknown)
        return handler_method(*args, **kwargs)

    def _handle_ContactMaterial2D(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `ContactMaterial2D` Material

        nDMaterial('ContactMaterial2D', matTag, mu, G, c, t)

        rule = {
            "positional": ["matType", "matTag", "mu", "G", "c", "t"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "mu": arg_map.get("mu"),
            "G": arg_map.get("G"),
            "c": arg_map.get("c"),
            "t": arg_map.get("t"),
            "materialCommandType": "nDMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_ContactMaterial3D(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `ContactMaterial3D` Material

        nDMaterial('ContactMaterial3D', matTag, mu, G, c, t)

        rule = {
            "positional": ["matType", "matTag", "mu", "G", "c", "t"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "mu": arg_map.get("mu"),
            "G": arg_map.get("G"),
            "c": arg_map.get("c"),
            "t": arg_map.get("t"),
            "materialCommandType": "nDMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _unknown(self, *args, **kwargs):
        # should never use this function but use MaterialManager.handle_unknown_material()
        raise NotImplementedError

    def clear(self):
        self.materials.clear()
