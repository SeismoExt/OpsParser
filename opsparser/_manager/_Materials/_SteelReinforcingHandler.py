from typing import Any

from .._BaseHandler import SubBaseHandler


class SteelReinforcingHandler(SubBaseHandler):
    """Handler for Steel & Reinforcing-Steel Materials in OpenSees
    
    This handler processes all steel and reinforcing steel material types, including:
    Steel01, Steel02, Steel4, ReinforcingSteel, Dodd_Restrepo,
    RambergOsgoodSteel, SteelMPF, Steel01Thermal."""
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
                "Steel01": {
                    "positional": ["matType", "matTag", "Fy", "E0", "b", "a1?", "a2?", "a3?", "a4?"]
                },
                "Steel02": {
                    "positional": ["matType", "matTag", "Fy", "E0", "b", "R0?", "cR1?", "cR2?", "a1?", "a2?", "a3?", "a4?"]
                },
                "Steel4": {
                    "positional": ["matType", "matTag", "Fy", "E0", "b"],
                    "options": {
                        "-asym": "asym?*0",
                        "-kin": ["b_k?", "params?", "b_kc?", "R_0c?", "r_1c?", "r_2c?"],
                        "-iso": ["b_i?", "rho_i?", "b_l?", "R_i?", "l_yp?", "b_ic?", "rho_ic?", "b_lc?", "R_ic?"],
                        "-ult": ["f_u?", "R_u?", "f_uc?", "R_uc?"],
                        "-init": "sig_init?",
                        "-mem": "cycNum?"
                    }
                },
                "ReinforcingSteel": {
                    "positional": ["matType", "matTag", "fy", "fu", "Es", "Esh", "eps_sh", "eps_ult"],
                    "options": {
                        "-GABuck": ["lsr?", "beta?", "r?", "gamma?"],
                        "-DMBuck": ["lsr?", "alpha?"],
                        "-CMFatigue": ["Cf?", "alpha?", "Cd?"],
                        "-IsoHard": ["a1?", "limit?"],
                        "-MPCurveParams": ["R1?","R2?","R3?"]
                    }
                },
                "Dodd_Restrepo": {
                    "positional": ["matType", "matTag", "Fy", "Fsu", "ESH", "ESU", "Youngs", "ESHI", "FSHI", "OmegaFac?"]
                },
                "RambergOsgoodSteel": {
                    "positional": ["matType", "matTag", "fy", "E0", "a", "n"]
                },
                "SteelMPF": {
                    "positional": ["matType", "matTag", "fyp", "fyn", "E0", "bp", "bn", "params", "a1?", "a2?", "a3?", "a4?"]
                },
                "Steel01Thermal": {
                    "positional": ["matType", "matTag", "Fy", "E0", "b", "a1?", "a2?", "a3?", "a4?"]
                }
            }
        }

    # ---------- matType to handle ----------
    @staticmethod
    def handles() -> list[str]:
        return ["uniaxialMaterial"]

    @staticmethod
    def types() -> list[str]:
        return ["Steel01", "Steel02", "Steel4", "ReinforcingSteel", "Dodd_Restrepo",
                "RambergOsgoodSteel", "SteelMPF", "Steel01Thermal"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        matType = args[0]
        dispatch = {
            "Steel01": self._handle_Steel01,
            "Steel02": self._handle_Steel02,
            "Steel4": self._handle_Steel4,
            "ReinforcingSteel": self._handle_ReinforcingSteel,
            "Dodd_Restrepo": self._handle_Dodd_Restrepo,
            "RambergOsgoodSteel": self._handle_RambergOsgoodSteel,
            "SteelMPF": self._handle_SteelMPF,
            "Steel01Thermal": self._handle_Steel01Thermal
        }.get(matType, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_Steel01(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `Steel01` Material

        uniaxialMaterial('Steel01', matTag, Fy, E0, b, a1=0.0, a2=1.0, a3=0.0, a4=1.0)
        
        rule = {
            "positional": ["matType", "matTag", "Fy", "E0", "b", "a1?", "a2?", "a3?", "a4?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "Fy": arg_map.get("Fy"),
            "E0": arg_map.get("E0"),
            "b": arg_map.get("b"),
        }

        # 添加可选参数
        optional_params = ["a1", "a2", "a3", "a4"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param, 0.0 if param in ["a1", "a3"] else 1.0)

        self.materials[matTag] = material_info
        return material_info

    def _handle_Steel02(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `Steel02` Material
        
        uniaxialMaterial('Steel02', matTag, Fy, E0, b, R0=18, cR1=0.925, cR2=0.15, a1=0.0, a2=1.0, a3=0.0, a4=1.0, sigInit=0.0)
        
        rule = {
            "positional": ["matType", "matTag", "Fy", "E0", "b", "R0?", "cR1?", "cR2?", "a1?", "a2?", "a3?", "a4?", "sigInit?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "Fy": arg_map.get("Fy"),
            "E0": arg_map.get("E0"),
            "b": arg_map.get("b"),
        }

        # 添加可选参数
        optional_params = {
            "R0": 18.0,
            "cR1": 0.925,
            "cR2": 0.15,
            "a1": 0.0,
            "a2": 1.0,
            "a3": 0.0,
            "a4": 1.0,
            "sigInit": 0.0
        }

        for param, default_value in optional_params.items():
            if param in arg_map and arg_map.get(param) is not None:
                material_info[param] = arg_map.get(param)
            else:
                material_info[param] = default_value

        self.materials[matTag] = material_info
        return material_info

    def _handle_Steel4(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `Steel4` Material
        
        uniaxialMaterial('Steel4', matTag, Fy, E0, '-asym', '-kin', b_k, *params, b_kc, R_0c, r_1c, r_2c,
                         '-iso', b_i, rho_i, b_l, R_i, l_yp, b_ic, rho_ic, b_lc, R_ic,
                         '-ult', f_u, R_u, f_uc, R_uc, '-init', sig_init, '-mem', cycNum)
        
        rule = {
            "positional": ["matType", "matTag", "Fy", "E0", "b"],
            "options": {
                "-asym": "asym?*0",
                "-kin": ["b_k?", "params?", "b_kc?", "R_0c?", "r_1c?", "r_2c?"],
                "-iso": ["b_i?", "rho_i?", "b_l?", "R_i?", "l_yp?", "b_ic?", "rho_ic?", "b_lc?", "R_ic?"],
                "-ult": ["f_u?", "R_u?", "f_uc?", "R_uc?"],
                "-init": "sig_init",
                "-mem": "cycNum"
            }
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "Fy": arg_map.get("Fy"),
            "E0": arg_map.get("E0"),
            "b": arg_map.get("b"),
        }

        # 处理选项标志和相关参数
        if "-asym" in args:
            material_info["asym"] = True

        if "-kin" in args:
            R_0,r_1,r_2 = arg_map.get("params",[20,0.90,0.15])
            material_info.update({
                "b_k": arg_map.get("b_k"),
                "R_0": R_0,
                "r_1": r_1,
                "r_2": r_2,
                "b_kc": arg_map.get("b_kc"),
                "R_0c": arg_map.get("R_0c"),
                "r_1c": arg_map.get("r_1c"),
                "r_2c": arg_map.get("r_2c"),
            })

        if "-iso" in args:
            material_info.update({
                "b_i": arg_map.get("b_i"),
                "rho_i": arg_map.get("rho_i"),
                "b_l": arg_map.get("b_l"),
                "R_i": arg_map.get("R_i"),
                "l_yp": arg_map.get("l_yp"),
                "b_ic": arg_map.get("b_ic"),
                "rho_ic": arg_map.get("rho_ic"),
                "b_lc": arg_map.get("b_lc"),
                "R_ic": arg_map.get("R_ic"),
            })

        if "-ult" in args:
            material_info.update({
                "f_u": arg_map.get("f_u"),
                "R_u": arg_map.get("R_u"),
                "f_uc": arg_map.get("f_uc"),
                "R_uc": arg_map.get("R_uc"),
            })

        if "-init" in args:
            material_info["sig_init"] = arg_map.get("sig_init")

        if "-mem" in args:
            material_info["cycNum"] = arg_map.get("cycNum")

        self.materials[matTag] = material_info
        return material_info

    def _handle_ReinforcingSteel(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `ReinforcingSteel` Material
        
        uniaxialMaterial('ReinforcingSteel', matTag, fy, fu, Es, Esh, eps_sh, eps_ult, '-GABuck', lsr, beta, r, gamma,
                         '-DMBuck', lsr, alpha=1.0, '-CMFatigue', Cf, alpha, Cd, '-IsoHard', a1=4.3, limit=1.0,
                         '-MPCurveParams', R1=0.333, R2=18.0, R3=4.0)
        
        rule = {
            "positional": ["matType", "matTag", "fy", "fu", "Es", "Esh", "eps_sh", "eps_ult"],
            "options": {
                "-GABuck": ["lsr?", "beta?", "r?", "gamma?"],
                "-DMBuck": ["lsr?", "alpha?"],
                "-CMFatigue": ["Cf?", "alpha?", "Cd?"],
                "-IsoHard": ["a1?", "limit?"],
                "-MPCurveParams": ["R1?", "R2?", "R3?"]
            }
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fy": arg_map.get("fy"),
            "fu": arg_map.get("fu"),
            "Es": arg_map.get("Es"),
            "Esh": arg_map.get("Esh"),
            "eps_sh": arg_map.get("eps_sh"),
            "eps_ult": arg_map.get("eps_ult"),
        }

        # 处理选项标志和相关参数
        if "-GABuck" in args:
            material_info.update({
                "lsr": arg_map.get("lsr"),
                "beta": arg_map.get("beta"),
                "r": arg_map.get("r"),
                "gamma": arg_map.get("gamma"),
            })

        if "-DMBuck" in args:
            material_info.update({
                "lsr": arg_map.get("lsr"),
                "alpha": arg_map.get("alpha", 1.0),
            })

        if "-CMFatigue" in args:
            material_info.update({
                "Cf": arg_map.get("Cf"),
                "alpha": arg_map.get("alpha"),
                "Cd": arg_map.get("Cd"),
            })

        if "-IsoHard" in args:
            material_info.update({
                "a1": arg_map.get("a1", 4.3),
                "limit": arg_map.get("limit", 1.0),
            })

        if "-MPCurveParams" in args:
            material_info.update({
                "R1": arg_map.get("R1", 0.333),
                "R2": arg_map.get("R2", 18.0),
                "R3": arg_map.get("R3", 4.0),
            })

        self.materials[matTag] = material_info
        return material_info

    def _handle_Dodd_Restrepo(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `Dodd_Restrepo` Material
        
        uniaxialMaterial('Dodd_Restrepo', matTag, Fy, Fsu, ESH, ESU, Youngs, ESHI, FSHI, OmegaFac=1.0)
        
        rule = {
            "positional": ["matType", "matTag", "Fy", "Fsu", "ESH", "ESU", "Youngs", "ESHI", "FSHI", "OmegaFac?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "Fy": arg_map.get("Fy"),
            "Fsu": arg_map.get("Fsu"),
            "ESH": arg_map.get("ESH"),
            "ESU": arg_map.get("ESU"),
            "Youngs": arg_map.get("Youngs"),
            "ESHI": arg_map.get("ESHI"),
            "FSHI": arg_map.get("FSHI"),
        }

        # 添加可选参数
        if arg_map.get("OmegaFac"):
            material_info["OmegaFac"] = arg_map.get("OmegaFac",1.0)

        self.materials[matTag] = material_info
        return material_info

    def _handle_RambergOsgoodSteel(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `RambergOsgoodSteel` Material
        
        uniaxialMaterial('RambergOsgoodSteel', matTag, fy, E0, a, n)
        
        rule = {
            "positional": ["matType", "matTag", "fy", "E0", "a", "n"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fy": arg_map.get("fy"),
            "E0": arg_map.get("E0"),
            "a": arg_map.get("a"),
            "n": arg_map.get("n"),
        }

        self.materials[matTag] = material_info
        return material_info

    def _handle_SteelMPF(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `SteelMPF` Material
        
        uniaxialMaterial('SteelMPF', matTag, fyp, fyn, E0, bp, bn, *params, a1=0.0, a2=1.0, a3=0.0, a4=1.0)
        
        rule = {
            "positional": ["matType", "matTag", "fyp", "fyn", "E0", "bp", "bn", "params", "a1?", "a2?", "a3?", "a4?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fyp": arg_map.get("fyp"),
            "fyn": arg_map.get("fyn"),
            "E0": arg_map.get("E0"),
            "bp": arg_map.get("bp"),
            "bn": arg_map.get("bn"),
        }

        # 处理params参数列表
        if "params" in arg_map:
            material_info["params"] = arg_map.get("params")

        # 添加可选参数
        optional_params = ["a1", "a2", "a3", "a4"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param, 0.0 if param in ["a1", "a3"] else 1.0)

        self.materials[matTag] = material_info
        return material_info

    def _handle_Steel01Thermal(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `Steel01Thermal` Material
        
        uniaxialMaterial('Steel01Thermal', matTag, Fy, E0, b, a1, a2, a3, a4)
        
        rule = {
            "positional": ["matType", "matTag", "Fy", "E0", "b", "a1?", "a2?", "a3?", "a4?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "Fy": arg_map.get("Fy"),
            "E0": arg_map.get("E0"),
            "b": arg_map.get("b"),
        }

        # 添加可选参数
        optional_params = ["a1", "a2", "a3", "a4"]
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
