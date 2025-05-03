import openseespy.opensees as ops
import pytest

from opsparser import ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    ops.wipe()
    return ElementManager()


@pytest.fixture
def element_manager_2d() -> ElementManager:
    """2D模型的ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)  # 2D模型 (平面应变)
    return ElementManager()


@pytest.fixture
def element_manager_3d() -> ElementManager:
    """3D模型的ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 4)  # 3D模型，每个节点4个自由度(u,p)
    return ElementManager()


def test_handle_SSPquadUP(element_manager_2d: ElementManager) -> None:
    """测试SSPquadUP元素的数据处理"""
    cmd = "element"
    # 根据文档创建SSPquadUP元素
    # element('SSPquadUP', eleTag, *eleNodes, matTag, thick, fBulk, fDen, k1, k2, void, alpha, <b1=0.0, b2=0.0>)
    args = ("SSPquadUP", 1, *[1, 2, 3, 4], 101, 0.5, 2.0e6, 1.0, 1.0e-4, 1.2e-4, 0.4, 0.2)
    element_manager_2d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager_2d.elements
    element_data = element_manager_2d.elements[1]
    assert element_data["eleType"] == "SSPquadUP"
    assert element_data["eleTag"] == 1
    assert element_data["eleNodes"] == [1, 2, 3, 4]
    assert element_data["matTag"] == 101
    assert element_data["thick"] == 0.5
    assert element_data["fBulk"] == 2.0e6
    assert element_data["fDen"] == 1.0
    assert element_data["k1"] == 1.0e-4
    assert element_data["k2"] == 1.2e-4
    assert element_data["void"] == 0.4
    assert element_data["alpha"] == 0.2


def test_handle_SSPquadUP_with_options(element_manager_2d: ElementManager) -> None:
    """测试带可选参数的SSPquadUP元素的数据处理"""
    cmd = "element"
    # 使用可选参数b1和b2
    args = ("SSPquadUP", 2, *[11, 12, 13, 14], 102, 0.6, 2.1e6, 1.1, 1.1e-4, 1.3e-4, 0.5, 0.3, 0.5, 0.6)
    element_manager_2d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 2 in element_manager_2d.elements
    element_data = element_manager_2d.elements[2]
    assert element_data["eleType"] == "SSPquadUP"
    assert element_data["eleTag"] == 2
    assert element_data["eleNodes"] == [11, 12, 13, 14]
    assert element_data["matTag"] == 102
    assert element_data["thick"] == 0.6
    assert element_data["fBulk"] == 2.1e6
    assert element_data["fDen"] == 1.1
    assert element_data["k1"] == 1.1e-4
    assert element_data["k2"] == 1.3e-4
    assert element_data["void"] == 0.5
    assert element_data["alpha"] == 0.3
    assert element_data["b1"] == 0.5
    assert element_data["b2"] == 0.6


def test_handle_SSPbrickUP(element_manager_3d: ElementManager) -> None:
    """测试SSPbrickUP元素的数据处理"""
    cmd = "element"
    # 根据文档创建SSPbrickUP元素
    # element('SSPbrickUP', eleTag, *eleNodes, matTag, fBulk, fDen, k1, k2, k3, void, alpha, <b1, b2, b3>)
    args = ("SSPbrickUP", 3, *[21, 22, 23, 24, 25, 26, 27, 28], 103, 2.2e6, 1.2, 1.2e-4, 1.3e-4, 1.4e-4, 0.6, 0.4)
    element_manager_3d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 3 in element_manager_3d.elements
    element_data = element_manager_3d.elements[3]
    assert element_data["eleType"] == "SSPbrickUP"
    assert element_data["eleTag"] == 3
    assert element_data["eleNodes"] == [21, 22, 23, 24, 25, 26, 27, 28]
    assert element_data["matTag"] == 103
    assert element_data["fBulk"] == 2.2e6
    assert element_data["fDen"] == 1.2
    assert element_data["k1"] == 1.2e-4
    assert element_data["k2"] == 1.3e-4
    assert element_data["k3"] == 1.4e-4
    assert element_data["void"] == 0.6
    assert element_data["alpha"] == 0.4


def test_handle_SSPbrickUP_with_options(element_manager_3d: ElementManager) -> None:
    """测试带可选参数的SSPbrickUP元素的数据处理"""
    cmd = "element"
    # 使用可选参数b1、b2和b3
    args = ("SSPbrickUP", 4, *[31, 32, 33, 34, 35, 36, 37, 38], 104, 2.3e6, 1.3, 1.3e-4, 1.4e-4, 1.5e-4, 0.7, 0.5, 0.1, 0.2, 0.3)
    element_manager_3d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 4 in element_manager_3d.elements
    element_data = element_manager_3d.elements[4]
    assert element_data["eleType"] == "SSPbrickUP"
    assert element_data["eleTag"] == 4
    assert element_data["eleNodes"] == [31, 32, 33, 34, 35, 36, 37, 38]
    assert element_data["matTag"] == 104
    assert element_data["fBulk"] == 2.3e6
    assert element_data["fDen"] == 1.3
    assert element_data["k1"] == 1.3e-4
    assert element_data["k2"] == 1.4e-4
    assert element_data["k3"] == 1.5e-4
    assert element_data["void"] == 0.7
    assert element_data["alpha"] == 0.5
    assert element_data["b1"] == 0.1
    assert element_data["b2"] == 0.2
    assert element_data["b3"] == 0.3


def test_handle_unknown_OtherUp(element_manager_3d: ElementManager) -> None:
    """测试处理未知的OtherUp元素类型"""
    cmd = "element"
    # 使用一个不存在的OtherUp元素类型
    args = ("unknownSSPelement", 5, *[41, 42, 43, 44, 45, 46, 47, 48], 105, 2.4e6, 1.4, 1.4e-4, 1.5e-4, 1.6e-4, 0.8, 0.6)
    element_manager_3d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 5 in element_manager_3d.elements
    element_data = element_manager_3d.elements[5]
    assert element_data["eleType"] == "unknownSSPelement"
    assert element_data["eleTag"] == 5
    assert "args" in element_data  # 未知元素应该将额外参数保存在args中
