from typing import Any

from .._BaseHandler import SubBaseHandler


class TsinghuaSandModelsHandler(SubBaseHandler):
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
                "CycLiqCP": {
                    "positional": ["matType", "matTag", "G0", "kappa", "h", "Mfc", "dre1", "Mdc", "dre2", "rdr", "alpha", "dir", "ein", "rho"]
                },
                "CycLiqCPSP": {
                    "positional": ["matType", "matTag", "G0", "kappa", "h", "M", "dre1", "dre2", "rdr", "alpha", "dir", "lambdac", "ksi", "e0", "np", "nd", "ein", "rho"]
                }
            }
        }

    # ---------- matType to handle ----------
    @staticmethod
    def handles() -> list[str]:
        return ["nDMaterial"]

    @staticmethod
    def types() -> list[str]:
        return ["CycLiqCP", "CycLiqCPSP"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        matType = args[0]
        handler_method = getattr(self, f"_handle_{matType}", self._unknown)
        return handler_method(*args, **kwargs)

    def _handle_CycLiqCP(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `CycLiqCP` Material

        nDMaterial('CycLiqCP', matTag, G0, kappa, h, Mfc, dre1, Mdc, dre2, rdr, alpha, dir, ein, rho)

        rule = {
            "positional": ["matType", "matTag", "G0", "kappa", "h", "Mfc", "dre1", "Mdc", "dre2", "rdr", "alpha", "dir", "ein", "rho"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "G0": arg_map.get("G0"),
            "kappa": arg_map.get("kappa"),
            "h": arg_map.get("h"),
            "Mfc": arg_map.get("Mfc"),
            "dre1": arg_map.get("dre1"),
            "Mdc": arg_map.get("Mdc"),
            "dre2": arg_map.get("dre2"),
            "rdr": arg_map.get("rdr"),
            "alpha": arg_map.get("alpha"),
            "dir": arg_map.get("dir"),
            "ein": arg_map.get("ein"),
            "rho": arg_map.get("rho"),
            "materialCommandType": "nDMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _handle_CycLiqCPSP(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `CycLiqCPSP` Material

        nDMaterial('CycLiqCPSP', matTag, G0, kappa, h, M, dre1, dre2, rdr, alpha, dir, lambdac, ksi, e0, np, nd, ein, rho)

        rule = {
            "positional": ["matType", "matTag", "G0", "kappa", "h", "M", "dre1", "dre2", "rdr", "alpha", "dir", "lambdac", "ksi", "e0", "np", "nd", "ein", "rho"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "G0": arg_map.get("G0"),
            "kappa": arg_map.get("kappa"),
            "h": arg_map.get("h"),
            "M": arg_map.get("M"),
            "dre1": arg_map.get("dre1"),
            "dre2": arg_map.get("dre2"),
            "rdr": arg_map.get("rdr"),
            "alpha": arg_map.get("alpha"),
            "dir": arg_map.get("dir"),
            "lambdac": arg_map.get("lambdac"),
            "ksi": arg_map.get("ksi"),
            "e0": arg_map.get("e0"),
            "np": arg_map.get("np"),
            "nd": arg_map.get("nd"),
            "ein": arg_map.get("ein"),
            "rho": arg_map.get("rho"),
            "materialCommandType": "nDMaterial"
        }
        self.materials[matTag] = material_info
        return material_info

    def _unknown(self, *args, **kwargs):
        # should never use this function but use MaterialManager.handle_unknown_material()
        raise NotImplementedError

    def clear(self):
        self.materials.clear()
