from typing import Any

from .._BaseHandler import SubBaseHandler


class ConcreteHandler(SubBaseHandler):
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
                "Concrete01": {
                    "positional": ["matType", "matTag", "fpc", "epsc0", "fpcu", "epscu"]
                },
                "Concrete02": {
                    "positional": ["matType", "matTag", "fpc", "epsc0", "fpcu", "epscu", "lambda", "ft", "Ets"]
                },
                "Concrete04": {
                    "positional": ["matType", "matTag", "fc", "epsc", "epscu", "Ec", "fct?", "et?", "beta?"]
                },
                "Concrete06": {
                    "positional": ["matType", "matTag", "fc", "e0", "n", "k", "alpha1", "fcr", "ecr", "b", "alpha2"]
                },
                "Concrete07": {
                    "positional": ["matType", "matTag", "fc", "epsc", "Ec", "ft", "et", "xp", "xn", "r"]
                },
                "Concrete01WithSITC": {
                    "positional": ["matType", "matTag", "fpc", "epsc0", "fpcu", "epsU", "endStrainSITC?"]
                },
                "ConfinedConcrete01": {
                    "positional": ["matType", "matTag", "secType", "fpc", "ec0", "colors"]
                },
                "ConcreteD": {
                    "positional": ["matType", "matTag", "fc", "epsc", "ft", "epst", "Ec", "alphac", "alphat", "cesp?", "etap?"]
                },
                "FRPConfinedConcrete": {
                    "positional": ["matType", "matTag", "fpc1", "fpcc", "epsc0", "D", "c", "Ej", "Sj", "tj", "eju", "S", "fyl", "fyh",
                                  "dlong", "dtrans", "Es", "v0", "k", "useBuck"]
                },
                "FRPConfinedConcrete02": {
                    "positional": ["matType", "matTag", "fc0", "Ec", "ec0", "t_wrap", "Ej", "fju", "eps_ju", "R", "Abar", "As", "Dcore"]
                },
                "ConcreteCM": {
                    "positional": ["matType", "matTag", "fpcc", "epcc", "Ec", "rc", "xcrn", "ft", "et", "rt", "xcrp", "mon"]
                },
                "TDConcrete": {
                    "positional": ["matType", "matTag", "fc", "fct", "Ec", "beta", "tD"]
                },
                "TDConcreteEXP": {
                    "positional": ["matType", "matTag", "fc", "fct", "Ec", "beta", "tD"]
                },
                "TDConcreteMC10": {
                    "positional": ["matType", "matTag", "fc", "fct", "Ec", "ecm", "beta", "tD", "cem"]
                },
                "TDConcreteMC10NL": {
                    "positional": ["matType", "matTag", "fc", "fct", "Ec", "ecm", "beta", "tD", "cem"]
                }
            }
        }

    # ---------- matType to handle ----------
    @staticmethod
    def handles() -> list[str]:
        return ["uniaxialMaterial"]

    @staticmethod
    def types() -> list[str]:
        return ["Concrete01", "Concrete02", "Concrete04", "Concrete06", "Concrete07",
                "Concrete01WithSITC", "ConfinedConcrete01", "ConcreteD", "FRPConfinedConcrete",
                "FRPConfinedConcrete02", "ConcreteCM", "TDConcrete", "TDConcreteEXP",
                "TDConcreteMC10", "TDConcreteMC10NL"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        matType = args[0]
        dispatch = {
            "Concrete01": self._handle_Concrete01,
            "Concrete02": self._handle_Concrete02,
            "Concrete04": self._handle_Concrete04,
            "Concrete06": self._handle_Concrete06,
            "Concrete07": self._handle_Concrete07,
            "Concrete01WithSITC": self._handle_Concrete01WithSITC,
            "ConfinedConcrete01": self._handle_ConfinedConcrete01,
            "ConcreteD": self._handle_ConcreteD,
            "FRPConfinedConcrete": self._handle_FRPConfinedConcrete,
            "FRPConfinedConcrete02": self._handle_FRPConfinedConcrete02,
            "ConcreteCM": self._handle_ConcreteCM,
            "TDConcrete": self._handle_TDConcrete,
            "TDConcreteEXP": self._handle_TDConcreteEXP,
            "TDConcreteMC10": self._handle_TDConcreteMC10,
            "TDConcreteMC10NL": self._handle_TDConcreteMC10NL
        }.get(matType, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_Concrete01(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `Concrete01` Material

        uniaxialMaterial('Concrete01', matTag, fpc, epsc0, fpcu, epscu)

        rule = {
            "positional": ["matType", "matTag", "fpc", "epsc0", "fpcu", "epscu"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fpc": arg_map.get("fpc"),
            "epsc0": arg_map.get("epsc0"),
            "fpcu": arg_map.get("fpcu"),
            "epscu": arg_map.get("epscu"),
        }

        self.materials[matTag] = material_info
        return material_info

    def _handle_Concrete02(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `Concrete02` Material

        uniaxialMaterial('Concrete02', matTag, fpc, epsc0, fpcu, epscu, lambda, ft, Ets)

        rule = {
            "positional": ["matType", "matTag", "fpc", "epsc0", "fpcu", "epscu", "lambda", "ft", "Ets"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fpc": arg_map.get("fpc"),
            "epsc0": arg_map.get("epsc0"),
            "fpcu": arg_map.get("fpcu"),
            "epscu": arg_map.get("epscu"),
            "lambda": arg_map.get("lambda"),
            "ft": arg_map.get("ft"),
            "Ets": arg_map.get("Ets"),
        }

        self.materials[matTag] = material_info
        return material_info

    def _handle_Concrete04(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `Concrete04` Material

        uniaxialMaterial('Concrete04', matTag, fc, epsc, epscu, Ec, fct, et, beta)

        rule = {
            "positional": ["matType", "matTag", "fc", "epsc", "epscu", "Ec", "fct?", "et?", "beta?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fc": arg_map.get("fc"),
            "epsc": arg_map.get("epsc"),
            "epscu": arg_map.get("epscu"),
            "Ec": arg_map.get("Ec"),
        }

        # 添加可选参数
        optional_params = ["fct", "et", "beta"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info
        return material_info

    def _handle_Concrete06(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `Concrete06` Material

        uniaxialMaterial('Concrete06', matTag, fc, e0, n, k, alpha1, fcr, ecr, b, alpha2)

        rule = {
            "positional": ["matType", "matTag", "fc", "e0", "n", "k", "alpha1", "fcr", "ecr", "b", "alpha2"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fc": arg_map.get("fc"),
            "e0": arg_map.get("e0"),
            "n": arg_map.get("n"),
            "k": arg_map.get("k"),
            "alpha1": arg_map.get("alpha1"),
            "fcr": arg_map.get("fcr"),
            "ecr": arg_map.get("ecr"),
            "b": arg_map.get("b"),
            "alpha2": arg_map.get("alpha2"),
        }

        self.materials[matTag] = material_info
        return material_info

    # 其他混凝土材料处理方法...
    def _handle_Concrete07(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `Concrete07` Material

        uniaxialMaterial('Concrete07', matTag, fc, epsc, Ec, ft, et, xp, xn, r)

        rule = {
            "positional": ["matType", "matTag", "fc", "epsc", "Ec", "ft", "et", "xp", "xn", "r"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fc": arg_map.get("fc"),
            "epsc": arg_map.get("epsc"),
            "Ec": arg_map.get("Ec"),
            "ft": arg_map.get("ft"),
            "et": arg_map.get("et"),
            "xp": arg_map.get("xp"),
            "xn": arg_map.get("xn"),
            "r": arg_map.get("r"),
        }

        self.materials[matTag] = material_info
        return material_info

    def _handle_Concrete01WithSITC(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `Concrete01WithSITC` Material

        uniaxialMaterial('Concrete01WithSITC', matTag, fpc, epsc0, fpcu, epsU, endStrainSITC=0.01)

        rule = {
            "positional": ["matType", "matTag", "fpc", "epsc0", "fpcu", "epsU", "endStrainSITC?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fpc": arg_map.get("fpc"),
            "epsc0": arg_map.get("epsc0"),
            "fpcu": arg_map.get("fpcu"),
            "epsU": arg_map.get("epsU"),
        }

        # 添加可选参数
        if "endStrainSITC" in arg_map:
            material_info["endStrainSITC"] = arg_map.get("endStrainSITC")

        self.materials[matTag] = material_info
        return material_info

    def _handle_ConfinedConcrete01(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `ConfinedConcrete01` Material

        uniaxialMaterial('ConfinedConcrete01', matTag, secType, fpc, Ec, epscu_type, epscu_val, nu, L1, L2, L3, phis, S, fyh, Es0, haRatio, mu, phiLon, '-internal', *internalArgs, '-wrap', *wrapArgs, '-gravel', '-silica', '-tol', tol, '-maxNumIter', maxNumIter, '-epscuLimit', epscuLimit, '-stRatio', stRatio)

        rule = {
            "positional": ["matType", "matTag", "secType", "fpc", "Ec", "epscu_type", "epscu_val", "nu", "L1", "L2", "L3", "phis", "S", "fyh", "Es0", "haRatio", "mu", "phiLon", "options"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "secType": arg_map.get("secType"),
            "fpc": arg_map.get("fpc"),
            "Ec": arg_map.get("Ec"),
            "epscu_type": arg_map.get("epscu_type"),
            "epscu_val": arg_map.get("epscu_val"),
            "nu": arg_map.get("nu"),
            "L1": arg_map.get("L1"),
            "L2": arg_map.get("L2"),
            "L3": arg_map.get("L3"),
            "phis": arg_map.get("phis"),
            "S": arg_map.get("S"),
            "fyh": arg_map.get("fyh"),
            "Es0": arg_map.get("Es0"),
            "haRatio": arg_map.get("haRatio"),
            "mu": arg_map.get("mu"),
            "phiLon": arg_map.get("phiLon"),
        }

        # 处理可选参数
        if "options" in arg_map:
            material_info["options"] = arg_map.get("options")

        self.materials[matTag] = material_info
        return material_info

    def _handle_ConcreteD(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `ConcreteD` Material

        uniaxialMaterial('ConcreteD', matTag, fc, epsc, ft, epst, Ec, alphac, alphat, cesp=0.25, etap=1.15)

        rule = {
            "positional": ["matType", "matTag", "fc", "epsc", "ft", "epst", "Ec", "alphac", "alphat", "cesp?", "etap?"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fc": arg_map.get("fc"),
            "epsc": arg_map.get("epsc"),
            "ft": arg_map.get("ft"),
            "epst": arg_map.get("epst"),
            "Ec": arg_map.get("Ec"),
            "alphac": arg_map.get("alphac"),
            "alphat": arg_map.get("alphat"),
        }

        # 添加可选参数
        optional_params = ["cesp", "etap"]
        for param in optional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info
        return material_info

    def _handle_FRPConfinedConcrete(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `FRPConfinedConcrete` Material

        uniaxialMaterial('FRPConfinedConcrete', matTag, fpc1, fpc2, epsc0, D, c, Ej, Sj, tj, eju, S, fyl, fyh, dlong, dtrans, Es, nu0, k, useBuck)

        rule = {
            "positional": ["matType", "matTag", "fpc1", "fpc2", "epsc0", "D", "c", "Ej", "Sj", "tj", "eju", "S", "fyl", "fyh", 
                          "dlong", "dtrans", "Es", "nu0", "k", "useBuck"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fpc1": arg_map.get("fpc1"),
            "fpc2": arg_map.get("fpc2"),
            "epsc0": arg_map.get("epsc0"),
            "D": arg_map.get("D"),
            "c": arg_map.get("c"),
            "Ej": arg_map.get("Ej"),
            "Sj": arg_map.get("Sj"),
            "tj": arg_map.get("tj"),
            "eju": arg_map.get("eju"),
            "S": arg_map.get("S"),
            "fyl": arg_map.get("fyl"),
            "fyh": arg_map.get("fyh"),
            "dlong": arg_map.get("dlong"),
            "dtrans": arg_map.get("dtrans"),
            "Es": arg_map.get("Es"),
            "nu0": arg_map.get("nu0"),
            "k": arg_map.get("k"),
            "useBuck": arg_map.get("useBuck"),
        }

        self.materials[matTag] = material_info
        return material_info

    def _handle_FRPConfinedConcrete02(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `FRPConfinedConcrete02` Material

        uniaxialMaterial('FRPConfinedConcrete02', matTag, fc0, Ec, ec0, <'-JacketC', tfrp, Efrp, erup, R>, <'-Ultimate', fcu, ecu>, ft, Ets, Unit)

        rule = {
            "positional": ["matType", "matTag", "fc0", "Ec", "ec0", "options"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fc0": arg_map.get("fc0"),
            "Ec": arg_map.get("Ec"),
            "ec0": arg_map.get("ec0"),
        }

        # 处理选项参数
        if "options" in arg_map:
            material_info["options"] = arg_map.get("options")

        # 处理其他必需参数
        required_params = ["ft", "Ets", "Unit"]
        for param in required_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info
        return material_info

    def _handle_ConcreteCM(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `ConcreteCM` Material

        uniaxialMaterial('ConcreteCM', matTag, fpcc, epcc, Ec, rc, xcrn, ft, et, rt, xcrp, mon, '-GapClose', GapClose=0)

        rule = {
            "positional": ["matType", "matTag", "fpcc", "epcc", "Ec", "rc", "xcrn", "ft", "et", "rt", "xcrp", "mon", "options"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fpcc": arg_map.get("fpcc"),
            "epcc": arg_map.get("epcc"),
            "Ec": arg_map.get("Ec"),
            "rc": arg_map.get("rc"),
            "xcrn": arg_map.get("xcrn"),
            "ft": arg_map.get("ft"),
            "et": arg_map.get("et"),
            "rt": arg_map.get("rt"),
            "xcrp": arg_map.get("xcrp"),
        }

        # 添加可选参数
        if "mon" in arg_map:
            material_info["mon"] = arg_map.get("mon")
    
        # 处理选项
        if "options" in arg_map:
            material_info["options"] = arg_map.get("options")

        self.materials[matTag] = material_info
        return material_info

    def _handle_TDConcrete(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `TDConcrete` Material

        uniaxialMaterial('TDConcrete', matTag, fc, fct, Ec, beta, tD, epsshu, psish, Tcr, phiu, psicr1, psicr2, tcast)

        rule = {
            "positional": ["matType", "matTag", "fc", "fct", "Ec", "beta", "tD", "epsshu", "psish", "Tcr", "phiu", "psicr1", "psicr2", "tcast"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fc": arg_map.get("fc"),
            "fct": arg_map.get("fct"),
            "Ec": arg_map.get("Ec"),
            "beta": arg_map.get("beta"),
            "tD": arg_map.get("tD"),
        }

        # 添加其他参数
        additional_params = ["epsshu", "psish", "Tcr", "phiu", "psicr1", "psicr2", "tcast"]
        for param in additional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info
        return material_info

    def _handle_TDConcreteEXP(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `TDConcreteEXP` Material

        uniaxialMaterial('TDConcreteEXP', matTag, fc, fct, Ec, beta, tD, epsshu, psish, Tcr, epscru, sigCr, psicr1, psicr2, tcast)

        rule = {
            "positional": ["matType", "matTag", "fc", "fct", "Ec", "beta", "tD", "epsshu", "psish", "Tcr", "epscru", "sigCr", "psicr1", "psicr2", "tcast"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fc": arg_map.get("fc"),
            "fct": arg_map.get("fct"),
            "Ec": arg_map.get("Ec"),
            "beta": arg_map.get("beta"),
            "tD": arg_map.get("tD"),
        }

        # 添加其他参数
        additional_params = ["epsshu", "psish", "Tcr", "epscru", "sigCr", "psicr1", "psicr2", "tcast"]
        for param in additional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info
        return material_info

    def _handle_TDConcreteMC10(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `TDConcreteMC10` Material

        uniaxialMaterial('TDConcreteMC10', matTag, fc, fct, Ec, Ecm, beta, tD, epsba, epsbb, epsda, epsdb, phiba, phibb, phida, phidb, tcast, cem)

        rule = {
            "positional": ["matType", "matTag", "fc", "fct", "Ec", "Ecm", "beta", "tD", "epsba", "epsbb", "epsda", "epsdb", "phiba", "phibb", "phida", "phidb", "tcast", "cem"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fc": arg_map.get("fc"),
            "fct": arg_map.get("fct"),
            "Ec": arg_map.get("Ec"),
            "Ecm": arg_map.get("Ecm"),
            "beta": arg_map.get("beta"),
            "tD": arg_map.get("tD"),
        }

        # 添加其他参数
        additional_params = ["epsba", "epsbb", "epsda", "epsdb", "phiba", "phibb", "phida", "phidb", "tcast", "cem"]
        for param in additional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info
        return material_info

    def _handle_TDConcreteMC10NL(self, *args, **kwargs) -> dict[str, Any]:
        """
        Handle `TDConcreteMC10NL` Material

        uniaxialMaterial('TDConcreteMC10NL', matTag, fc, fcu, epscu, fct, Ec, Ecm, beta, tD, epsba, epsbb, epsda, epsdb, phiba, phibb, phida, phidb, tcast, cem)

        rule = {
            "positional": ["matType", "matTag", "fc", "fcu", "epscu", "fct", "Ec", "Ecm", "beta", "tD", "epsba", "epsbb", "epsda", "epsdb", "phiba", "phibb", "phida", "phidb", "tcast", "cem"]
        }
        """
        arg_map = self._parse(self.handles()[0], *args, **kwargs)

        matTag = arg_map.get("matTag")
        material_info = {
            "matType": arg_map.get("matType"),
            "matTag": matTag,
            "fc": arg_map.get("fc"),
            "fcu": arg_map.get("fcu"),
            "epscu": arg_map.get("epscu"),
            "fct": arg_map.get("fct"),
            "Ec": arg_map.get("Ec"),
            "Ecm": arg_map.get("Ecm"),
            "beta": arg_map.get("beta"),
            "tD": arg_map.get("tD"),
        }

        # 添加其他参数
        additional_params = ["epsba", "epsbb", "epsda", "epsdb", "phiba", "phibb", "phida", "phidb", "tcast", "cem"]
        for param in additional_params:
            if arg_map.get(param, None) is not None:
                material_info[param] = arg_map.get(param)

        self.materials[matTag] = material_info
        return material_info

    def _unknown(self, *args, **kwargs):
        # should never use this function but use MaterialManager.handle_unknown_material()
        raise NotImplementedError(f"Unknown material type: {args[0]}")

    def clear(self):
        self.materials.clear()
