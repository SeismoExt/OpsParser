import functools
import types
from collections import defaultdict
from typing import Any, Iterator, Optional, Union

from ._manager import BaseHandler, ElementManager, LoadManager, MaterialManager, NodeManager, TimeSeriesManager


class HandlerCollection:
    """
    A collection managing handlers, supporting attribute, key, and iteration access.
    Can be accessed via collection.HandlerName, collection['HandlerName'], or for handler in collection.
    """
    def __init__(self):
        self._handlers: dict[str, BaseHandler] = {}

    def add(self, handler: Union[BaseHandler, list[BaseHandler]], name: Optional[Union[str, list[str]]] = None) -> None:
        """Add handler(s) to the collection."""
        if isinstance(handler, list):
            if not name:
                name = [h.__class__.__name__ for h in handler]
            for h,h_name in zip(handler, name):
                self.add(h,h_name)
            return

        handler_name: str = name if name else handler.__class__.__name__
        if handler_name in self._handlers:
            # Can log a warning or raise an error to handle duplicate names if needed
            print(f"Warning: Handler named '{handler_name}' already exists. It will be overwritten.")
        self._handlers[handler_name] = handler

    def __getattr__(self, name: str) -> BaseHandler:
        """Allow accessing handlers using attribute syntax (e.g., collection.Node)."""
        if name in self._handlers:
            return self._handlers[name]
        # Delegate to default attribute access if name starts with underscore or is not a handler name
        if name.startswith('_'):
             raise AttributeError(name)
        try:
            return self._handlers[name]
        except KeyError as e:
            raise AttributeError(name) from e

    def __getitem__(self, key: str) -> BaseHandler:
        """Allow accessing handlers using dictionary key syntax (e.g., collection['Node'])."""
        try:
            return self._handlers[key]
        except KeyError as e:
            raise KeyError(key) from e

    def __iter__(self) -> Iterator[BaseHandler]:
        """Allow iterating over handlers (e.g., for handler in collection:)."""
        return iter(self._handlers.values())

    def __len__(self) -> int:
        """Return the number of handlers in the collection."""
        return len(self._handlers)

    def get_dispatch_table(self) -> dict[str, BaseHandler]:
        """Build a dispatch table mapping function names to handlers."""
        dispatch_table: dict[str, BaseHandler] = {}
        for handler in self: # Iterates over handler instances
            handled_funcs: list[str] = handler.handles() # Assuming handles() returns list[str]
            for func_name in handled_funcs:
                 if func_name in dispatch_table:
                     # Handle potential conflicts where multiple handlers handle the same function
                     print(f"Warning: Function '{func_name}' is handled by multiple handlers. Using the last one found: {handler.__class__.__name__}")
                 dispatch_table[func_name] = handler
        return dispatch_table

class OpenSeesParser:
    def __init__(self, module):
        self.module = module
        self.call_log: defaultdict[str, list] = defaultdict(list)
        self.original_functions: dict[str, Any] = {}

        # Register handlers here
        self.handlers = HandlerCollection()
        self.handlers.add(NodeManager(),"Node")
        self.handlers.add(ElementManager(),"Element")
        self.handlers.add(MaterialManager(),"Material")
        # self.handlers.add(TimeSeriesManager(),"TimeSeries")
        # self.handlers.add(LoadManager(),"Load")

        # Build a dispatch table: func_name -> handler
        self.dispatch_table: dict[str, BaseHandler] = self.handlers.get_dispatch_table()

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
        for handler in self.handlers:
            handler.clear()


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import openseespy.opensees as ops

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
    node_dict = parser.handlers["Node"].nodes

    # 准备画图数据
    x_coords = []
    y_coords = []
    labels = []

    for tag in node_dict:
        coords = parser.handlers["Node"].get_node_coords(tag)
        x_coords.append(coords[0])
        y_coords.append(coords[1])
        labels.append(str(tag))

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
