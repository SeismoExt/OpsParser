from typing import Any

import openseespy.opensees as ops

from .._BaseHandler import SubBaseHandler


class BrickHandler(SubBaseHandler):
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

        # Brick elements only work in 3D
        rules["stdBrick"] = {
            "positional": ["eleType", "eleTag", "eleNodes*8", "matTag", "b1?", "b2?", "b3?"],
        }

        rules["bbarBrick"] = {
            "positional": ["eleType", "eleTag", "eleNodes*8", "matTag", "b1?", "b2?", "b3?"],
        }

        rules["20NodeBrick"] = {
            "positional": ["eleType", "eleTag", "eleNodes*20", "matTag", "bf1", "bf2", "bf3", "massDen"],
        }

        rules["SSPbrick"] = {
            "positional": ["eleType", "eleTag", "eleNodes*8", "matTag", "b1?", "b2?", "b3?"],
        }

        return {"element": rules}

    @staticmethod
    def handles() -> list[str]:
        return ["element"]

    @staticmethod
    def types() -> list[str]:
        return [
            "stdBrick", "bbarBrick", "20NodeBrick", "SSPbrick"
        ]

    def handle(self, func_name: str, arg_map: dict[str, Any]):
        args, kwargs = arg_map["args"], arg_map["kwargs"]
        ele_type = args[0]
        dispatch = {
            "stdBrick": self._handle_stdBrick,
            "bbarBrick": self._handle_bbarBrick,
            "20NodeBrick": self._handle_20NodeBrick,
            "SSPbrick": self._handle_SSPbrick,
        }.get(ele_type, self._unknown)
        dispatch(*args, **kwargs)

    def _handle_stdBrick(self, *args, **kwargs) -> dict[str, Any]:
        """Handle Standard Brick Element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "matTag": arg_map.get("matTag"),
        }

        # Handle optional body forces
        if "b1" in arg_map:
            eleinfo["b1"] = arg_map.get("b1", 0.0)
        if "b2" in arg_map:
            eleinfo["b2"] = arg_map.get("b2", 0.0)
        if "b3" in arg_map:
            eleinfo["b3"] = arg_map.get("b3", 0.0)

        self.elements[eleTag] = eleinfo

    def _handle_bbarBrick(self, *args, **kwargs) -> dict[str, Any]:
        """Handle Bbar Brick Element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "matTag": arg_map.get("matTag"),
        }

        # Handle optional body forces
        if "b1" in arg_map:
            eleinfo["b1"] = arg_map.get("b1", 0.0)
        if "b2" in arg_map:
            eleinfo["b2"] = arg_map.get("b2", 0.0)
        if "b3" in arg_map:
            eleinfo["b3"] = arg_map.get("b3", 0.0)

        self.elements[eleTag] = eleinfo

    def _handle_20NodeBrick(self, *args, **kwargs) -> dict[str, Any]:
        """Handle Twenty Node Brick Element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "matTag": arg_map.get("matTag"),
            "bf1": arg_map.get("bf1"),
            "bf2": arg_map.get("bf2"),
            "bf3": arg_map.get("bf3"),
            "massDen": arg_map.get("massDen"),
        }

        self.elements[eleTag] = eleinfo

    def _handle_SSPbrick(self, *args, **kwargs) -> dict[str, Any]:
        """Handle SSPbrick Element"""
        arg_map = self._parse("element", *args, **kwargs)

        eleTag = arg_map.get("eleTag")

        eleinfo = {
            "eleType": arg_map.get("eleType"),
            "eleTag": eleTag,
            "eleNodes": arg_map.get("eleNodes", []),
            "matTag": arg_map.get("matTag"),
        }

        # Handle optional body forces
        if "b1" in arg_map:
            eleinfo["b1"] = arg_map.get("b1", 0.0)
        if "b2" in arg_map:
            eleinfo["b2"] = arg_map.get("b2", 0.0)
        if "b3" in arg_map:
            eleinfo["b3"] = arg_map.get("b3", 0.0)

        self.elements[eleTag] = eleinfo

    def _unknown(self, *args, **kwargs):
        # should never use this function but use ElementManager.handle_unknown_element()
        raise NotImplementedError

    def clear(self):
        self.elements.clear()
