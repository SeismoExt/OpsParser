import openseespy.opensees as ops
import pytest

from opsparser import ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return ElementManager()


def test_handle_CatenaryCable(element_manager: ElementManager) -> None:
    """测试CatenaryCable元素的数据处理"""
    # 设置模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 3)

    # CatenaryCable参数: eleTag, iNode, jNode, weight, E, A, L0, alpha, temperature_change, rho, errorTol, Nsubsteps, massType
    cmd = "element"
    args = (
        "CatenaryCable", 1, 1, 2, 10.0, 29000.0, 1.5, 100.0,
        1.2e-5, 20.0, 0.0078, 1e-8, 5, 0
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager.elements
    element_data = element_manager.elements[1]
    assert element_data["eleType"] == "CatenaryCable"
    assert element_data["eleTag"] == 1
    assert element_data["iNode"] == 1
    assert element_data["jNode"] == 2
    assert element_data["weight"] == 10.0
    assert element_data["E"] == 29000.0
    assert element_data["A"] == 1.5
    assert element_data["L0"] == 100.0
    assert element_data["alpha"] == 1.2e-5
    assert element_data["temperature_change"] == 20.0
    assert element_data["rho"] == 0.0078
    assert element_data["errorTol"] == 1e-8
    assert element_data["Nsubsteps"] == 5
    assert element_data["massType"] == 0


def test_handle_CatenaryCable_different_values(element_manager: ElementManager) -> None:
    """测试CatenaryCable元素的数据处理（使用不同的参数值）"""
    cmd = "element"
    args = (
        "CatenaryCable", 2, 3, 4, 15.0, 30000.0, 2.0, 120.0,
        1.5e-5, 25.0, 0.008, 1e-9, 10, 1
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 2 in element_manager.elements
    element_data = element_manager.elements[2]
    assert element_data["eleType"] == "CatenaryCable"
    assert element_data["eleTag"] == 2
    assert element_data["iNode"] == 3
    assert element_data["jNode"] == 4
    assert element_data["weight"] == 15.0
    assert element_data["E"] == 30000.0
    assert element_data["A"] == 2.0
    assert element_data["L0"] == 120.0
    assert element_data["alpha"] == 1.5e-5
    assert element_data["temperature_change"] == 25.0
    assert element_data["rho"] == 0.008
    assert element_data["errorTol"] == 1e-9
    assert element_data["Nsubsteps"] == 10
    assert element_data["massType"] == 1


def test_handle_unknown_Cable(element_manager: ElementManager) -> None:
    """测试处理未知的缆索元素"""
    cmd = "element"
    args = ("customCable", 3, 5, 6, 10.0, 29000.0, 1.0, 80.0)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 3 in element_manager.elements
    element_data = element_manager.elements[3]
    assert element_data["eleType"] == "customCable"
    assert element_data["eleTag"] == 3
    assert "args" in element_data  # 未知元素应该将额外参数保存在args中
