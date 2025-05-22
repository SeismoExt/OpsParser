import enum
from typing import Any, List
import functools
import types
from collections import defaultdict

from ._manager import (
    BaseHandler, ElementManager, LoadManager, MaterialManager, NodeManager, TimeSeriesManager,
    ModelManager, SPConstraintManager, MPConstraintManager, GeomTransfManager, SectionManager
)


class OpenSeesCommand(enum.Enum):
    # Enum members' values are the manager classes themselves.
    # IMPORTANT: NodeManager, ElementManager, etc., MUST be implemented as singletons(DONE by Metaclass)
    NODE = NodeManager
    ELEMENT = ElementManager
    MATERIAL = MaterialManager
    TIMESERIES = TimeSeriesManager
    LOAD = LoadManager
    MODEL = ModelManager
    SPCONSTRAINT = SPConstraintManager
    MPCONSTRAINT = MPConstraintManager
    GEOMTRANSF = GeomTransfManager
    SECTION = SectionManager

    @property
    def instance(self) -> BaseHandler:
        """
        Returns the singleton instance of the manager class.
        Assumes self.value (e.g., NodeManager class) is a singleton,
        so calling it (e.g., NodeManager()) returns its unique instance.
        """
        return self.value()


class OpenSeesParser:
    def __init__(self, module):
        self.module = module
        self.call_log: defaultdict[str, List[Any]] = defaultdict(list)
        self.original_functions: dict[str, Any] = {}

        # self.handler_instances dictionary is no longer needed here.
        # The OpenSeesCommand enum will be the source of truth for handler instances.
        
        self.dispatch_table: dict[str, BaseHandler] = self._build_dispatch_table()

    def _build_dispatch_table(self) -> dict[str, BaseHandler]:
        """Build a dispatch table mapping function names to handlers."""
        dispatch_table: dict[str, BaseHandler] = {}
        for command_enum_member in OpenSeesCommand: # Iterate over OpenSeesCommand enum members
            handler_instance = command_enum_member.instance # Get the singleton instance
            handled_funcs: List[str] = handler_instance.handles()
            for func_name in handled_funcs:
                 if func_name in dispatch_table:
                     # Note: The warning now refers to the class name of the handler instance
                     print(f"Warning: Function '{func_name}' is handled by multiple handlers. Using the last one found: {handler_instance.__class__.__name__}")
                 dispatch_table[func_name] = handler_instance
        return dispatch_table

    def hook_all(self, debug = False):
        for name in dir(self.module):
            attr = getattr(self.module, name)
            if isinstance(attr, (types.FunctionType, types.BuiltinFunctionType)):
                self._hook_function(name, attr, debug)

    def _hook_function(self, name, func, debug = False):
        self.original_functions[name] = func

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            arg_map = {"args": args, "kwargs": kwargs}

            self.call_log[name].append(arg_map)

            # Dispatch to handler
            handler = self.dispatch_table.get(name)
            if handler:
                if debug:
                    print(name, arg_map)
                handler.handle(name, arg_map)

            return func(*args, **kwargs)

        setattr(self.module, name, wrapper)

    def restore_all(self):
        for name, func in self.original_functions.items():
            setattr(self.module, name, func)
        self.original_functions.clear()

    def clear(self):
        self.call_log.clear()
        for command_enum_member in OpenSeesCommand: # Iterate over OpsCommand enum members
            handler_instance = command_enum_member.instance # Get the singleton instance
            handler_instance.clear()


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import openseespy.opensees as ops
    from _manager import NodeManager as Node

    # 假设你已经有下面这些类
    # - OpenSeesParser
    # - NodeManager(BaseHandler)
    # - ElementManager(BaseHandler)
    # ...（参考前文）

    # 创建 spy 并挂钩所有命令
    parser = OpenSeesParser(ops)
    parser.hook_all()

    # 运行 OpenSees 命令
    ops.model("basic", "-ndm", 2, "-ndf", 3)
    ops.node(1, 0.0, 0.0)
    ops.node(2, 1.0, 0.0)
    ops.node(3, 1.0, 1.0)
    ops.node(4, 0.0, 1.0)

    # 提取节点数据
    # Directly get the NodeManager singleton instance
    node_dict = Node.nodes

    # 准备画图数据
    x_coords = []
    y_coords = []
    labels = []

    for tag_node in node_dict:
        # Use the singleton instance to get node coordinates
        coords = Node.get_node_coords(tag_node)
        x_coords.append(coords[0])
        y_coords.append(coords[1])
        labels.append(str(tag_node))

    # 绘图
    plt.figure(figsize=(5, 5))
    plt.scatter(x_coords, y_coords, c="blue", s=60)

    # 添加标签
    for i, txt in enumerate(labels):
        plt.text(x_coords[i] + 0.02, y_coords[i] + 0.02, txt, fontsize=10)

    plt.title("OpenSees Node Layout")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis("equal")
    plt.grid(True)
    plt.show()
