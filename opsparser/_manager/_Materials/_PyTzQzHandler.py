from typing import Any

from .._BaseHandler import SubBaseHandler


class PyTzQzHandler(SubBaseHandler):
    """Handler for Py-Tz-Qz Materials in OpenSees
    
    This handler processes all Py-Tz-Qz material types, including:
    PySimple1, TzSimple1, QzSimple1, PyLiq1, TzLiq1, QzLiq1."""
    def __init__(self, registry: dict[str, dict], materials_store: dict[int, dict]):
        """
        registry: matType → handler global mapping (for manager generation)
        materials_store: Shared reference to MaterialManager.materials
        """
        self.materials = materials_store
        self._register(registry)

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        return {
            "uniaxialMaterial": {
                "alternative": True,
                "PySimple1": {
                    "positional": ["matType", "matTag", "soilType", "pult", "Y50", "Cd", "c?"]
                },
                "TzSimple1": {
                    "positional": ["matType", "matTag", "soilType", "tult", "z50", "c?"]
                },
                "QzSimple1": {
                    "positional": ["matType", "matTag", "qzType", "qult", "Z50", "suction?", "c?"]
                },
                "PyLiq1": {
                    "positional": ["matType", "matTag", "soilType", "pult", "Y50", "Cd", "c", "pRes", "ele1?", "ele2?"],
                    "options": {"-timeSeries": "timeSeriesTag"}
                },
                "TzLiq1": {
                    "positional": ["matType", "matTag", "tzType", "tult", "z50", "c", "ele1?", "ele2?"],
                    "options": {"-timeSeries": "timeSeriesTag"}
                },
                "QzLiq1": {
                    "positional": ["matType", "matTag", "soilType", "qult", "Z50", "Cd", "c", "alpha", "ele1?", "ele2?"],
                    "options": {"-timeSeries": "timeSeriesTag"}
                },
            }
        }

    # ---------- matType to handle ----------
    @staticmethod
    def handles() -> list[str]:
        return ["uniaxialMaterial"]

    @staticmethod
    def types() -> list[str]:
        return ["PySimple1", "TzSimple1", "QzSimple1", "PyLiq1", "TzLiq1", "QzLiq1"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        matType = args[0]

        dispatch = {
            "PySimple1": self._handle_PySimple1,
            "TzSimple1": self._handle_TzSimple1,
            "QzSimple1": self._handle_QzSimple1,
            "PyLiq1": self._handle_PyLiq1,
            "TzLiq1": self._handle_TzLiq1,
            "QzLiq1": self._handle_QzLiq1,
        }.get(matType, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_PySimple1(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `PySimple1` Material

        uniaxialMaterial('PySimple1', matTag, soilType, pult, Y50, Cd, c=0.0)

        rule = {
            "positional": ["matType", "matTag", "soilType", "pult", "Y50", "Cd", "c?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "soilType": arg_map.get("soilType"),
            "pult": arg_map.get("pult"),
            "Y50": arg_map.get("Y50"),
            "Cd": arg_map.get("Cd")
        }

        # 添加可选参数
        if "c" in arg_map:
            material_info["c"] = arg_map.get("c")

        self.materials[matTag] = material_info
        return material_info

    def _handle_TzSimple1(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `TzSimple1` Material

        uniaxialMaterial('TzSimple1', matTag, soilType, tult, z50, c=0.0)
        
        rule = {
            "positional": ["matType", "matTag", "soilType", "tult", "z50", "c?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "soilType": arg_map.get("soilType"),
            "tult": arg_map.get("tult"),
            "z50": arg_map.get("z50")
        }

        # 添加可选参数
        if "c" in arg_map:
            material_info["c"] = arg_map.get("c")

        self.materials[matTag] = material_info
        return material_info

    def _handle_QzSimple1(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `QzSimple1` Material

        uniaxialMaterial('QzSimple1', matTag, qzType, qult, Z50, suction=0.0, c=0.0)
        
        rule = {
            "positional": ["matType", "matTag", "qzType", "qult", "Z50", "suction?", "c?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "qzType": arg_map.get("qzType"),
            "qult": arg_map.get("qult"),
            "Z50": arg_map.get("Z50")
        }

        # 添加可选参数
        optional_params = ["suction", "c"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info
        return material_info

    def _handle_PyLiq1(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `PyLiq1` Material (with element references)

        uniaxialMaterial('PyLiq1', matTag, soilType, pult, Y50, Cd, c, pRes, ele1, ele2)

        (with time series)
        uniaxialMaterial('PyLiq1', matTag, soilType, pult, Y50, Cd, c, pRes, '-timeSeries', timeSeriesTag)

        rule = {
            "positional": ["matType", "matTag", "soilType", "pult", "Y50", "Cd", "c", "pRes", "ele1?", "ele2?"],
            "options": {"-timeSeries": "timeSeriesTag"}
        },
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "soilType": arg_map.get("soilType"),
            "pult": arg_map.get("pult"),
            "Y50": arg_map.get("Y50"),
            "Cd": arg_map.get("Cd"),
            "c": arg_map.get("c"),
            "pRes": arg_map.get("pRes"),
        }

        if arg_map.get("ele1"):
            material_info["ele1"] = arg_map.get("ele1")

        if arg_map.get("ele2"):
            material_info["ele2"] = arg_map.get("ele2")

        if "-timeSeries" in args:
            material_info["timeSeriesTag"] = arg_map.get("timeSeriesTag")

        self.materials[matTag] = material_info
        return material_info

    def _handle_TzLiq1(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `TzLiq1` Material (with element references)

        uniaxialMaterial('TzLiq1', matTag, tzType, tult, z50, c, ele1, ele2)
        
        (with time series)
        uniaxialMaterial('TzLiq1', matTag, tzType, tult, z50, c, '-timeSeries', timeSeriesTag)
        
        rule = {
            "positional": ["matType", "matTag", "tzType", "tult", "z50", "c", "ele1?", "ele2?"],
            "options": {"-timeSeries": "timeSeriesTag"}
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "tzType": arg_map.get("tzType"),
            "tult": arg_map.get("tult"),
            "z50": arg_map.get("z50"),
            "c": arg_map.get("c"),
        }

        if arg_map.get("ele1"):
            material_info["ele1"] = arg_map.get("ele1")

        if arg_map.get("ele2"):
            material_info["ele2"] = arg_map.get("ele2")

        if "-timeSeries" in args:
            material_info["timeSeriesTag"] = arg_map.get("timeSeriesTag")

        self.materials[matTag] = material_info
        return material_info

    def _handle_QzLiq1(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `QzLiq1` Material (with element references)

        uniaxialMaterial('QzLiq1', matTag, soilType, qult, Z50, Cd, c, alpha, ele1, ele2)
        
        (with time series)
        uniaxialMaterial('QzLiq1', matTag, soilType, qult, Z50, Cd, c, alpha, '-timeSeries', timeSeriesTag)
        
        rule = {
            "positional": ["matType", "matTag", "soilType", "qult", "Z50", "Cd", "c", "alpha", "ele1?", "ele2?"],
            "options": {"-timeSeries": "timeSeriesTag"}
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "soilType": arg_map.get("soilType"),
            "qult": arg_map.get("qult"),
            "Z50": arg_map.get("Z50"),
            "Cd": arg_map.get("Cd"),
            "c": arg_map.get("c"),
            "alpha": arg_map.get("alpha"),
        }

        if arg_map.get("ele1"):
            material_info["ele1"] = arg_map.get("ele1")

        if arg_map.get("ele2"):
            material_info["ele2"] = arg_map.get("ele2")

        if "-timeSeries" in args:
            material_info["timeSeriesTag"] = arg_map.get("timeSeriesTag")

        self.materials[matTag] = material_info
        return material_info

    def _unknown(self, *args, **kwargs):
        # should never use this function but use MaterialManager.handle_unknown_material()
        raise NotImplementedError

    def clear(self):
        self.materials.clear()
