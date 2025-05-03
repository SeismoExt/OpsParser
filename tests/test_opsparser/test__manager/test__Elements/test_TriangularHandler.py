import openseespy.opensees as ops
import pytest

from opsparser import ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return ElementManager()


def test_handle_Tri31(element_manager: ElementManager) -> None:
    """测试Tri31三角形元素的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # 创建Tri31单元
    cmd = "element"
    args = ("Tri31", 1, *[1, 2, 3], 0.2, "PlaneStress", 101)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager.elements
    element_data = element_manager.elements[1]
    assert element_data["eleType"] == "Tri31"
    assert element_data["eleTag"] == 1
    assert element_data["eleNodes"] == [1, 2, 3]
    assert element_data["thick"] == 0.2
    assert element_data["type"] == "PlaneStress"
    assert element_data["matTag"] == 101


def test_handle_Tri31_with_options(element_manager: ElementManager) -> None:
    """测试带选项的Tri31三角形元素的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # 创建带选项的Tri31单元
    cmd = "element"
    args = ("Tri31", 2, *[4, 5, 6], 0.25, "PlaneStrain", 102, "pressure", 15.0, "rho", 2400.0, "b1", 0.3, "b2", 0.4)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 2 in element_manager.elements
    element_data = element_manager.elements[2]
    assert element_data["eleType"] == "Tri31"
    assert element_data["eleTag"] == 2
    assert element_data["eleNodes"] == [4, 5, 6]
    assert element_data["thick"] == 0.25
    assert element_data["type"] == "PlaneStrain"
    assert element_data["matTag"] == 102
    assert element_data["pressure"] == 15.0
    assert element_data["rho"] == 2400.0
    assert element_data["b1"] == 0.3
    assert element_data["b2"] == 0.4


def test_handle_unknown_Triangular(element_manager: ElementManager) -> None:
    """测试处理未知的三角形元素"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # 创建未知类型的三角形单元
    cmd = "element"
    args = ("customTri", 3, *[7, 8, 9], 0.3, "PlaneStress", 103)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 3 in element_manager.elements
    element_data = element_manager.elements[3]
    assert element_data["eleType"] == "customTri"
    assert element_data["eleTag"] == 3
    assert "args" in element_data  # 未知元素应该将额外参数保存在args中
