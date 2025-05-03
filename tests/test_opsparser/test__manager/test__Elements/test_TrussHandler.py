from typing import Any, Optional

import openseespy.opensees as ops
import pytest

from opsparser import ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return ElementManager()


def test_handle_Truss(element_manager: ElementManager) -> None:
    """测试处理标准桁架元素"""
    # 设置测试数据
    cmd = "element"
    args = ("Truss", 1, *[1, 2], 100.0, 301, "-rho", 1.5, "-cMass", 1, "-doRayleigh", 1)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager.elements
    element_data = element_manager.elements[1]
    assert element_data["eleType"] == "Truss"
    assert element_data["eleTag"] == 1
    assert element_data["eleNodes"] == [1, 2]
    assert element_data["A"] == 100.0
    assert element_data["matTag"] == 301
    assert element_data["rho"] == 1.5
    assert element_data["cFlag"] == 1
    assert element_data["rFlag"] == 1


def test_handle_TrussSection(element_manager: ElementManager) -> None:
    """测试处理带有截面的桁架元素"""
    # 设置测试数据
    cmd = "element"
    args = ("TrussSection", 2, *[3, 4], 102, "-rho", 2.0, "-cMass", 0)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 2 in element_manager.elements
    element_data = element_manager.elements[2]
    assert element_data["eleType"] == "TrussSection"
    assert element_data["eleTag"] == 2
    assert element_data["eleNodes"] == [3, 4]
    assert element_data["secTag"] == 102
    assert element_data["rho"] == 2.0
    assert element_data["cFlag"] == 0
    assert element_data["rFlag"] == 0  # 默认值


def test_handle_corotTruss(element_manager: ElementManager) -> None:
    """测试处理协旋转桁架元素"""
    # 设置测试数据
    cmd = "element"
    args = ("corotTruss", 3, *[5, 6], 150.0, 303, "-doRayleigh", 1)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 3 in element_manager.elements
    element_data = element_manager.elements[3]
    assert element_data["eleType"] == "corotTruss"
    assert element_data["eleTag"] == 3
    assert element_data["eleNodes"] == [5, 6]
    assert element_data["A"] == 150.0
    assert element_data["matTag"] == 303
    assert element_data["rho"] == 0.0  # 默认值
    assert element_data["cFlag"] == 0  # 默认值
    assert element_data["rFlag"] == 1


def test_handle_corotTrussSection(element_manager: ElementManager) -> None:
    """测试处理协旋转带有截面的桁架元素"""
    # 设置测试数据
    cmd = "element"
    args = ("corotTrussSection", 4, *[7, 8], 104)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 4 in element_manager.elements
    element_data = element_manager.elements[4]
    assert element_data["eleType"] == "corotTrussSection"
    assert element_data["eleTag"] == 4
    assert element_data["eleNodes"] == [7, 8]
    assert element_data["secTag"] == 104
    assert element_data["rho"] == 0.0  # 默认值
    assert element_data["cFlag"] == 0  # 默认值
    assert element_data["rFlag"] == 0  # 默认值


def test_handle_unknown_truss(element_manager: ElementManager) -> None:
    """测试处理未知桁架元素类型"""
    # 设置测试数据
    cmd = "element"
    args = ("CustomTruss", 5, *[9, 10], 200.0, 305, 0.5)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 5 in element_manager.elements
    element_data = element_manager.elements[5]
    assert element_data["eleType"] == "CustomTruss"
    assert element_data["eleTag"] == 5
    assert "args" in element_data  # 未知元素应该将额外参数保存在args中