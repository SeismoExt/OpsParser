from typing import Any

import openseespy.opensees as ops

from .._BaseHandler import SubBaseHandler


class BeamColumnHandler(SubBaseHandler):
    def __init__(self, registry: dict[str, dict], element_store: dict[int, dict]):
        """
        registry: eleType → handler  的全局映射 (供 manager 生成)
        element_store: ElementManager.elements 共享引用
        """
        self.elements = element_store
        self._register(registry)

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        rules = {"alternative": True}

        # ndm for 2D/3D if needed
        ndm = ops.getNDM()[0]
        assert len(ops.getNDM()) == 1, f"Invalid length of ndm, expected 1, got {len(ops.getNDM()) =}"  # noqa: S101

        # 添加不同元素类型的规则
        if ndm == 2:
            rules["elasticBeamColumn"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2", "secTag", "transfTag"],
                "options": {
                    "-mass?": "mass",
                    "-cMass?*0": "cMass",
                    "-release?": "releaseCode",
                }
            }
        elif ndm == 3:
            rules["elasticBeamColumn"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2","secTag", "transfTag"],
                "options": {
                    "-mass?": "mass",
                    "-cMass?*0": "cMass",
                    "-releasez?": "releaseCodeZ",
                    "-releasey?": "releaseCodeY",
                }
            }
        else:
            raise NotImplementedError(f"Invalid {ndm =} for `elasticBeamColumn`")

        rules["ModElasticBeam2d"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "Area", "E_mod", "Iz", "K11", "K33", "K44", "transfTag"],
            "options": {
                "-mass?": "massDens",
                "-cMass?*0": "cMass",
            }
        }

        if ndm == 2:
            rules["ElasticTimoshenkoBeam"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2", "E_mod", "G_mod", "Area", "Iz", "Avy", "transfTag"],
                "options": {
                    "-mass?": "massDens",
                    "-cMass?*0": "cMass",
                }
            }
        elif ndm == 3:
            rules["ElasticTimoshenkoBeam"] = {
                "positional": ["eleType", "eleTag", "eleNodes*2", "E_mod", "G_mod", "Area", "Jxx", "Iy", "Iz", "Avy", "Avz", "transfTag"],
                "options": {
                    "-mass?": "massDens",
                    "-cMass?*0": "cMass",
                }
            }
        else:
            raise NotImplementedError(f"Invalid {ndm =} for `ElasticTimoshenkoBeam`")

        rules["dispBeamColumn"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "transfTag", "integrationTag"],
            "options": {
                "-cMass?*0": "cMass",
                "-mass?": "mass",
            }
        }

        rules["forceBeamColumn"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "transfTag", "integrationTag"],
            "options": {
                "-iter?": ["maxIter", "tol"],
                "-mass?": "mass",
            }
        }

        rules["nonlinearBeamColumn"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "numIntgrPts", "secTag", "transfTag"],
            "options": {
                "-iter?": ["maxIter", "tol"],
                "-mass?": "mass",
                "-integration?*1": "intType",
            }
        }

        rules["dispBeamColumnInt"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "numIntgrPts", "secTag", "transfTag", "cRot"],
            "options": {
                "-mass?": "massDens",
            }
        }

        rules["MVLEM"] = {
            "positional": ["eleType", "eleTag", "Dens", "eleNodes*2", "m", "c"],
            "options": {
                "-thick?": "thick*",
                "-width?": "widths*",
                "-rho?": "rho*",
                "-matConcrete?": "matConcreteTags*",
                "-matSteel?": "matSteelTags*",
                "-matShear?": "matShearTag",
            }
        }

        rules["SFI_MVLEM"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "m", "c"],
            "options": {
                "-thick?": "thick*",
                "-width?": "widths*",
                "-mat?": "mat_tags*",
            }
        }
        rules["Pipe"] = {
            "positional": ["eleType", "eleTag", "eleNodes*2", "pipeMatTag", "pipeSecTag", "xC?", "yC?", "zC?"],
            "options": {
                "-Ti?*0": "Ti",
                "-T0?": "T0",
                "-p?": "p",
                "-tolWall?*0": "tolWall",
                "-noThermalLoad?*0": "noThermalLoad",
                "-noPressureLoad?*0": "noPressureLoad",
            }
        }

        return {"element": rules}

    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return [
            "elasticBeamColumn", "ModElasticBeam2d", "ElasticTimoshenkoBeam",
            "dispBeamColumn", "forceBeamColumn", "nonlinearBeamColumn",
            "dispBeamColumnInt", "MVLEM", "SFI_MVLEM", "Pipe",
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "elasticBeamColumn": self._handle_elasticBeamColumn,
            "ModElasticBeam2d": self._handle_ModElasticBeam2d,
            "ElasticTimoshenkoBeam": self._handle_ElasticTimoshenkoBeam,
            "dispBeamColumn": self._handle_dispBeamColumn,
            "forceBeamColumn": self._handle_forceBeamColumn,
            "nonlinearBeamColumn": self._handle_nonlinearBeamColumn,
            "dispBeamColumnInt": self._handle_dispBeamColumnInt,
            "MVLEM": self._handle_MVLEM,
            "SFI_MVLEM": self._handle_SFI_MVLEM,
            "Pipe": self._handle_Pipe,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_elasticBeamColumn(self, *args, **kwargs) -> dict[str, Any]:
        """handle elasticBeamColumn element"""
        # First try to parse with default format: element('elasticBeamColumn', eleTag, *eleNodes, secTag, transfTag, ...)
        arg_map = self._parse("element", *args, **kwargs)
        command_type = 1
        # Check if there are unparsed positional args, if yes, it means we should use the second format
        if len(arg_map.get("args",[])) > 1:
            command_type = 2
            ndm = ops.getNDM()[0]
            if ndm == 2:
                rule = {
                    "positional": ["eleType", "eleTag", "eleNodes*2", "Area", "E_mod", "Iz", "transfTag"],
                    "options": {
                        "-mass?": "massDens",
                        "-cMass?*0": "cMass",
                        "-release?": "releaseCode",
                    }
                }
            elif ndm == 3:
                rule = {
                    "positional": ["eleType", "eleTag", "eleNodes*2", "Area", "E_mod", "G_mod", "Jxx", "Iy", "Iz", "transfTag"],
                    "options": {
                        "-mass?": "massDens",
                        "-cMass?*0": "cMass",
                        "-releasez?": "releaseCodeZ",
                        "-releasey?": "releaseCodeY",
                    }
                }
            # Parse with the rule directly
            arg_map = self._parse_rule_based_command(rule, *args, **kwargs)

        # Get parameters
        eleTag = arg_map.get("eleTag")
        eleinfo = {
                "eleType": arg_map.get("eleType"),
                "eleTag": eleTag,
                "eleNodes": arg_map.get("eleNodes", []),
                "transfTag": arg_map.get("transfTag"),
            }

        if command_type == 1:
            eleinfo["secTag"] = arg_map.get("secTag")
        else:
            if ndm==2:
                eleinfo["Area"] = arg_map.get("Area")
                eleinfo["E_mod"] = arg_map.get("E_mod")
                eleinfo["Iz"] = arg_map.get("Iz")
            elif ndm==3:
                eleinfo["Area"] = arg_map.get("Area")
                eleinfo["E_mod"] = arg_map.get("E_mod")
                eleinfo["G_mod"] = arg_map.get("G_mod")
                eleinfo["Jxx"] = arg_map.get("Jxx")
                eleinfo["Iy"] = arg_map.get("Iy")
                eleinfo["Iz"] = arg_map.get("Iz")

        if 'massDens' in arg_map:
            eleinfo['massDens'] = arg_map.get('massDens',0.0)

        if 'cMass' in arg_map:
            eleinfo['cMass'] = None

        if 'releaseCode' in arg_map:
            eleinfo['releaseCode'] = arg_map.get('releaseCode',0)

        if 'releaseCodeZ' in arg_map:
            eleinfo['releaseCodeZ'] = arg_map.get('releaseCodeZ',0)

        if 'releaseCodeY' in arg_map:
            eleinfo['releaseCodeY'] = arg_map.get('releaseCodeY',0)

        self.elements[eleTag] = eleinfo

    def _handle_ModElasticBeam2d(self, *args, **kwargs) -> dict[str, Any]:
        """Handle ModElasticBeam2d element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "Area": arg_map.get("Area"),
            "E_mod": arg_map.get("E_mod"),
            "Iz": arg_map.get("Iz"),
            "K11": arg_map.get("K11"),
            "K33": arg_map.get("K33"),
            "K44": arg_map.get("K44"),
            "transfTag": arg_map.get("transfTag"),
        }

        # Handle optional parameters
        if 'massDens' in arg_map:
            eleinfo['massDens'] = arg_map.get('massDens',0.0)

        if 'cMass' in arg_map:
            eleinfo['cMass'] = None

        self.elements[eleTag] = eleinfo

    def _handle_ElasticTimoshenkoBeam(self, *args, **kwargs) -> dict[str, Any]:
        """Handle ElasticTimoshenkoBeam element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "E_mod": arg_map.get("E_mod"),
            "G_mod": arg_map.get("G_mod"),
            "Area": arg_map.get("Area"),
            "Iz": arg_map.get("Iz"),
            "Avy": arg_map.get("Avy"),
            "transfTag": arg_map.get("transfTag"),
        }

        # Add 3D specific parameters if present
        ndm = ops.getNDM()[0]
        if ndm == 3:
            eleinfo["Jxx"] = arg_map.get("Jxx")
            eleinfo["Iy"] = arg_map.get("Iy")
            eleinfo["Avz"] = arg_map.get("Avz")

        # Handle optional parameters
        if 'massDens' in arg_map:
            eleinfo['massDens'] = arg_map.get('massDens', 0.0)

        if 'cMass' in arg_map:
            eleinfo['cMass'] = None

        self.elements[eleTag] = eleinfo

    def _handle_dispBeamColumn(self, *args, **kwargs) -> dict[str, Any]:
        """Handle dispBeamColumn element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "transfTag": arg_map.get("transfTag"),
            "integrationTag": arg_map.get("integrationTag"),
        }

        # Handle optional parameters
        if 'cMass' in arg_map:
            eleinfo['cMass'] = None

        if 'mass' in arg_map:
            eleinfo['mass'] = arg_map.get('mass', 0.0)

        self.elements[eleTag] = eleinfo

    def _handle_forceBeamColumn(self, *args, **kwargs) -> dict[str, Any]:
        """Handle forceBeamColumn element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "transfTag": arg_map.get("transfTag"),
            "integrationTag": arg_map.get("integrationTag"),
        }

        # Handle optional parameters
        if 'maxIter' in arg_map:
            eleinfo['maxIter'] = arg_map.get('maxIter', 10)

        if 'tol' in arg_map:
            eleinfo['tol'] = arg_map.get('tol', 1e-12)

        if 'mass' in arg_map:
            eleinfo['mass'] = arg_map.get('mass', 0.0)

        self.elements[eleTag] = eleinfo

    def _handle_nonlinearBeamColumn(self, *args, **kwargs) -> dict[str, Any]:
        """Handle nonlinearBeamColumn element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "numIntgrPts": arg_map.get("numIntgrPts"),
            "secTag": arg_map.get("secTag"),
            "transfTag": arg_map.get("transfTag"),
        }

        # Handle optional parameters
        if 'maxIter' in arg_map:
            eleinfo['maxIter'] = arg_map.get('maxIter', 10)

        if 'tol' in arg_map:
            eleinfo['tol'] = arg_map.get('tol', 1e-12)

        if 'mass' in arg_map:
            eleinfo['mass'] = arg_map.get('mass', 0.0)

        if 'intType' in arg_map:
            # Since intType is a str, extract it manually
            idx = args.index("-integration")
            eleinfo['intType'] = args[idx+1]

        self.elements[eleTag] = eleinfo

    def _handle_dispBeamColumnInt(self, *args, **kwargs) -> dict[str, Any]:
        """Handle dispBeamColumnInt element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "numIntgrPts": arg_map.get("numIntgrPts"),
            "secTag": arg_map.get("secTag"),
            "transfTag": arg_map.get("transfTag"),
            "cRot": arg_map.get("cRot"),
        }

        # Handle optional parameters
        if 'massDens' in arg_map:
            eleinfo['massDens'] = arg_map.get('massDens', 0.0)

        self.elements[eleTag] = eleinfo

    def _handle_MVLEM(self, *args, **kwargs) -> dict[str, Any]:
        """Handle MVLEM element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "Dens": arg_map.get("Dens"),
            "eleNodes": arg_map.get("eleNodes", []),
            "m": arg_map.get("m"),
            "c": arg_map.get("c"),
        }

        # Handle array parameters
        if 'thick' in arg_map:
            eleinfo['thick'] = arg_map.get('thick', [])

        if 'widths' in arg_map:
            eleinfo['widths'] = arg_map.get('widths', [])

        if 'rho' in arg_map:
            eleinfo['rho'] = arg_map.get('rho', [])

        if 'matConcreteTags' in arg_map:
            eleinfo['matConcreteTags'] = arg_map.get('matConcreteTags', [])

        if 'matSteelTags' in arg_map:
            eleinfo['matSteelTags'] = arg_map.get('matSteelTags', [])

        if 'matShearTag' in arg_map:
            eleinfo['matShearTag'] = arg_map.get('matShearTag')

        self.elements[eleTag] = eleinfo

    def _handle_SFI_MVLEM(self, *args, **kwargs) -> dict[str, Any]:
        """Handle SFI_MVLEM element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "m": arg_map.get("m"),
            "c": arg_map.get("c"),
        }

        # Handle array parameters
        if 'thick' in arg_map:
            eleinfo['thick'] = arg_map.get('thick', [])

        if 'widths' in arg_map:
            eleinfo['widths'] = arg_map.get('widths', [])

        if 'mat_tags' in arg_map:
            eleinfo['mat_tags'] = arg_map.get('mat_tags', [])

        self.elements[eleTag] = eleinfo

    def _handle_Pipe(self, *args, **kwargs) -> dict[str, Any]:
        """Handle Pipe element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "pipeMatTag": arg_map.get("pipeMatTag"),
            "pipeSecTag": arg_map.get("pipeSecTag"),
        }

        # Handle curved pipe parameters
        if 'xC' in arg_map:
            eleinfo['xC'] = arg_map.get('xC')
        if 'yC' in arg_map:
            eleinfo['yC'] = arg_map.get('yC')
        if 'zC' in arg_map:
            eleinfo['zC'] = arg_map.get('zC')

        # Handle optional parameters
        if 'Ti' in arg_map:
            eleinfo['Ti'] = None

        if 'T0' in arg_map:
            eleinfo['T0'] = arg_map.get('T0')

        if 'p' in arg_map:
            eleinfo['p'] = arg_map.get('p')

        if 'tolWall' in arg_map:
            eleinfo['tolWall'] = arg_map.get('tolWall')

        if 'noThermalLoad' in arg_map:
            eleinfo['noThermalLoad'] = None

        if 'noPressureLoad' in arg_map:
            eleinfo['noPressureLoad'] = None

        self.elements[eleTag] = eleinfo

    def _unknown(self, *args, **kwargs):
        # should never use this function but use ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()
