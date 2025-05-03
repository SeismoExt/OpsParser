import re
import warnings
from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Union


class BaseHandler(ABC):
    # ---------------------------------------------------------------------
    # Abstract Property - MUST be implemented by subclasses
    # ---------------------------------------------------------------------
    @property
    @abstractmethod
    def _COMMAND_RULES(self) -> dict[str, dict[str, Any]]:
        """
        A set of parsing rules for the most commonly used OpenSeesPy
        commands.  Each entry describes how positional arguments should be mapped
        and what optional *flag*-style arguments exist.  A trailing ``*`` on the
        key name indicates that the value can contain an arbitrary number of
        tokens which will be returned as a :class:`list`.

        Example(OpenSeesPy Commands):
            node(nodeTag, *crds, '-ndf', ndf, '-mass', *mass, '-disp', ...)
            mass(nodeTag, *massValues)
            element(eleType, tag, *eleNodes, *eleArgs)
            uniaxialMaterial(matType, matTag, *matArgs)
            timeSeries(typeName, tag, *args)
            load(tag, *args)

        Example(rule set dict): {
            "node": {
                "positional": ["tag", "coords*"],
                "options": {
                    "-ndf": "ndf",
                    "-mass": "mass*",
                    "-disp": "disp*",
                    "-vel": "vel*",
                    "-accel": "accel*",
                },
            },
            "mass": {
                "positional": ["tag", "mass*"],
            },
            "element": {
                "positional": ["eleType", "tag", "args*"],
            },
            "uniaxialMaterial": {
                "positional": ["matType", "matTag", "args*"],
            },
            "timeSeries": {
                "positional": ["typeName", "tag", "args*"],
            },
            "load": {
                "positional": ["tag", "args*"],
            },
        }
        """
        raise NotImplementedError

    # ---------------------------------------------------------------------
    # Abstract API - MUST be implemented by subclasses
    # ---------------------------------------------------------------------
    @staticmethod
    @abstractmethod
    def handles() -> list[str]:
        """Return a list of function names this handler can process."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def handles() -> list[str]:
        """返回该处理器支持的命令列表(如 element / uniaxialMaterial / nDMaterial)"""
        raise NotImplementedError

    @abstractmethod
    def handle(self, func_name: str, arg_map: dict[str, Any]):
        """Process the function *func_name* using the already parsed *arg_map*."""
        raise NotImplementedError

    @abstractmethod
    def clear(self):
        """Reset internal data maintained by a concrete handler."""
        raise NotImplementedError


    # ------------------------------------------------------------------
    # Generic helpers shared by all handlers
    # ------------------------------------------------------------------
    @staticmethod
    def _extract_args_by_str(lst: list[Any], target_keys: Union[str, list, tuple, set]) -> list[Any]:
        """Return the values *following* any of *target_keys* until the next
        string token is encountered.

        Parameters
        ----------
        lst : list[Any]
            The full argument list.
        target_keys : Union[str, list, tuple, set]
            A single key or an iterable of keys that should be searched for.

        Returns
        -------
        list[Any]
            List of non-string values following any target key until the next string.

        Notes
        -----
        - If lst is None or empty, returns an empty list
        - If target_keys is None, treats it as an empty collection
        - If no target key is found, returns an empty list
        """
        if lst is None or len(lst) == 0:
            return []

        result: list[Any] = []
        found = False

        if target_keys is None:
            target_keys = set()
        elif isinstance(target_keys, str):
            target_keys = {target_keys}
        else:
            try:
                target_keys = set(target_keys)
            except (TypeError, ValueError):
                target_keys = {target_keys}

        for item in lst:
            if found:
                if isinstance(item, str):
                    break
                result.append(item)
            elif not isinstance(item, list) and item in target_keys:
                found = True

        return result

    @staticmethod
    def _parse_rule_based_command(rule: dict[str, Any], *args: Any, **kwargs:Any) -> dict[str, Any]:
        """Parse command arguments according to a specific rule."""
        result: dict[str, Any] = {}
        arg_list: list[Any] = [x for x in list(args) if x != {} and x is not None]

        # Parse positional arguments
        result.update(BaseHandler._parse_positional_args(rule, arg_list))

        # 记录解析选项标志前的args
        orig_args = result.get("args", [])

        # Parse option flags
        option_result = BaseHandler._parse_option_flags(rule, arg_list)
        result.update(option_result)

        # 如果有解析出选项标志, 并且存在args字段, 则清理args中的选项标志及其值
        if option_result and "args" in result and orig_args:
            # 获取所有选项标志
            option_flags = rule.get("options", {}).keys()
            # 清理args中的选项标志及其值
            cleaned_args = []
            skip_count = 0

            for i, item in enumerate(orig_args):
                if skip_count > 0:
                    skip_count -= 1
                    continue

                # 如果当前项是选项标志, 跳过它及其值
                if isinstance(item,str) and item in option_flags:
                    # 获取这个选项后面的值的数量
                    values = BaseHandler._extract_args_by_str(orig_args[i:], item)
                    skip_count = len(values)
                    continue

                cleaned_args.append(item)

            # 更新args字段
            if cleaned_args:
                result["args"] = cleaned_args
            else:
                # 如果清理后args为空, 则移除args字段
                result.pop("args", None)

        # kwargs take precedence over everything parsed from *args*
        result.update(kwargs)
        return result

    @staticmethod
    def get_name_and_count(origin_name: str) -> tuple[str, int]:
        """Get name and count from a name with count suffix."""
        if '*' in origin_name:
            match = re.match(r"(.+?)\*(\d+)$", origin_name)
            if match:
                name, count = match.groups()
                return name.rstrip('?'), int(count)
            elif origin_name.endswith("*"):
                name = origin_name.rstrip('*')
                return name.rstrip('?'), "all"
        return origin_name.rstrip('?'), 1

    @staticmethod
    def _parse_positional_args(rule: dict[str, Any], arg_list: list[Any]) -> dict[str, Any]:
        """Parse positional arguments according to rule."""
        result: dict[str, Any] = {}
        idx = 0
        stop_idx = len(arg_list)
        for name in rule.get("positional", []):
            # 检查是否是带有数字限制的参数模式, 如 name*2
            clean_name, count = BaseHandler.get_name_and_count(name)
            if isinstance(count, int):
                if idx+count > stop_idx:
                    if '?' in name:
                        count = 0
                    else:
                        raise ValueError(f"Invalid ini value for positional argument {name}: {count =} must be less than {stop_idx-idx}")
                result[clean_name] = arg_list[idx] if count == 1 else None if count == 0 else arg_list[idx:idx + count]
                idx += count
            elif isinstance(count,str) and count == "all":
                # Consume tokens until next recognised option flag (if any)
                for flag in rule.get("options", {}):
                    pure_flag = flag.split('*')[0].rstrip('?')
                    if pure_flag in arg_list[idx:]:
                        candidate = arg_list.index(pure_flag, idx)
                        stop_idx = min(stop_idx, candidate)
                result[clean_name] = arg_list[idx:stop_idx]
                idx = stop_idx
            else:
                # Handle unknown count format
                raise ValueError(f"Invalid parameter format for {name}: {count =} must be int or 'all'")

        # Store unconsumed positional tokens under "args"
        if idx < len(arg_list):
            result.setdefault("args", []).extend(arg_list[idx:])

        return result

    @staticmethod
    def _parse_option_flags(rule: dict[str, Any], arg_list: list[Any]) -> dict[str, Any]:
        """Parse option flags according to rule."""
        result: dict[str, Any] = {}

        for flag, name in rule.get("options", {}).items():
            pure_flag = flag.split('*')[0].rstrip('?')
            if pure_flag in arg_list:
                values = BaseHandler._extract_args_by_str(arg_list, pure_flag)
                idx = 0
                stop_idx = len(values)
                if isinstance(name, str):
                    name = [name]

                # 这些参数可能对应多个参数,需要分别处理
                for subname in name:
                    clean_name, count = BaseHandler.get_name_and_count(subname)
                    if isinstance(count, int):
                        if idx+count > stop_idx:
                            if '?' in flag:
                                count = 0
                            else:
                                raise ValueError(f"Invalid ini value for optional argument {subname}: {count =} must be less than {stop_idx-idx}")

                        result[clean_name] = values[idx] if count == 1 else None if count == 0 else values[idx:idx + count]
                        idx += count
                    elif isinstance(count, str) and count == "all":
                        result[clean_name] = values[idx:stop_idx] if stop_idx > idx else values[idx]
                        idx = stop_idx
                    else:
                        # Handle unknown count format
                        raise ValueError(f"Invalid parameter format for {subname}: {count =} must be int or 'all'")

        return result

    # ------------------------------------------------------------------
    # Universal command-line like argument parser
    # ------------------------------------------------------------------
    def _parse(self, func_name: str, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """
        Parse OpenSeesPy command arguments (*args, **kwargs*) into a standardized dictionary.

        Rules:
            1. The command name determines how positional arguments are assigned via :pyattr:`_COMMAND_RULES`.
               Names ending with "*" absorb all remaining arguments as a list.
            2. Flag-style (e.g. '-mass') options are parsed with their associated values, following TCL conventions.
            3. Any explicit **kwargs take precedence over parsed values.

        If the command is not found in :pyattr:`_COMMAND_RULES`, a default parser is used to extract
        flags and positional arguments, aiming for practical compatibility with typical OpenSeesPy usage.

        Returns:
            dict[str, Any]: Parsed argument mapping for the handler.
        """
        kwargs = dict(kwargs or {})  # copy to avoid mutating caller data
        rule = self._COMMAND_RULES.get(func_name)

        # If rule has alternatives, means this command has many alternative rules, so need to check which rule to use
        alternative = rule.get("alternative", False)
        if alternative:
            # if not isinstance(rule, defaultdict):
            #     warnings.warn(f"Rule for command {func_name} is not a defaultdict; unexpected behavior may occur.", UserWarning, stacklevel=2)
            specific_rule = rule[args[0]]   # if not defaultdict and args[0] is not a key, will raise KeyError
            return self._parse_rule_based_command(specific_rule, *args, **kwargs)

        # Otherwise use rule-based parsing directly
        return self._parse_rule_based_command(rule, *args, **kwargs)

    # -----------------------------------------------------------------
    # registration utility
    # -----------------------------------------------------------------
    def _register(self, registry: dict[str, "BaseHandler"]) -> None:
        """
        注册该处理器可处理的类型到注册表中

        Parameters
        ----------
        registry : dict[str, BaseHandler]
            Manager维护的 {类型: 处理器} 映射
        """
        for arg_type in self.types():
            registry[arg_type] = self

class SubBaseHandler(BaseHandler):
    @staticmethod
    @abstractmethod
    def types() -> list[str]:
        """返回该处理器支持的类型列表(如 element命令的eleType 或 material命令的matType)"""
        raise NotImplementedError
