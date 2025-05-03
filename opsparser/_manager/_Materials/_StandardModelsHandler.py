from typing import Any

from .._BaseHandler import SubBaseHandler


class StandardModelsHandler(SubBaseHandler):
    def __init__(self, registry: dict[str, dict], materials_store: dict[int, dict]):
        """
        registry: matType → handler  的全局映射 (供 manager 生成)
        materials_store: MaterialManager.materials 共享引用
        """
        self.materials = materials_store
        self._register(registry)

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        return {
            "nDMaterial": {
                "alternative":True,
                "ElasticIsotropic": {
                    "positional": ["matType", "matTag", "E", "nu", "rho?"]
                },
                "ElasticOrthotropic": {
                    "positional": ["matType", "matTag", "Ex", "Ey", "Ez", "nu_xy", "nu_yz", "nu_zx", "Gxy", "Gyz", "Gzx", "rho?"]
                },
                "J2Plasticity": {
                    "positional": ["matType", "matTag", "K", "G", "sig0", "sigInf", "delta", "H"]
                },
                "DruckerPrager": {
                    "positional": ["matType", "matTag", "K", "G", "sigmaY", "rho", "rhoBar", "Kinf", "Ko", "delta1", "delta2", "H", "theta", "density", "atmPressure?"]
                },
                "PlaneStress": {
                    "positional": ["matType", "matTag", "mat3DTag"]
                },
                "PlaneStrain": {
                    "positional": ["matType", "matTag", "mat3DTag"]
                },
                "MultiaxialCyclicPlasticity": {
                    "positional": ["matType", "matTag", "rho", "K", "G", "Su", "Ho", "h", "m", "beta", "KCoeff"]
                },
                "BoundingCamClay": {
                    "positional": ["matType", "matTag", "massDensity", "C", "bulkMod", "OCR", "mu_o", "alpha", "lambda", "h", "m"]
                },
                "PlateFiber": {
                    "positional": ["matType", "matTag", "threeDTag"]
                },
                "FSAM": {
                    "positional": ["matType", "matTag", "rho", "sXTag", "sYTag", "concTag", "rouX", "rouY", "nu", "alfadow"]
                },
                "ManzariDafalias": {
                    "positional": ["matType", "matTag", "G0", "nu", "e_init", "Mc", "c", "lambda_c", "e0", "ksi", "P_atm", "m", "h0", "ch", "nb", "A0", "nd", "z_max", "cz", "Den"]
                },
                "PM4Sand": {
                    "positional": ["matType", "matTag", "D_r", "G_o", "h_po", "Den", "P_atm?", "h_o?", "e_max?", "e_min?", "n_b?", "n_d?", "A_do?", "z_max?", "c_z?", "c_e?", "phi_cv?", "nu?", "g_degr?", "c_dr?", "c_kaf?", "Q_bolt?", "R_bolt?", "m_par?", "F_sed?", "p_sed?"]
                },
                "PM4Silt": {
                    "positional": ["matType", "matTag", "S_u", "Su_Rat", "G_o", "h_po", "Den", "Su_factor?", "P_atm?", "nu?", "nG?", "h0?", "eInit?", "lambda?", "phicv?", "nb_wet?", "nb_dry?", "nd?", "Ado?", "ru_max?", "z_max?", "cz?", "ce?", "cgd?", "ckaf?", "m_m?", "CG_consol?"]
                },
                "StressDensityModel": {
                    "positional": ["matType", "matTag", "mDen", "eNot", "A", "n", "nu", "a1", "b1", "a2", "b2", "a3", "b3", "fd", "muNot", "muCyc", "sc", "M", "patm", "ssls", "hsl", "p1"]
                },
                "AcousticMedium": {
                    "positional": ["matType", "matTag", "K", "rho"]
                }
            }
        }


     # ---------- matType to handle ----------
    @staticmethod
    def handles() -> list[str]:
        return ["nDMaterial"]

    @staticmethod
    def types() -> list[str]:
        return [
            "ElasticIsotropic", "ElasticOrthotropic", "J2Plasticity", "DruckerPrager",
            "PlaneStress", "PlaneStrain", "MultiaxialCyclicPlasticity", "BoundingCamClay",
            "PlateFiber", "FSAM", "ManzariDafalias", "PM4Sand", "PM4Silt",
            "StressDensityModel", "AcousticMedium"
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "ElasticIsotropic": self._handle_ElasticIsotropic,
            "ElasticOrthotropic": self._handle_ElasticOrthotropic,
            "J2Plasticity": self._handle_J2Plasticity,
            "DruckerPrager": self._handle_DruckerPrager,
            "PlaneStress": self._handle_PlaneStress,
            "PlaneStrain": self._handle_PlaneStrain,
            "MultiaxialCyclicPlasticity": self._handle_MultiaxialCyclicPlasticity,
            "BoundingCamClay": self._handle_BoundingCamClay,
            "PlateFiber": self._handle_PlateFiber,
            "FSAM": self._handle_FSAM,
            "ManzariDafalias": self._handle_ManzariDafalias,
            "PM4Sand": self._handle_PM4Sand,
            "PM4Silt": self._handle_PM4Silt,
            "StressDensityModel": self._handle_StressDensityModel,
            "AcousticMedium": self._handle_AcousticMedium
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_ElasticIsotropic(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `ElasticIsotropic` Material

        nDMaterial('ElasticIsotropic', matTag, E, nu, rho=0.0)

        rule = {
            "positional": ["matType", "matTag", "E", "nu", "rho?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "E": arg_map.get("E"),
            "nu": arg_map.get("nu"),
        }
        if arg_map.get("rho"):
            material_info["rho"] = arg_map.get("rho",0.0)

        self.materials[matTag] = material_info

    def _handle_ElasticOrthotropic(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `ElasticOrthotropic` Material

        nDMaterial('ElasticOrthotropic', matTag, Ex, Ey, Ez, nu_xy, nu_yz, nu_zx, Gxy, Gyz, Gzx, rho=0.0)

        rule = {
            "positional": ["matType", "matTag", "Ex", "Ey", "Ez", "nu_xy", "nu_yz", "nu_zx", "Gxy", "Gyz", "Gzx", "rho?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "Ex": arg_map.get("Ex"),
            "Ey": arg_map.get("Ey"),
            "Ez": arg_map.get("Ez"),
            "nu_xy": arg_map.get("nu_xy"),
            "nu_yz": arg_map.get("nu_yz"),
            "nu_zx": arg_map.get("nu_zx"),
            "Gxy": arg_map.get("Gxy"),
            "Gyz": arg_map.get("Gyz"),
            "Gzx": arg_map.get("Gzx")
        }
        if arg_map.get("rho"):
            material_info["rho"] = arg_map.get("rho", 0.0)

        self.materials[matTag] = material_info

    def _handle_J2Plasticity(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `J2Plasticity` Material

        nDMaterial('J2Plasticity', matTag, K, G, sig0, sigInf, delta, H)

        rule = {
            "positional": ["matType", "matTag", "K", "G", "sig0", "sigInf", "delta", "H"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "K": arg_map.get("K"),
            "G": arg_map.get("G"),
            "sig0": arg_map.get("sig0"),
            "sigInf": arg_map.get("sigInf"),
            "delta": arg_map.get("delta"),
            "H": arg_map.get("H")
        }
        self.materials[matTag] = material_info

    def _handle_DruckerPrager(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `DruckerPrager` Material

        nDMaterial('DruckerPrager', matTag, K, G, sigmaY, rho, rhoBar, Kinf, Ko, delta1, delta2, H, theta, density, atmPressure=101e3)

        rule = {
            "positional": ["matType", "matTag", "K", "G", "sigmaY", "rho", "rhoBar", "Kinf", "Ko", "delta1", "delta2", "H", "theta", "density", "atmPressure?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "K": arg_map.get("K"),
            "G": arg_map.get("G"),
            "sigmaY": arg_map.get("sigmaY"),
            "rho": arg_map.get("rho"),
            "rhoBar": arg_map.get("rhoBar"),
            "Kinf": arg_map.get("Kinf"),
            "Ko": arg_map.get("Ko"),
            "delta1": arg_map.get("delta1"),
            "delta2": arg_map.get("delta2"),
            "H": arg_map.get("H"),
            "theta": arg_map.get("theta"),
            "density": arg_map.get("density")
        }
        if arg_map.get("atmPressure"):
            material_info["atmPressure"] = arg_map.get("atmPressure", 101e3)

        self.materials[matTag] = material_info

    def _handle_PlaneStress(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `PlaneStress` Material

        nDMaterial('PlaneStress', matTag, mat3DTag)

        rule = {
            "positional": ["matType", "matTag", "mat3DTag"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "mat3DTag": arg_map.get("mat3DTag")
        }
        self.materials[matTag] = material_info

    def _handle_PlaneStrain(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `PlaneStrain` Material

        nDMaterial('PlaneStrain', matTag, mat3DTag)

        rule = {
            "positional": ["matType", "matTag", "mat3DTag"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "mat3DTag": arg_map.get("mat3DTag")
        }
        self.materials[matTag] = material_info

    def _handle_PlateFiber(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `PlateFiber` Material

        nDMaterial('PlateFiber', matTag, threeDTag)

        rule = {
            "positional": ["matType", "matTag", "threeDTag"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "threeDTag": arg_map.get("threeDTag")
        }
        self.materials[matTag] = material_info

    def _handle_MultiaxialCyclicPlasticity(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `MultiaxialCyclicPlasticity` Material

        nDMaterial('MultiaxialCyclicPlasticity', matTag, rho, K, G, Su, Ho, h, m, beta, KCoeff)

        rule = {
            "positional": ["matType", "matTag", "rho", "K", "G", "Su", "Ho", "h", "m", "beta", "KCoeff"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "rho": arg_map.get("rho"),
            "K": arg_map.get("K"),
            "G": arg_map.get("G"),
            "Su": arg_map.get("Su"),
            "Ho": arg_map.get("Ho"),
            "h": arg_map.get("h"),
            "m": arg_map.get("m"),
            "beta": arg_map.get("beta"),
            "KCoeff": arg_map.get("KCoeff")
        }
        self.materials[matTag] = material_info

    def _handle_BoundingCamClay(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `BoundingCamClay` Material

        nDMaterial('BoundingCamClay', matTag, massDensity, C, bulkMod, OCR, mu_o, alpha, lambda, h, m)

        rule = {
            "positional": ["matType", "matTag", "massDensity", "C", "bulkMod", "OCR", "mu_o", "alpha", "lambda", "h", "m"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "massDensity": arg_map.get("massDensity"),
            "C": arg_map.get("C"),
            "bulkMod": arg_map.get("bulkMod"),
            "OCR": arg_map.get("OCR"),
            "mu_o": arg_map.get("mu_o"),
            "alpha": arg_map.get("alpha"),
            "lambda": arg_map.get("lambda"),
            "h": arg_map.get("h"),
            "m": arg_map.get("m")
        }
        self.materials[matTag] = material_info

    def _handle_FSAM(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `FSAM` Material

        nDMaterial('FSAM', matTag, rho, sXTag, sYTag, concTag, rouX, rouY, nu, alfadow)

        rule = {
            "positional": ["matType", "matTag", "rho", "sXTag", "sYTag", "concTag", "rouX", "rouY", "nu", "alfadow"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "rho": arg_map.get("rho"),
            "sXTag": arg_map.get("sXTag"),
            "sYTag": arg_map.get("sYTag"),
            "concTag": arg_map.get("concTag"),
            "rouX": arg_map.get("rouX"),
            "rouY": arg_map.get("rouY"),
            "nu": arg_map.get("nu"),
            "alfadow": arg_map.get("alfadow")
        }
        self.materials[matTag] = material_info

    def _handle_ManzariDafalias(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `ManzariDafalias` Material

        nDMaterial('ManzariDafalias', matTag, G0, nu, e_init, Mc, c, lambda_c, e0, ksi, P_atm, m, h0, ch, nb, A0, nd, z_max, cz, Den)

        rule = {
            "positional": ["matType", "matTag", "G0", "nu", "e_init", "Mc", "c", "lambda_c", "e0", "ksi", "P_atm", "m", "h0", "ch", "nb", "A0", "nd", "z_max", "cz", "Den"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "G0": arg_map.get("G0"),
            "nu": arg_map.get("nu"),
            "e_init": arg_map.get("e_init"),
            "Mc": arg_map.get("Mc"),
            "c": arg_map.get("c"),
            "lambda_c": arg_map.get("lambda_c"),
            "e0": arg_map.get("e0"),
            "ksi": arg_map.get("ksi"),
            "P_atm": arg_map.get("P_atm"),
            "m": arg_map.get("m"),
            "h0": arg_map.get("h0"),
            "ch": arg_map.get("ch"),
            "nb": arg_map.get("nb"),
            "A0": arg_map.get("A0"),
            "nd": arg_map.get("nd"),
            "z_max": arg_map.get("z_max"),
            "cz": arg_map.get("cz"),
            "Den": arg_map.get("Den")
        }
        self.materials[matTag] = material_info

    def _handle_PM4Sand(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `PM4Sand` Material

        nDMaterial('PM4Sand', matTag, D_r, G_o, h_po, Den, P_atm?, h_o?, e_max?, e_min?, n_b?, n_d?, A_do?, z_max?, c_z?, c_e?, phi_cv?, nu?, g_degr?, c_dr?, c_kaf?, Q_bolt?, R_bolt?, m_par?, F_sed?, p_sed?)

        rule = {
            "positional": ["matType", "matTag", "D_r", "G_o", "h_po", "Den", "P_atm?", "h_o?", "e_max?", "e_min?", "n_b?", "n_d?", "A_do?", "z_max?", "c_z?", "c_e?", "phi_cv?", "nu?", "g_degr?", "c_dr?", "c_kaf?", "Q_bolt?", "R_bolt?", "m_par?", "F_sed?", "p_sed?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "D_r": arg_map.get("D_r"),
            "G_o": arg_map.get("G_o"),
            "h_po": arg_map.get("h_po"),
            "Den": arg_map.get("Den")
        }

        # 添加可选参数
        optional_params = ["P_atm", "h_o", "e_max", "e_min", "n_b", "n_d", "A_do",
                          "z_max", "c_z", "c_e", "phi_cv", "nu", "g_degr", "c_dr",
                          "c_kaf", "Q_bolt", "R_bolt", "m_par", "F_sed", "p_sed"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info

    def _handle_PM4Silt(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `PM4Silt` Material

        nDMaterial('PM4Silt', matTag, S_u, Su_Rat, G_o, h_po, Den, Su_factor?, P_atm?, nu?, nG?, h0?, eInit?, lambda?, phicv?, nb_wet?, nb_dry?, nd?, Ado?, ru_max?, z_max?, cz?, ce?, cgd?, ckaf?, m_m?, CG_consol?)

        rule = {
            "positional": ["matType", "matTag", "S_u", "Su_Rat", "G_o", "h_po", "Den", "Su_factor?", "P_atm?", "nu?", "nG?", "h0?", "eInit?", "lambda?", "phicv?", "nb_wet?", "nb_dry?", "nd?", "Ado?", "ru_max?", "z_max?", "cz?", "ce?", "cgd?", "ckaf?", "m_m?", "CG_consol?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "S_u": arg_map.get("S_u"),
            "Su_Rat": arg_map.get("Su_Rat"),
            "G_o": arg_map.get("G_o"),
            "h_po": arg_map.get("h_po"),
            "Den": arg_map.get("Den")
        }

        # 添加可选参数
        optional_params = ["Su_factor", "P_atm", "nu", "nG", "h0", "eInit", "lambda",
                          "phicv", "nb_wet", "nb_dry", "nd", "Ado", "ru_max", "z_max",
                          "cz", "ce", "cgd", "ckaf", "m_m", "CG_consol"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info

    def _handle_StressDensityModel(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `StressDensityModel` Material

        nDMaterial('StressDensityModel', matTag, mDen, eNot, A, n, nu, a1, b1, a2, b2, a3, b3, fd, muNot, muCyc, sc, M, patm, ssls*, hsl, p1)

        rule = {
            "positional": ["matType", "matTag", "mDen", "eNot", "A", "n", "nu", "a1", "b1", "a2", "b2", "a3", "b3", "fd", "muNot", "muCyc", "sc", "M", "patm", "ssls", "hsl", "p1"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "mDen": arg_map.get("mDen"),
            "eNot": arg_map.get("eNot"),
            "A": arg_map.get("A"),
            "n": arg_map.get("n"),
            "nu": arg_map.get("nu"),
            "a1": arg_map.get("a1"),
            "b1": arg_map.get("b1"),
            "a2": arg_map.get("a2"),
            "b2": arg_map.get("b2"),
            "a3": arg_map.get("a3"),
            "b3": arg_map.get("b3"),
            "fd": arg_map.get("fd"),
            "muNot": arg_map.get("muNot"),
            "muCyc": arg_map.get("muCyc"),
            "sc": arg_map.get("sc"),
            "M": arg_map.get("M"),
            "patm": arg_map.get("patm")
        }

        # 处理特殊参数
        if arg_map.get("ssls"):
            material_info["ssls"] = arg_map.get("ssls")
        if arg_map.get("hsl"):
            material_info["hsl"] = arg_map.get("hsl")
        if arg_map.get("p1"):
            material_info["p1"] = arg_map.get("p1")

        self.materials[matTag] = material_info

    def _handle_AcousticMedium(self, *args, **kwargs) -> dict[str, Any]:
        """
        handle `AcousticMedium` Material

        nDMaterial('AcousticMedium', matTag, K, rho)

        rule = {
            "positional": ["matType", "matTag", "K", "rho"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "K": arg_map.get("K"),
            "rho": arg_map.get("rho")
        }
        self.materials[matTag] = material_info

    def _unknown(self, *args, **kwargs):
        # should never use this function but use MaterialManager.handle_unknown_material()
        raise NotImplementedError

    def clear(self):
        self.materials.clear()
