from typing import Any

import openseespy.opensees as ops

from .._BaseHandler import SubBaseHandler


class BearingHandler(SubBaseHandler):
    def __init__(self, registry: dict[str, dict], element_store: dict[int, dict]):
        """
        registry: eleType → handler 的全局映射 (供 manager 生成)
        element_store: ElementManager.elements 共享引用
        """
        self.elements = element_store
        self._register(registry)

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        rules = {"alternative": True}

        # 获取维度信息
        ndm = ops.getNDM()[0]
        assert len(ops.getNDM()) == 1, f"Invalid length of ndm, expected 1, got {len(ops.getNDM()) =}"  # noqa: S101

        # 添加不同支座类型的规则
        # elastomericBearingPlasticity 规则
        if ndm == 2:
            rules["elastomericBearingPlasticity"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2", "kInit", "qd", "alpha1", "alpha2", "mu"],
                "options": {
                    "-P": "PMatTag",
                    "-Mz": "MzMatTag",
                    "-orient?": "orientVals*6",
                    "-shearDist?": "sDratio",
                    "-doRayleigh?*0": "doRayleigh",
                    "-mass?": "m",
                }
            }
        elif ndm == 3:
            rules["elastomericBearingPlasticity"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2", "kInit", "qd", "alpha1", "alpha2", "mu"],
                "options": {
                    "-P": "PMatTag",
                    "-T": "TMatTag",
                    "-My": "MyMatTag",
                    "-Mz": "MzMatTag",
                    "-orient?": "orientVals*9",
                    "-shearDist?": "sDratio",
                    "-doRayleigh?*0": "doRayleigh",
                    "-mass?": "m",
                }
            }

        # elastomericBearingBoucWen 规则
        if ndm == 2:
            rules["elastomericBearingBoucWen"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2", "kInit", "qd", "alpha1", "alpha2", "mu", "eta", "beta", "gamma"],
                "options": {
                    "-P": "PMatTag",
                    "-Mz": "MzMatTag",
                    "-orient?": "orientVals*6",
                    "-shearDist?": "sDratio",
                    "-doRayleigh?*0": "doRayleigh",
                    "-mass?": "m",
                }
            }
        elif ndm == 3:
            rules["elastomericBearingBoucWen"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2", "kInit", "qd", "alpha1", "alpha2", "mu", "eta", "beta", "gamma"],
                "options": {
                    "-P": "PMatTag",
                    "-T": "TMatTag",
                    "-My": "MyMatTag",
                    "-Mz": "MzMatTag",
                    "-orient?": "orientVals*9",
                    "-shearDist?": "sDratio",
                    "-doRayleigh?*0": "doRayleigh",
                    "-mass?": "m",
                }
            }

        # flatSliderBearing 规则
        if ndm == 2:
            rules["flatSliderBearing"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2", "frnMdlTag", "kInit"],
                "options": {
                    "-P": "PMatTag",
                    "-Mz": "MzMatTag",
                    "-orient?": "orientVals*6",
                    "-shearDist?": "sDratio",
                    "-doRayleigh?*0": "doRayleigh",
                    "-mass?": "m",
                    "-maxIter?": ["iter", "tol"],
                }
            }
        elif ndm == 3:
            rules["flatSliderBearing"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2", "frnMdlTag", "kInit"],
                "options": {
                    "-P": "PMatTag",
                    "-T": "TMatTag",
                    "-My": "MyMatTag",
                    "-Mz": "MzMatTag",
                    "-orient?": "orientVals*9",
                    "-shearDist?": "sDratio",
                    "-doRayleigh?*0": "doRayleigh",
                    "-mass?": "m",
                    "-iter?": ["maxIter", "tol"],
                }
            }

        # singleFPBearing 规则
        if ndm == 2:
            rules["singleFPBearing"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2", "frnMdlTag", "Reff", "kInit"],
                "options": {
                    "-P": "PMatTag",
                    "-Mz": "MzMatTag",
                    "-orient?": "orientVals*6",
                    "-shearDist?": "sDratio",
                    "-doRayleigh?*0": "doRayleigh",
                    "-mass?": "m",
                    "-iter?": ["maxIter", "tol"],
                }
            }
        elif ndm == 3:
            rules["singleFPBearing"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2", "frnMdlTag", "Reff", "kInit"],
                "options": {
                    "-P": "PMatTag",
                    "-T": "TMatTag",
                    "-My": "MyMatTag",
                    "-Mz": "MzMatTag",
                    "-orient?": "orientVals*9",
                    "-shearDist?": "sDratio",
                    "-doRayleigh?*0": "doRayleigh",
                    "-mass?": "m",
                    "-iter?": ["maxIter", "tol"],
                }
            }

        # TFP (Triple Friction Pendulum)
        rules["TFP"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "R1", "R2", "R3", "R4", "Db1", "Db2", "Db3", "Db4",
                         "d1", "d2", "d3", "d4", "mu1", "mu2", "mu3", "mu4", "h1", "h2", "h3", "h4", "H0", "colLoad"],
            "options": {
                "K?": "K",
            }
        }

        # multipleShearSpring
        rules["multipleShearSpring"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "nSpring"],
            "options": {
                "-mat": "matTag",
                "-lim?": "lim",
                "-orient?": "orientVals*6",
                "-mass?": "mass",
            }
        }

        # KikuchiBearing
        rules["KikuchiBearing"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2"],
            "options": {
                "-shape?*1": "shape",
                "-size*": ["size", "totalRubber?"],
                "-totalHeight?": "totalHeight",
                "-nMSS": "nMSS",
                "-matMSS": "matMSSTag",
                "-limDisp?": "limDisp",
                "-nMNS": "nMNS",
                "-matMNS": "matMNSTag",
                "-lambda?": "lambda",
                "-orient?": [f"vecx*{ndm}",f"vecyp*{ndm}"],
                "-mass?": "m",
                "-noPDInput?*0": "noPDInput",
                "-noTilt?*0": "noTilt",
                "-adjustPDOutput?": ["ci", "cj"],
                "-doBalance?": ["limFo", "limFi", "nIter"],
            }
        }

        # ElastomericX
        rules["ElastomericX"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "Fy", "alpha", "Gr", "Kbulk", "D1", "D2", "ts", "tr", "n"],
            "options": {
                "orient?": "orientVals*6",
                "kc?": "kc",
                "PhiM?": "PhiM",
                "ac?": "ac",
                "sDratio?": "sDratio",
                "m?": "m",
                "cd?": "cd",
                "tc?": "tc",
                "tag1?": "tag1",
                "tag2?": "tag2",
                "tag3?": "tag3",
                "tag4?": "tag4",
            }
        }

        # LeadRubberX
        rules["LeadRubberX"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "Fy", "alpha", "Gr", "Kbulk", "D1", "D2", "ts", "tr", "n"],
            "options": {
                "orient?": "orientVals*6",
                "kc?": "kc",
                "PhiM?": "PhiM",
                "ac?": "ac",
                "sDratio?": "sDratio",
                "m?": "m",
                "cd?": "cd",
                "tc?": "tc",
                "qL?": "qL",
                "cL?": "cL",
                "kS?": "kS",
                "aS?": "aS",
                "tag1?": "tag1",
                "tag2?": "tag2",
                "tag3?": "tag3",
                "tag4?": "tag4",
                "tag5?": "tag5"
            }
        }

        # HDR
        rules["HDR"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "Gr", "Kbulk", "D1", "D2", "ts", "tr", "n",
                          "a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3", "c4"],
            "options": {
                "orient?": "orientVals*6",
                "kc?": "kc",
                "PhiM?": "PhiM",
                "ac?": "ac",
                "sDratio?": "sDratio",
                "m?": "m",
                "tc?": "tc"
            }
        }

        # RJWatsonEqsBearing
        if ndm == 2:
            rules["RJWatsonEqsBearing"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2", "frnMdlTag", "kInit"],
                "options": {
                    "-P": "PMatTag",
                    "-Vy": "VyMatTag",
                    "-Mz": "MzMatTag",
                    "-orient?": "orientVals*6",
                    "-shearDist?": "sDratio",
                    "-doRayleigh?*0": "doRayleigh",
                    "-mass?": "m",
                    "-iter?": ["maxIter", "tol"],
                }
            }
        elif ndm == 3:
            rules["RJWatsonEqsBearing"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2", "frnMdlTag", "kInit"],
                "options": {
                    "-P": "PMatTag",
                    "-Vy": "VyMatTag",
                    "-Vz": "VzMatTag",
                    "-T": "TMatTag",
                    "-My": "MyMatTag",
                    "-Mz": "MzMatTag",
                    "-orient?": "orientVals*9",
                    "-shearDist?": "sDratio",
                    "-doRayleigh?*0": "doRayleigh",
                    "-mass?": "m",
                    "-iter?": ["maxIter", "tol"],
                }
            }

        # FPBearingPTV
        rules["FPBearingPTV"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "MuRef", "IsPressureDependent", "pRef",
                         "IsTemperatureDependent", "Diffusivity", "Conductivity", "IsVelocityDependent",
                         "rateParameter", "ReffectiveFP", "Radius_Contact", "kInitial", "theMaterialA",
                         "theMaterialB", "theMaterialC", "theMaterialD", "x1", "x2", "x3", "y1", "y2", "y3",
                         "shearDist", "doRayleigh", "mass", "iter", "tol", "unit"]
        }

        # 添加 YamamotoBiaxialHDR 规则
        rules["YamamotoBiaxialHDR"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "Tp", "DDo", "DDi", "Hr"],
            "options": {
                "-coRS?": ["cr", "cs"],
                "-orient?": "orientVals*6",
                "-mass?": "m",
            }
        }

        # 添加 TripleFrictionPendulum
        rules["TripleFrictionPendulum"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "frnTag1", "frnTag2", "frnTag3", "vertMatTag",
                          "rotZMatTag", "rotXMatTag", "rotYMatTag", "L1", "L2", "L3", "d1", "d2", "d3", "W",
                          "uy", "kvt", "minFv", "tol"]
        }

        return {"element": rules}

    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return [
            "elastomericBearingPlasticity", "elastomericBearingBoucWen", "flatSliderBearing",
            "singleFPBearing", "TFP", "multipleShearSpring", "KikuchiBearing", "YamamotoBiaxialHDR",
            "ElastomericX", "LeadRubberX", "HDR", "RJWatsonEqsBearing", "FPBearingPTV", "TripleFrictionPendulum"
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "elastomericBearingPlasticity": self._handle_elastomericBearingPlasticity,
            "elastomericBearingBoucWen": self._handle_elastomericBearingBoucWen,
            "flatSliderBearing": self._handle_flatSliderBearing,
            "singleFPBearing": self._handle_singleFPBearing,
            "TFP": self._handle_TFP,
            "multipleShearSpring": self._handle_multipleShearSpring,
            "KikuchiBearing": self._handle_KikuchiBearing,
            "YamamotoBiaxialHDR": self._handle_YamamotoBiaxialHDR,
            "ElastomericX": self._handle_ElastomericX,
            "LeadRubberX": self._handle_LeadRubberX,
            "HDR": self._handle_HDR,
            "RJWatsonEqsBearing": self._handle_RJWatsonEqsBearing,
            "FPBearingPTV": self._handle_FPBearingPTV,
            "TripleFrictionPendulum": self._handle_TripleFrictionPendulum,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_elastomericBearingPlasticity(self, *args, **kwargs) -> dict[str, Any]:
        """处理elastomericBearingPlasticity支座元素"""
        arg_map = self._parse("element", *args, **kwargs)
        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "kInit": arg_map.get("kInit"),
            "qd": arg_map.get("qd"),
            "alpha1": arg_map.get("alpha1"),
            "alpha2": arg_map.get("alpha2"),
            "mu": arg_map.get("mu"),
            "PMatTag": arg_map.get("PMatTag"),
            "MzMatTag": arg_map.get("MzMatTag"),
        }

        # 处理3D情况下的额外参数
        if ops.getNDM()[0] == 3:
            eleinfo["TMatTag"] = arg_map.get("TMatTag")
            eleinfo["MyMatTag"] = arg_map.get("MyMatTag")

        # 处理可选参数
        if "orientVals" in arg_map:
            eleinfo["orientVals"] = arg_map.get("orientVals")

        if "sDratio" in arg_map:
            eleinfo["sDratio"] = arg_map.get("sDratio")

        if "doRayleigh" in arg_map:
            eleinfo["doRayleigh"] = True

        if "m" in arg_map:
            eleinfo["m"] = arg_map.get("m")

        self.elements[eleTag] = eleinfo
        return eleinfo

    def _handle_elastomericBearingBoucWen(self, *args, **kwargs) -> dict[str, Any]:
        """处理elastomericBearingBoucWen支座元素"""
        arg_map = self._parse("element", *args, **kwargs)
        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "kInit": arg_map.get("kInit"),
            "qd": arg_map.get("qd"),
            "alpha1": arg_map.get("alpha1"),
            "alpha2": arg_map.get("alpha2"),
            "mu": arg_map.get("mu"),
            "eta": arg_map.get("eta"),
            "beta": arg_map.get("beta"),
            "gamma": arg_map.get("gamma"),
            "PMatTag": arg_map.get("PMatTag"),
            "MzMatTag": arg_map.get("MzMatTag"),
        }

        # 处理3D情况下的额外参数
        if ops.getNDM()[0] == 3:
            eleinfo["TMatTag"] = arg_map.get("TMatTag")
            eleinfo["MyMatTag"] = arg_map.get("MyMatTag")

        # 处理可选参数
        if "orientVals" in arg_map:
            eleinfo["orientVals"] = arg_map.get("orientVals")

        if "sDratio" in arg_map:
            eleinfo["sDratio"] = arg_map.get("sDratio")

        if "doRayleigh" in arg_map:
            eleinfo["doRayleigh"] = True

        if "m" in arg_map:
            eleinfo["m"] = arg_map.get("m")

        self.elements[eleTag] = eleinfo
        return eleinfo

    def _handle_flatSliderBearing(self, *args, **kwargs) -> dict[str, Any]:
        """处理flatSliderBearing支座元素"""
        arg_map = self._parse("element", *args, **kwargs)
        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "frnMdlTag": arg_map.get("frnMdlTag"),
            "kInit": arg_map.get("kInit"),
            "PMatTag": arg_map.get("PMatTag"),
            "MzMatTag": arg_map.get("MzMatTag"),
        }

        # 处理3D情况下的额外参数
        if ops.getNDM()[0] == 3:
            eleinfo["TMatTag"] = arg_map.get("TMatTag")
            eleinfo["MyMatTag"] = arg_map.get("MyMatTag")

        # 处理可选参数
        if "orientVals" in arg_map:
            eleinfo["orientVals"] = arg_map.get("orientVals")

        if "sDratio" in arg_map:
            eleinfo["sDratio"] = arg_map.get("sDratio")

        if "doRayleigh" in arg_map:
            eleinfo["doRayleigh"] = True

        if "m" in arg_map:
            eleinfo["m"] = arg_map.get("m")

        if "maxIter" in arg_map:
            eleinfo["maxIter"] = arg_map.get("maxIter")
            eleinfo["tol"] = arg_map.get("tol")

        self.elements[eleTag] = eleinfo
        return eleinfo

    def _handle_singleFPBearing(self, *args, **kwargs) -> dict[str, Any]:
        """处理singleFPBearing支座元素"""
        arg_map = self._parse("element", *args, **kwargs)
        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "frnMdlTag": arg_map.get("frnMdlTag"),
            "Reff": arg_map.get("Reff"),
            "kInit": arg_map.get("kInit"),
            "PMatTag": arg_map.get("PMatTag"),
            "MzMatTag": arg_map.get("MzMatTag"),
        }

        # 处理3D情况下的额外参数
        if ops.getNDM()[0] == 3:
            eleinfo["TMatTag"] = arg_map.get("TMatTag")
            eleinfo["MyMatTag"] = arg_map.get("MyMatTag")

        # 处理可选参数
        if "orientVals" in arg_map:
            eleinfo["orientVals"] = arg_map.get("orientVals")

        if "sDratio" in arg_map:
            eleinfo["sDratio"] = arg_map.get("sDratio")

        if "doRayleigh" in arg_map:
            eleinfo["doRayleigh"] = True

        if "m" in arg_map:
            eleinfo["m"] = arg_map.get("m")

        if "maxIter" in arg_map:
            eleinfo["maxIter"] = arg_map.get("maxIter")
            eleinfo["tol"] = arg_map.get("tol")

        self.elements[eleTag] = eleinfo
        return eleinfo

    def _handle_TFP(self, *args, **kwargs) -> dict[str, Any]:
        """处理Triple Friction Pendulum (TFP)支座元素"""
        arg_map = self._parse("element", *args, **kwargs)
        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "R1": arg_map.get("R1"),
            "R2": arg_map.get("R2"),
            "R3": arg_map.get("R3"),
            "R4": arg_map.get("R4"),
            "Db1": arg_map.get("Db1"),
            "Db2": arg_map.get("Db2"),
            "Db3": arg_map.get("Db3"),
            "Db4": arg_map.get("Db4"),
            "d1": arg_map.get("d1"),
            "d2": arg_map.get("d2"),
            "d3": arg_map.get("d3"),
            "d4": arg_map.get("d4"),
            "mu1": arg_map.get("mu1"),
            "mu2": arg_map.get("mu2"),
            "mu3": arg_map.get("mu3"),
            "mu4": arg_map.get("mu4"),
            "h1": arg_map.get("h1"),
            "h2": arg_map.get("h2"),
            "h3": arg_map.get("h3"),
            "h4": arg_map.get("h4"),
            "H0": arg_map.get("H0"),
            "colLoad": arg_map.get("colLoad"),
        }

        # 处理可选参数
        if "K" in arg_map:
            eleinfo["K"] = arg_map.get("K")

        self.elements[eleTag] = eleinfo
        return eleinfo

    def _handle_multipleShearSpring(self, *args, **kwargs) -> dict[str, Any]:
        """处理multipleShearSpring支座元素"""
        arg_map = self._parse("element", *args, **kwargs)
        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "nSpring": arg_map.get("nSpring"),
            "matTag": arg_map.get("matTag"),
        }

        # 处理可选参数
        if "lim" in arg_map:
            eleinfo["lim"] = arg_map.get("lim")

        if "orientVals" in arg_map:
            eleinfo["orientVals"] = arg_map.get("orientVals")

        if "mass" in arg_map:
            eleinfo["mass"] = arg_map.get("mass")

        self.elements[eleTag] = eleinfo
        return eleinfo

    def _handle_KikuchiBearing(self, *args, **kwargs) -> dict[str, Any]:
        """处理KikuchiBearing支座元素"""
        arg_map = self._parse("element", *args, **kwargs)
        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "size": arg_map.get("size"),
            "totalRubber": arg_map.get("totalRubber"),
            "nMSS": arg_map.get("nMSS"),
            "matMSSTag": arg_map.get("matMSSTag"),
            "nMNS": arg_map.get("nMNS"),
            "matMNSTag": arg_map.get("matMNSTag"),
        }

        # 处理可选参数
        if "-shape" in args:
            eleinfo["shape"] = args[args.index("-shape")+1]

        if "totalHeight" in arg_map:
            eleinfo["totalHeight"] = arg_map.get("totalHeight")

        if "limDisp" in arg_map:
            eleinfo["limDisp"] = arg_map.get("limDisp")

        if "lambda" in arg_map:
            eleinfo["lambda"] = arg_map.get("lambda")

        if "vecx" in arg_map:
            eleinfo["vecx"] = arg_map.get("vecx")

        if "vecyp" in arg_map:
            eleinfo["vecyp"] = arg_map.get("vecyp")

        if "m" in arg_map:
            eleinfo["m"] = arg_map.get("m")

        if "noPDInput" in arg_map:
            eleinfo["noPDInput"] = True

        if "noTilt" in arg_map:
            eleinfo["noTilt"] = True

        if "ci" in arg_map:
            eleinfo["ci"] = arg_map.get("ci",0.5)
            eleinfo["cj"] = arg_map.get("cj",0.5)

        if "limFo" in arg_map:
            eleinfo["limFo"] = arg_map.get("limFo")
            eleinfo["limFi"] = arg_map.get("limFi")
            eleinfo["nIter"] = arg_map.get("nIter")

        self.elements[eleTag] = eleinfo
        return eleinfo

    def _handle_YamamotoBiaxialHDR(self, *args, **kwargs) -> dict[str, Any]:
        """处理YamamotoBiaxialHDR支座元素"""
        arg_map = self._parse("element", *args, **kwargs)
        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "Tp": arg_map.get("Tp"),
            "DDo": arg_map.get("DDo"),
            "DDi": arg_map.get("DDi"),
            "Hr": arg_map.get("Hr"),
        }

        # 处理可选参数
        if "cr" in arg_map:
            eleinfo["cr"] = arg_map.get("cr")
            eleinfo["cs"] = arg_map.get("cs")

        if "orientVals" in arg_map:
            eleinfo["orientVals"] = arg_map.get("orientVals")

        if "m" in arg_map:
            eleinfo["m"] = arg_map.get("m")

        self.elements[eleTag] = eleinfo
        return eleinfo

    def _handle_ElastomericX(self, *args, **kwargs) -> dict[str, Any]:
        """处理ElastomericX支座元素"""
        arg_map = self._parse("element", *args, **kwargs)
        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "Fy": arg_map.get("Fy"),
            "alpha": arg_map.get("alpha"),
            "Gr": arg_map.get("Gr"),
            "Kbulk": arg_map.get("Kbulk"),
            "D1": arg_map.get("D1"),
            "D2": arg_map.get("D2"),
            "ts": arg_map.get("ts"),
            "tr": arg_map.get("tr"),
            "n": arg_map.get("n"),
        }

        # 处理可选参数
        optional_params = ["orientVals", "kc", "PhiM", "ac", "sDratio", "m", "cd", "tc",
                         "tag1", "tag2", "tag3", "tag4"]

        for param in optional_params:
            if arg_map.get(param, None) is not None:
                eleinfo[param] = arg_map.get(param)

        self.elements[eleTag] = eleinfo
        return eleinfo

    def _handle_LeadRubberX(self, *args, **kwargs) -> dict[str, Any]:
        """处理LeadRubberX支座元素"""
        arg_map = self._parse("element", *args, **kwargs)
        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "Fy": arg_map.get("Fy"),
            "alpha": arg_map.get("alpha"),
            "Gr": arg_map.get("Gr"),
            "Kbulk": arg_map.get("Kbulk"),
            "D1": arg_map.get("D1"),
            "D2": arg_map.get("D2"),
            "ts": arg_map.get("ts"),
            "tr": arg_map.get("tr"),
            "n": arg_map.get("n"),
        }

        # 处理可选参数
        optional_params = ["orientVals", "kc", "PhiM", "ac", "sDratio", "m", "cd", "tc",
                         "qL", "cL", "kS", "aS", "tag1", "tag2", "tag3", "tag4", "tag5"]

        for param in optional_params:
            if arg_map.get(param, None) is not None:
                eleinfo[param] = arg_map.get(param)

        self.elements[eleTag] = eleinfo
        return eleinfo

    def _handle_HDR(self, *args, **kwargs) -> dict[str, Any]:
        """处理HDR支座元素"""
        arg_map = self._parse("element", *args, **kwargs)
        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "Gr": arg_map.get("Gr"),
            "Kbulk": arg_map.get("Kbulk"),
            "D1": arg_map.get("D1"),
            "D2": arg_map.get("D2"),
            "ts": arg_map.get("ts"),
            "tr": arg_map.get("tr"),
            "n": arg_map.get("n"),
            "a1": arg_map.get("a1"),
            "a2": arg_map.get("a2"),
            "a3": arg_map.get("a3"),
            "b1": arg_map.get("b1"),
            "b2": arg_map.get("b2"),
            "b3": arg_map.get("b3"),
            "c1": arg_map.get("c1"),
            "c2": arg_map.get("c2"),
            "c3": arg_map.get("c3"),
            "c4": arg_map.get("c4"),
        }

        # 处理可选参数
        optional_params = ["orientVals", "kc", "PhiM", "ac", "sDratio", "m", "tc"]

        for param in optional_params:
            if arg_map.get(param, None) is not None:
                eleinfo[param] = arg_map.get(param)

        self.elements[eleTag] = eleinfo
        return eleinfo

    def _handle_RJWatsonEqsBearing(self, *args, **kwargs) -> dict[str, Any]:
        """处理RJWatsonEqsBearing支座元素"""
        arg_map = self._parse("element", *args, **kwargs)
        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "frnMdlTag": arg_map.get("frnMdlTag"),
            "kInit": arg_map.get("kInit"),
            "PMatTag": arg_map.get("PMatTag"),
            "VyMatTag": arg_map.get("VyMatTag"),
            "MzMatTag": arg_map.get("MzMatTag"),
        }

        # 处理3D情况下的额外参数
        if ops.getNDM()[0] == 3:
            eleinfo["VzMatTag"] = arg_map.get("VzMatTag")
            eleinfo["TMatTag"] = arg_map.get("TMatTag")
            eleinfo["MyMatTag"] = arg_map.get("MyMatTag")

        # 处理可选参数
        if "orientVals" in arg_map:
            eleinfo["orientVals"] = arg_map.get("orientVals")

        if "sDratio" in arg_map:
            eleinfo["sDratio"] = arg_map.get("sDratio")

        if "doRayleigh" in arg_map:
            eleinfo["doRayleigh"] = True

        if "m" in arg_map:
            eleinfo["m"] = arg_map.get("m")

        if "maxIter" in arg_map:
            eleinfo["maxIter"] = arg_map.get("maxIter")
            eleinfo["tol"] = arg_map.get("tol")

        self.elements[eleTag] = eleinfo
        return eleinfo

    def _handle_FPBearingPTV(self, *args, **kwargs) -> dict[str, Any]:
        """处理FPBearingPTV支座元素"""
        arg_map = self._parse("element", *args, **kwargs)
        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "MuRef": arg_map.get("MuRef"),
            "IsPressureDependent": arg_map.get("IsPressureDependent"),
            "pRef": arg_map.get("pRef"),
            "IsTemperatureDependent": arg_map.get("IsTemperatureDependent"),
            "Diffusivity": arg_map.get("Diffusivity"),
            "Conductivity": arg_map.get("Conductivity"),
            "IsVelocityDependent": arg_map.get("IsVelocityDependent"),
            "rateParameter": arg_map.get("rateParameter"),
            "ReffectiveFP": arg_map.get("ReffectiveFP"),
            "Radius_Contact": arg_map.get("Radius_Contact"),
            "kInitial": arg_map.get("kInitial"),
            "theMaterialA": arg_map.get("theMaterialA"),
            "theMaterialB": arg_map.get("theMaterialB"),
            "theMaterialC": arg_map.get("theMaterialC"),
            "theMaterialD": arg_map.get("theMaterialD"),
            "x1": arg_map.get("x1"),
            "x2": arg_map.get("x2"),
            "x3": arg_map.get("x3"),
            "y1": arg_map.get("y1"),
            "y2": arg_map.get("y2"),
            "y3": arg_map.get("y3"),
            "shearDist": arg_map.get("shearDist"),
            "doRayleigh": arg_map.get("doRayleigh"),
            "mass": arg_map.get("mass"),
            "iter": arg_map.get("iter"),
            "tol": arg_map.get("tol"),
            "unit": arg_map.get("unit"),
        }

        self.elements[eleTag] = eleinfo
        return eleinfo

    def _handle_TripleFrictionPendulum(self, *args, **kwargs) -> dict[str, Any]:
        """处理TripleFrictionPendulum支座元素"""
        arg_map = self._parse("element", *args, **kwargs)
        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "frnTag1": arg_map.get("frnTag1"),
            "frnTag2": arg_map.get("frnTag2"),
            "frnTag3": arg_map.get("frnTag3"),
            "vertMatTag": arg_map.get("vertMatTag"),
            "rotZMatTag": arg_map.get("rotZMatTag"),
            "rotXMatTag": arg_map.get("rotXMatTag"),
            "rotYMatTag": arg_map.get("rotYMatTag"),
            "L1": arg_map.get("L1"),
            "L2": arg_map.get("L2"),
            "L3": arg_map.get("L3"),
            "d1": arg_map.get("d1"),
            "d2": arg_map.get("d2"),
            "d3": arg_map.get("d3"),
            "W": arg_map.get("W"),
            "uy": arg_map.get("uy"),
            "kvt": arg_map.get("kvt"),
            "minFv": arg_map.get("minFv"),
            "tol": arg_map.get("tol"),
        }

        self.elements[eleTag] = eleinfo
        return eleinfo

    def _unknown(self, *args, **kwargs):
        # 此函数不应直接使用，而应使用ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()
