from collections import defaultdict
from copy import deepcopy
from typing import Any, Literal, Optional

from ._BaseHandler import BaseHandler
from ._Materials import (
    ConcreteHandler,
    ConcreteWallsHandler,
    ContactMaterialsHandler,
    InitialStateHandler,
    OtherUniaxialHandler,
    PyTzQzHandler,
    StandardModelsHandler,
    StandardUniaxialHandler,
    SteelReinforcingHandler,
    TsinghuaSandModelsHandler,
    UCSDSaturatedSoilHandler,
    UCSDSoilModelsHandler,
)


class MaterialManager(BaseHandler):
    def __init__(self):
        # 统一数据仓库
        self.materials: dict[int, dict] = {}

        # 构建 “命令 -> {matType -> handler}” 映射
        self._command2typehandler: dict[str, dict[str, BaseHandler]] = defaultdict(dict)
        handler_classes = [
            StandardModelsHandler,
            StandardUniaxialHandler,
            TsinghuaSandModelsHandler,
            ConcreteWallsHandler,
            ConcreteHandler,
            ContactMaterialsHandler,
            InitialStateHandler,
            UCSDSoilModelsHandler,
            UCSDSaturatedSoilHandler,
            OtherUniaxialHandler,
            PyTzQzHandler,
            SteelReinforcingHandler,
        ]
        for cls in handler_classes:
            cmd = cls.handles()[0]
            for typ in cls.types():
                self._command2typehandler[cmd][typ] = cls(self._command2typehandler[cmd], self.materials)

    @property
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        """聚合各子 Handler 的 rule"""
        merged: defaultdict[str, dict[str, Any]] = defaultdict(lambda: defaultdict(lambda: deepcopy({"positional": ["matType", "matTag", "args*"]})))
        for t2h in self._command2typehandler.values():
            for h in set(t2h.values()):
                for k, v in h._COMMAND_RULES.items():
                    merged[k].update(v)
        return merged

    @staticmethod
    def handles():
        return ["uniaxialMaterial", "nDMaterial"]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        matType = arg_map["args"][0]
        registry = self._command2typehandler.get(func_name, {})
        handler = registry.get(matType)
        if handler:
            handler.handle(func_name, arg_map)
        else:
            self.handle_unknown_material(func_name, *arg_map["args"], **arg_map["kwargs"])

    def handle_unknown_material(self, func_name: str, *args, **kwargs):
        """Handle unknown material types"""
        arg_map = self._parse(func_name, *args, **kwargs)

        matTag = int(arg_map.get("matTag"))
        matType = arg_map.get("matType")
        args = arg_map.get("args", [])
        matinfo = {
            "matType": matType,
            "matTag": matTag,
            "args": args,
            "materialType": func_name  # uniaxialMaterial 或 nDMaterial
        }
        self.materials[matTag] = matinfo

    def get_material(self, matTag: int) -> Optional[dict]:
        """Get material information by tag"""
        return self.materials.get(matTag)

    @property
    def nDMaterial_list(self):
        return self._command2typehandler["nDMaterial"].keys()
    
    @property
    def uniaxialMaterial_list(self):
        return self._command2typehandler["uniaxialMaterial"].keys()
    
    def get_material(self, matTag:int) -> dict:
        return self.materials.get(matTag, None)

    def get_materials_by_type(self, matType: str) -> list[int]:
        """Get all materials of the specified type"""
        return {tag:data for tag, data in self.materials.items() if data.get("matType", "").lower() == matType.lower()}

    @property
    def nDMaterial(self) -> dict[int,dict]:
        """Get all nDMaterial"""
        return {tag:data for tag, data in self.materials.items() if data.get("matType", "") in self.nDMaterial_list}
    
    @property
    def uniaxialMaterial(self) -> dict[int,dict]:
        """Get all uniaxialMaterial"""
        return {tag:data for tag, data in self.materials.items() if data.get("matType", "") in self.uniaxialMaterial_list}

    def clear(self):
        self.materials.clear()
        