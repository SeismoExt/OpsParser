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

def test_handle_zeroLength(element_manager: ElementManager) -> None:
    """Test data handling for zeroLength element"""
    # 3D model case
    cmd = "element"
    args = ("zeroLength", 1, *[1, 20], "-mat", *[911, 923], "-dir", *[1, 5], "-doRayleigh", 0, "-orient", *[0, 0, 1], *[1, 1, 1])
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # Check if the element is correctly stored
    assert 1 in element_manager.elements
    element_data = element_manager.elements[1]
    assert element_data["eleType"] == "zeroLength"
    assert element_data["eleNodes"] == [1, 20]
    assert element_data["matTags"] == [911, 923]
    assert element_data["dirs"] == [1, 5]
    assert element_data["rFlag"] == 0
    assert element_data["vecx"] == [0, 0, 1]
    assert element_data["vecyp"] == [1, 1, 1]

def test_handle_zerolengthND(element_manager: ElementManager) -> None:
    """Test data handling for zeroLengthND element"""
    # Full argument case: includes optional uniTag and orient
    cmd = "element"
    args = ("zeroLengthND", 2, *[3, 4], 100, 200, "-orient", *[1, 0, 0], *[0, 1, 0])
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # Check if the element is correctly stored
    assert 2 in element_manager.elements
    element_data = element_manager.elements[2]
    assert element_data["eleType"] == "zeroLengthND"
    assert element_data["eleTag"] == 2
    assert element_data["eleNodes"] == [3, 4]
    assert element_data["matTag"] == 100
    assert element_data["uniTag"] == 200
    assert element_data["vecx"] == [1, 0, 0]
    assert element_data["vecyp"] == [0, 1, 0]

def test_handle_zeroLengthSection(element_manager: ElementManager) -> None:
    """Test data handling for zeroLengthSection element"""
    # Case with orient and doRayleigh options
    cmd = "element"
    args = ("zeroLengthSection", 10, *[5, 6], 501, "-orient", *[1, 0, 0], *[0, 1, 0], "-doRayleigh", 1)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # Check if the element is correctly stored
    assert 10 in element_manager.elements
    element_data = element_manager.elements[10]
    assert element_data["eleType"] == "zeroLengthSection"
    assert element_data["eleTag"] == 10
    assert element_data["eleNodes"] == [5, 6]
    assert element_data["secTag"] == 501
    assert element_data["vecx"] == [1, 0, 0]
    assert element_data["vecyp"] == [0, 1, 0]
    assert element_data["rFlag"] == 1

def test_handle_CoupledZeroLength(element_manager: ElementManager) -> None:
    """Test data handling for CoupledZeroLength element"""
    cmd = "element"
    args = ("CoupledZeroLength", 11, *[7, 8], 1, 2, 502, 1)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # Check if the element is correctly stored
    assert 11 in element_manager.elements
    element_data = element_manager.elements[11]
    assert element_data["eleType"] == "CoupledZeroLength"
    assert element_data["eleTag"] == 11
    assert element_data["eleNodes"] == [7, 8]
    assert element_data["dirn1"] == 1
    assert element_data["dirn2"] == 2
    assert element_data["matTag"] == 502
    assert element_data["rFlag"] == 1

def test_handle_zeroLengthContact2D(element_manager: ElementManager) -> None:
    """Test data handling for zeroLengthContact2D element"""
    cmd = "element"
    args = ("zeroLengthContact2D", 12, *[9, 10], 1000.0, 500.0, 0.3, "-normal", 1.0, 0.0)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # Check if the element is correctly stored
    assert 12 in element_manager.elements
    element_data = element_manager.elements[12]
    assert element_data["eleType"] == "zeroLengthContact2D"
    assert element_data["eleTag"] == 12
    assert element_data["eleNodes"] == [9, 10]
    assert element_data["Kn"] == 1000.0
    assert element_data["Kt"] == 500.0
    assert element_data["mu"] == 0.3
    assert element_data["Nx"] == 1.0
    assert element_data["Ny"] == 0.0

