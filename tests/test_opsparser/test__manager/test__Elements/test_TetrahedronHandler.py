import openseespy.opensees as ops
import pytest

from opsparser import ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return ElementManager()


def test_handle_FourNodeTetrahedron(element_manager: ElementManager) -> None:
    """测试FourNodeTetrahedron元素的基本数据处理"""
    # 创建FourNodeTetrahedron元素
    cmd = "element"
    args = ("FourNodeTetrahedron", 1, *[1, 2, 3, 4], 100)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager.elements
    element_data = element_manager.elements[1]
    assert element_data["eleType"] == "FourNodeTetrahedron"
    assert element_data["eleTag"] == 1
    assert element_data["eleNodes"] == [1, 2, 3, 4]
    assert element_data["matTag"] == 100


def test_handle_FourNodeTetrahedron_with_bodyforces(element_manager: ElementManager) -> None:
    """测试带体力参数的FourNodeTetrahedron元素的数据处理"""
    # 创建带体力的FourNodeTetrahedron元素
    cmd = "element"
    args = ("FourNodeTetrahedron", 2, *[5, 6, 7, 8], 101, 0.0, -9.81, 0.0)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 2 in element_manager.elements
    element_data = element_manager.elements[2]
    assert element_data["eleType"] == "FourNodeTetrahedron"
    assert element_data["eleTag"] == 2
    assert element_data["eleNodes"] == [5, 6, 7, 8]
    assert element_data["matTag"] == 101
    assert element_data["b1"] == 0.0
    assert element_data["b2"] == -9.81
    assert element_data["b3"] == 0.0
