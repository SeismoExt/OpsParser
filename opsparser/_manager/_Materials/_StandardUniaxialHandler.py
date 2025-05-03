from typing import Any

from .._BaseHandler import SubBaseHandler


class StandardUniaxialHandler(SubBaseHandler):
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
                 "Elastic": {
                     "positional": ["matType", "matTag", "E", "eta?", "Eneg?"]
                 },
                 "ElasticPP": {
                     "positional": ["matType", "matTag", "E", "epsyP", "epsyN?", "eps0?"]
                 },
                 "ElasticPPGap": {
                     "positional": ["matType", "matTag", "E", "Fy", "gap", "eta?", "damage?"]
                 },
                 "ENT": {
                     "positional": ["matType", "matTag", "E", "minE?"]
                 },
                 "Hysteretic": {
                     "positional": ["matType", "matTag", "s1p", "e1p", "s2p", "e2p", "s3p?", "e3p?", 
                                     "s1n?", "e1n?", "s2n?", "e2n?", "s3n?", "e3n?", "pinchX?", "pinchY?", 
                                     "damage1?", "damage2?", "beta?"]
                 },
                 "Parallel": {
                     "positional": ["matType", "matTag", "tags"]
                 },
                 "Series": {
                     "positional": ["matType", "matTag", "tags"]
                 }
            }
        }

   # ---------- matType to handle ----------
    @staticmethod
    def handles() -> list[str]:
        return ["uniaxialMaterial"]

    @staticmethod
    def types() -> list[str]:
        return ["Elastic", "ElasticPP", "ElasticPPGap", "ENT", "Hysteretic", "Parallel", "Series"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        matType = args[0]
        dispatch = {
            "Elastic": self._handle_Elastic,
            "ElasticPP": self._handle_ElasticPP,
            "ElasticPPGap": self._handle_ElasticPPGap,
            "ENT": self._handle_ENT,
            "Hysteretic": self._handle_Hysteretic,
            "Parallel": self._handle_Parallel,
            "Series": self._handle_Series
        }.get(matType, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_Elastic(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `Elastic` Material

        uniaxialMaterial('Elastic', matTag, E, eta=0.0, Eneg=E)
        
        rule = {
            "positional": ["matType", "matTag", "E", "eta?", "Eneg?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "E": arg_map.get("E"),
        }

        # Add optional parameters
        optional_params = ["eta", "Eneg"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                 material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info
        return material_info

    def _handle_ElasticPP(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `ElasticPP` Material
        
        uniaxialMaterial('ElasticPP', matTag, E, epsyP, epsyN=epsyP, eps0=0.0)
        
        rule = {
            "positional": ["matType", "matTag", "E", "epsyP", "epsyN?", "eps0?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "E": arg_map.get("E"),
            "epsyP": arg_map.get("epsyP"),
        }

        # Add optional parameters
        optional_params = ["epsyN", "eps0"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                 material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info
        return material_info

    def _handle_ElasticPPGap(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `ElasticPPGap` Material
        
        uniaxialMaterial('ElasticPPGap', matTag, E, Fy, gap, eta=0.0, damage="noDamage")
        
        rule = {
            "positional": ["matType", "matTag", "E", "Fy", "gap", "eta?", "damage?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "E": arg_map.get("E"),
            "Fy": arg_map.get("Fy"),
            "gap": arg_map.get("gap"),
        }

        # Add optional parameters
        optional_params = ["eta", "damage"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                 material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info
        return material_info

    def _handle_ENT(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `ENT` Material
        
        uniaxialMaterial('ENT', matTag, E, minE=0.0)
        
        rule = {
            "positional": ["matType", "matTag", "E", "minE?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "E": arg_map.get("E"),
        }

        # Add optional parameters
        if "minE" in arg_map:
            material_info["minE"] = arg_map.get("minE")

        self.materials[matTag] = material_info
        return material_info
        
    def _handle_Hysteretic(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `Hysteretic` Material
        
        uniaxialMaterial('Hysteretic', matTag, s1p, e1p, s2p, e2p, s3p=0.0, e3p=0.0, s1n=s1p, e1n=e1p, s2n=s2p, e2n=e2p, s3n=s3p, e3n=e3p, pinchX=1.0, pinchY=1.0, damage1=0.0, damage2=0.0, beta=0.0)
        
        rule = {
            "positional": ["matType", "matTag", "s1p", "e1p", "s2p", "e2p", "s3p?", "e3p?", 
                             "s1n?", "e1n?", "s2n?", "e2n?", "s3n?", "e3n?", "pinchX?", "pinchY?", 
                             "damage1?", "damage2?", "beta?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "s1p": arg_map.get("s1p"),
            "e1p": arg_map.get("e1p"),
            "s2p": arg_map.get("s2p"),
            "e2p": arg_map.get("e2p"),
        }

        # Add all optional parameters
        optional_params = ["s3p", "e3p", "s1n", "e1n", "s2n", "e2n", "s3n", "e3n",
                            "pinchX", "pinchY", "damage1", "damage2", "beta"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                 material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info
        return material_info
        
    def _handle_Parallel(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `Parallel` Material
        
        uniaxialMaterial('Parallel', matTag, *tags)
        
        rule = {
            "positional": ["matType", "matTag", "tags"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
        }

        # Process material tag list
        if "tags" in arg_map:
            material_info["tags"] = arg_map.get("tags")
        
        # Process possible factors parameter
        if "factors" in arg_map:
            material_info["factors"] = arg_map.get("factors")

        self.materials[matTag] = material_info
        return material_info
        
    def _handle_Series(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `Series` Material
        
        uniaxialMaterial('Series', matTag, *tags)
        
        rule = {
            "positional": ["matType", "matTag", "tags"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
        }

        # Process material tag list
        if "tags" in arg_map:
            material_info["tags"] = arg_map.get("tags")

        self.materials[matTag] = material_info
        return material_info

    def _unknown(self, *args, **kwargs):
        # Should never use this function but use MaterialManager.handle_unknown_material()
        raise NotImplementedError

    def clear(self):
        self.materials.clear()