def test_handle_zeroLengthContact3D(element_manager: ElementManager) -> None:
    """Test data handling for zeroLengthContact3D element"""
    cmd = "element"
    args = ("zeroLengthContact3D", 13, *[11, 12], 1500.0, 700.0, 0.25, 10.0, 3)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # Check if the element is correctly stored
    assert 13 in element_manager.elements
    element_data = element_manager.elements[13]
    assert element_data["eleType"] == "zeroLengthContact3D"
    assert element_data["eleTag"] == 13
    assert element_data["eleNodes"] == [11, 12]
    assert element_data["Kn"] == 1500.0
    assert element_data["Kt"] == 700.0
    assert element_data["mu"] == 0.25
    assert element_data["c"] == 10.0
    assert element_data["dir"] == 3

def test_handle_zeroLengthContactNTS2D(element_manager: ElementManager) -> None:
    """Test data handling for zeroLengthContactNTS2D element"""
    cmd = "element"
    args = ("zeroLengthContactNTS2D", 14, "-sNdNum", 2, "-mNdNum", 2, "-Nodes", *[13, 14, 15, 16], "kn", 2000.0, "kt", 1000.0, "phi", 30.0)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # Check if the element is correctly stored
    assert 14 in element_manager.elements
    element_data = element_manager.elements[14]
    assert element_data["eleType"] == "zeroLengthContactNTS2D"
    assert element_data["eleTag"] == 14
    assert element_data["sNdNum"] == 2
    assert element_data["mNdNum"] == 2
    assert element_data["NodesTags"] == [13, 14, 15, 16]
    assert element_data["kn"] == 2000.0
    assert element_data["kt"] == 1000.0
    assert element_data["phi"] == 30.0

def test_handle_zeroLengthInterface2D(element_manager: ElementManager) -> None:
    """Test data handling for zeroLengthInterface2D element"""
    cmd = "element"
    args = ("zeroLengthInterface2D", 15, "-sNdNum", 2, "-mNdNum", 2, "-dof", 1, 1, "-Nodes", *[17, 18, 19, 20], "kn", 2500.0, "kt", 1200.0, "phi", 35.0)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # Check if the element is correctly stored
    assert 15 in element_manager.elements
    element_data = element_manager.elements[15]
    assert element_data["eleType"] == "zeroLengthInterface2D"
    assert element_data["eleTag"] == 15
    assert element_data["sNdNum"] == 2
    assert element_data["mNdNum"] == 2
    assert element_data["sdof"] == 1
    assert element_data["mdof"] == 1
    assert element_data["NodesTags"] == [17, 18, 19, 20]
    assert element_data["kn"] == 2500.0
    assert element_data["kt"] == 1200.0
    assert element_data["phi"] == 35.0

def test_handle_zeroLengthImpact3D(element_manager: ElementManager) -> None:
    """Test data handling for zeroLengthImpact3D element"""
    cmd = "element"
    args = ("zeroLengthImpact3D", 16, *[21, 22], 1, 0.01, 0.4, 3000.0, 5000.0, 7000.0, 0.05, 50.0)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # Check if the element is correctly stored
    assert 16 in element_manager.elements
    element_data = element_manager.elements[16]
    assert element_data["eleType"] == "zeroLengthImpact3D"
    assert element_data["eleTag"] == 16
    assert element_data["eleNodes"] == [21, 22]
    assert element_data["direction"] == 1
    assert element_data["initGap"] == 0.01
    assert element_data["frictionRatio"] == 0.4
    assert element_data["Kt"] == 3000.0
    assert element_data["Kn"] == 5000.0
    assert element_data["Kn2"] == 7000.0
    assert element_data["Delta_y"] == 0.05
    assert element_data["cohesion"] == 50.0

def test_handle_unknown_zeroLength(element_manager: ElementManager) -> None:
    """Test handling unknown elements"""
    # 设置测试数据
    cmd = "element"
    args = ("customzeroLength", 1, *[1, 2], 100.0, 301, "-rho", 1.5, "-cMass", 1, "-doRayleigh", 1)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager.elements
    element_data = element_manager.elements[1]
    assert element_data["eleType"] == "customzeroLength"
    assert element_data["eleTag"] == 1
    assert "args" in element_data  # 未知元素应该将额外参数保存在args中
