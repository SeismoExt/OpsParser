import openseespy.opensees as ops
import pytest

from opsparser import MaterialManager


@pytest.fixture
def material_manager() -> MaterialManager:
    """每个测试前初始化一个MaterialManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return MaterialManager()


def test_handle_PySimple1(material_manager: MaterialManager) -> None:
    """测试PySimple1材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("PySimple1", 1, 1, 100.0, 0.01, 0.5, 0.1)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 1 in material_manager.materials
    material_data = material_manager.materials[1]
    assert material_data["matType"] == "PySimple1"
    assert material_data["matTag"] == 1
    assert material_data["soilType"] == 1
    assert material_data["pult"] == 100.0
    assert material_data["Y50"] == 0.01
    assert material_data["Cd"] == 0.5
    assert material_data["c"] == 0.1


def test_handle_TzSimple1(material_manager: MaterialManager) -> None:
    """测试TzSimple1材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("TzSimple1", 2, 1, 150.0, 0.02, 0.2)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 2 in material_manager.materials
    material_data = material_manager.materials[2]
    assert material_data["matType"] == "TzSimple1"
    assert material_data["matTag"] == 2
    assert material_data["soilType"] == 1
    assert material_data["tult"] == 150.0
    assert material_data["z50"] == 0.02
    assert material_data["c"] == 0.2


def test_handle_QzSimple1(material_manager: MaterialManager) -> None:
    """测试QzSimple1材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("QzSimple1", 3, 2, 200.0, 0.03, 0.05, 0.15)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 3 in material_manager.materials
    material_data = material_manager.materials[3]
    assert material_data["matType"] == "QzSimple1"
    assert material_data["matTag"] == 3
    assert material_data["qzType"] == 2
    assert material_data["qult"] == 200.0
    assert material_data["Z50"] == 0.03
    assert material_data["suction"] == 0.05
    assert material_data["c"] == 0.15


def test_handle_PyLiq1_with_elements(material_manager: MaterialManager) -> None:
    """测试PyLiq1材料的数据处理（使用元素引用）"""
    cmd = "uniaxialMaterial"
    args = ("PyLiq1", 4, 1, 120.0, 0.015, 0.6, 0.1, 60.0, 10, 11)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 4 in material_manager.materials
    material_data = material_manager.materials[4]
    assert material_data["matType"] == "PyLiq1"
    assert material_data["matTag"] == 4
    assert material_data["soilType"] == 1
    assert material_data["pult"] == 120.0
    assert material_data["Y50"] == 0.015
    assert material_data["Cd"] == 0.6
    assert material_data["c"] == 0.1
    assert material_data["pRes"] == 60.0
    assert material_data["ele1"] == 10
    assert material_data["ele2"] == 11


def test_handle_PyLiq1_with_timeSeries(material_manager: MaterialManager) -> None:
    """测试PyLiq1材料的数据处理（使用时间序列）"""
    cmd = "uniaxialMaterial"
    args = ("PyLiq1", 5, 1, 130.0, 0.016, 0.65, 0.12, 65.0, "-timeSeries", 20)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 5 in material_manager.materials
    material_data = material_manager.materials[5]
    assert material_data["matType"] == "PyLiq1"
    assert material_data["matTag"] == 5
    assert material_data["soilType"] == 1
    assert material_data["pult"] == 130.0
    assert material_data["Y50"] == 0.016
    assert material_data["Cd"] == 0.65
    assert material_data["c"] == 0.12
    assert material_data["pRes"] == 65.0
    assert material_data["timeSeriesTag"] == 20


def test_handle_TzLiq1_with_elements(material_manager: MaterialManager) -> None:
    """测试TzLiq1材料的数据处理（使用元素引用）"""
    cmd = "uniaxialMaterial"
    args = ("TzLiq1", 6, 2, 160.0, 0.025, 0.22, 12, 13)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 6 in material_manager.materials
    material_data = material_manager.materials[6]
    assert material_data["matType"] == "TzLiq1"
    assert material_data["matTag"] == 6
    assert material_data["tzType"] == 2
    assert material_data["tult"] == 160.0
    assert material_data["z50"] == 0.025
    assert material_data["c"] == 0.22
    assert material_data["ele1"] == 12
    assert material_data["ele2"] == 13


def test_handle_TzLiq1_with_timeSeries(material_manager: MaterialManager) -> None:
    """测试TzLiq1材料的数据处理（使用时间序列）"""
    cmd = "uniaxialMaterial"
    args = ("TzLiq1", 7, 2, 170.0, 0.026, 0.23, "-timeSeries", 21)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 7 in material_manager.materials
    material_data = material_manager.materials[7]
    assert material_data["matType"] == "TzLiq1"
    assert material_data["matTag"] == 7
    assert material_data["tzType"] == 2
    assert material_data["tult"] == 170.0
    assert material_data["z50"] == 0.026
    assert material_data["c"] == 0.23
    assert material_data["timeSeriesTag"] == 21


def test_handle_QzLiq1_with_elements(material_manager: MaterialManager) -> None:
    """测试QzLiq1材料的数据处理（使用元素引用）"""
    cmd = "uniaxialMaterial"
    args = ("QzLiq1", 8, 1, 220.0, 0.035, 0.7, 0.18, 0.5, 14, 15)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 8 in material_manager.materials
    material_data = material_manager.materials[8]
    assert material_data["matType"] == "QzLiq1"
    assert material_data["matTag"] == 8
    assert material_data["soilType"] == 1
    assert material_data["qult"] == 220.0
    assert material_data["Z50"] == 0.035
    assert material_data["Cd"] == 0.7
    assert material_data["c"] == 0.18
    assert material_data["alpha"] == 0.5
    assert material_data["ele1"] == 14
    assert material_data["ele2"] == 15


def test_handle_QzLiq1_with_timeSeries(material_manager: MaterialManager) -> None:
    """测试QzLiq1材料的数据处理（使用时间序列）"""
    cmd = "uniaxialMaterial"
    args = ("QzLiq1", 9, 1, 230.0, 0.036, 0.75, 0.19, 0.55, "-timeSeries", 22)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 9 in material_manager.materials
    material_data = material_manager.materials[9]
    assert material_data["matType"] == "QzLiq1"
    assert material_data["matTag"] == 9
    assert material_data["soilType"] == 1
    assert material_data["qult"] == 230.0
    assert material_data["Z50"] == 0.036
    assert material_data["Cd"] == 0.75
    assert material_data["c"] == 0.19
    assert material_data["alpha"] == 0.55
    assert material_data["timeSeriesTag"] == 22


def test_handle_unknown_py_tz_qz_material(material_manager: MaterialManager) -> None:
    """测试处理未知的Py-Tz-Qz材料模型"""
    cmd = "uniaxialMaterial"
    args = ("CustomPyMaterial", 10, 1, 300.0, 0.04)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 10 in material_manager.materials
    material_data = material_manager.materials[10]
    assert material_data["matType"] == "CustomPyMaterial"
    assert material_data["matTag"] == 10
    assert material_data["materialType"] == cmd
    assert "args" in material_data  # 未知材料应该将额外参数保存在args中
