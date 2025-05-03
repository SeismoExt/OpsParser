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


def test_handle_quadUP(element_manager_2d: ElementManager) -> None:
    """测试四节点四边形u-p元素的数据处理"""
    cmd = "element"
    args = ("quadUP", 1, *[1, 2, 3, 4], 0.5, 101, 2.0e6, 1.0, 1.0e-4, 1.0e-4)
    element_manager_2d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager_2d.elements
    element_data = element_manager_2d.elements[1]
    assert element_data["eleType"] == "quadUP"
    assert element_data["eleTag"] == 1
    assert element_data["eleNodes"] == [1, 2, 3, 4]
    assert element_data["thick"] == 0.5
    assert element_data["matTag"] == 101
    assert element_data["bulk"] == 2.0e6
    assert element_data["fmass"] == 1.0
    assert element_data["hPerm"] == 1.0e-4
    assert element_data["vPerm"] == 1.0e-4


def test_handle_quadUP_with_options(element_manager_2d: ElementManager) -> None:
    """测试带可选参数的四节点四边形u-p元素的数据处理"""
    cmd = "element"
    args = ("quadUP", 2, *[11, 12, 13, 14], 0.4, 102, 2.1e6, 1.1, 1.1e-4, 1.2e-4, 0.5, 0.6, 0.7)
    element_manager_2d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 2 in element_manager_2d.elements
    element_data = element_manager_2d.elements[2]
    assert element_data["eleType"] == "quadUP"
    assert element_data["eleTag"] == 2
    assert element_data["eleNodes"] == [11, 12, 13, 14]
    assert element_data["thick"] == 0.4
    assert element_data["matTag"] == 102
    assert element_data["bulk"] == 2.1e6
    assert element_data["fmass"] == 1.1
    assert element_data["hPerm"] == 1.1e-4
    assert element_data["vPerm"] == 1.2e-4
    assert element_data["b1"] == 0.5
    assert element_data["b2"] == 0.6
    assert element_data["t"] == 0.7


def test_handle_bbarQuadUP(element_manager_2d: ElementManager) -> None:
    """测试bbar四边形u-p元素的数据处理"""
    cmd = "element"
    args = ("bbarQuadUP", 3, *[21, 22, 23, 24], 0.6, 103, 2.2e6, 1.2, 1.2e-4, 1.3e-4)
    element_manager_2d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 3 in element_manager_2d.elements
    element_data = element_manager_2d.elements[3]
    assert element_data["eleType"] == "bbarQuadUP"
    assert element_data["eleTag"] == 3
    assert element_data["eleNodes"] == [21, 22, 23, 24]
    assert element_data["thick"] == 0.6
    assert element_data["matTag"] == 103
    assert element_data["bulk"] == 2.2e6
    assert element_data["fmass"] == 1.2
    assert element_data["hPerm"] == 1.2e-4
    assert element_data["vPerm"] == 1.3e-4


def test_handle_bbarQuadUP_with_options(element_manager_2d: ElementManager) -> None:
    """测试带可选参数的bbar四边形u-p元素的数据处理"""
    cmd = "element"
    args = ("bbarQuadUP", 4, *[31, 32, 33, 34], 0.7, 104, 2.3e6, 1.3, 1.3e-4, 1.4e-4, 0.1, 0.2, 0.3)
    element_manager_2d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 4 in element_manager_2d.elements
    element_data = element_manager_2d.elements[4]
    assert element_data["eleType"] == "bbarQuadUP"
    assert element_data["eleTag"] == 4
    assert element_data["eleNodes"] == [31, 32, 33, 34]
    assert element_data["thick"] == 0.7
    assert element_data["matTag"] == 104
    assert element_data["bulk"] == 2.3e6
    assert element_data["fmass"] == 1.3
    assert element_data["hPerm"] == 1.3e-4
    assert element_data["vPerm"] == 1.4e-4
    assert element_data["b1"] == 0.1
    assert element_data["b2"] == 0.2
    assert element_data["t"] == 0.3


def test_handle_9_4_QuadUP(element_manager_2d: ElementManager) -> None:
    """测试九四节点四边形u-p元素的数据处理"""
    cmd = "element"
    node_ids = list(range(41, 50))  # 9个节点：41-49
    args = ("9_4_QuadUP", 5, *node_ids, 0.8, 105, 2.4e6, 1.4, 1.4e-4, 1.5e-4)
    element_manager_2d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 5 in element_manager_2d.elements
    element_data = element_manager_2d.elements[5]
    assert element_data["eleType"] == "9_4_QuadUP"
    assert element_data["eleTag"] == 5
    assert element_data["eleNodes"] == node_ids
    assert element_data["thick"] == 0.8
    assert element_data["matTag"] == 105
    assert element_data["bulk"] == 2.4e6
    assert element_data["fmass"] == 1.4
    assert element_data["hPerm"] == 1.4e-4
    assert element_data["vPerm"] == 1.5e-4


def test_handle_9_4_QuadUP_with_options(element_manager_2d: ElementManager) -> None:
    """测试带可选参数的九四节点四边形u-p元素的数据处理"""
    cmd = "element"
    node_ids = list(range(51, 60))  # 9个节点：51-59
    args = ("9_4_QuadUP", 6, *node_ids, 0.9, 106, 2.5e6, 1.5, 1.5e-4, 1.6e-4, 0.4, 0.5)
    element_manager_2d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 6 in element_manager_2d.elements
    element_data = element_manager_2d.elements[6]
    assert element_data["eleType"] == "9_4_QuadUP"
    assert element_data["eleTag"] == 6
    assert element_data["eleNodes"] == node_ids
    assert element_data["thick"] == 0.9
    assert element_data["matTag"] == 106
    assert element_data["bulk"] == 2.5e6
    assert element_data["fmass"] == 1.5
    assert element_data["hPerm"] == 1.5e-4
    assert element_data["vPerm"] == 1.6e-4
    assert element_data["b1"] == 0.4
    assert element_data["b2"] == 0.5


def test_handle_brickUP(element_manager_3d: ElementManager) -> None:
    """测试八节点六面体u-p元素的数据处理"""
    cmd = "element"
    args = ("brickUP", 7, *[61, 62, 63, 64, 65, 66, 67, 68], 107, 2.6e6, 1.6, 1.6e-4, 1.7e-4, 1.8e-4)
    element_manager_3d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 7 in element_manager_3d.elements
    element_data = element_manager_3d.elements[7]
    assert element_data["eleType"] == "brickUP"
    assert element_data["eleTag"] == 7
    assert element_data["eleNodes"] == [61, 62, 63, 64, 65, 66, 67, 68]
    assert element_data["matTag"] == 107
    assert element_data["bulk"] == 2.6e6
    assert element_data["fmass"] == 1.6
    assert element_data["permX"] == 1.6e-4
    assert element_data["permY"] == 1.7e-4
    assert element_data["permZ"] == 1.8e-4


def test_handle_brickUP_with_options(element_manager_3d: ElementManager) -> None:
    """测试带可选参数的八节点六面体u-p元素的数据处理"""
    cmd = "element"
    args = ("brickUP", 8, *[71, 72, 73, 74, 75, 76, 77, 78], 108, 2.7e6, 1.7, 1.7e-4, 1.8e-4, 1.9e-4, 0.5, 0.6, 0.7)
    element_manager_3d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 8 in element_manager_3d.elements
    element_data = element_manager_3d.elements[8]
    assert element_data["eleType"] == "brickUP"
    assert element_data["eleTag"] == 8
    assert element_data["eleNodes"] == [71, 72, 73, 74, 75, 76, 77, 78]
    assert element_data["matTag"] == 108
    assert element_data["bulk"] == 2.7e6
    assert element_data["fmass"] == 1.7
    assert element_data["permX"] == 1.7e-4
    assert element_data["permY"] == 1.8e-4
    assert element_data["permZ"] == 1.9e-4
    assert element_data["bX"] == 0.5
    assert element_data["bY"] == 0.6
    assert element_data["bZ"] == 0.7


def test_handle_bbarBrickUP(element_manager_3d: ElementManager) -> None:
    """测试bbar砖u-p元素的数据处理"""
    cmd = "element"
    args = ("bbarBrickUP", 9, *[81, 82, 83, 84, 85, 86, 87, 88], 109, 2.8e6, 1.8, 1.8e-4, 1.9e-4, 2.0e-4)
    element_manager_3d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 9 in element_manager_3d.elements
    element_data = element_manager_3d.elements[9]
    assert element_data["eleType"] == "bbarBrickUP"
    assert element_data["eleTag"] == 9
    assert element_data["eleNodes"] == [81, 82, 83, 84, 85, 86, 87, 88]
    assert element_data["matTag"] == 109
    assert element_data["bulk"] == 2.8e6
    assert element_data["fmass"] == 1.8
    assert element_data["permX"] == 1.8e-4
    assert element_data["permY"] == 1.9e-4
    assert element_data["permZ"] == 2.0e-4


def test_handle_bbarBrickUP_with_options(element_manager_3d: ElementManager) -> None:
    """测试带可选参数的bbar砖u-p元素的数据处理"""
    cmd = "element"
    args = ("bbarBrickUP", 10, *[91, 92, 93, 94, 95, 96, 97, 98], 110, 2.9e6, 1.9, 1.9e-4, 2.0e-4, 2.1e-4, 0.2, 0.3, 0.4)
    element_manager_3d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 10 in element_manager_3d.elements
    element_data = element_manager_3d.elements[10]
    assert element_data["eleType"] == "bbarBrickUP"
    assert element_data["eleTag"] == 10
    assert element_data["eleNodes"] == [91, 92, 93, 94, 95, 96, 97, 98]
    assert element_data["matTag"] == 110
    assert element_data["bulk"] == 2.9e6
    assert element_data["fmass"] == 1.9
    assert element_data["permX"] == 1.9e-4
    assert element_data["permY"] == 2.0e-4
    assert element_data["permZ"] == 2.1e-4
    assert element_data["bX"] == 0.2
    assert element_data["bY"] == 0.3
    assert element_data["bZ"] == 0.4


def test_handle_20_8_BrickUP(element_manager_3d: ElementManager) -> None:
    """测试二十八节点砖u-p元素的数据处理"""
    cmd = "element"
    node_ids = list(range(101, 121))  # 20个节点：101-120
    args = ("20_8_BrickUP", 11, *node_ids, 111, 3.0e6, 2.0, 2.0e-4, 2.1e-4, 2.2e-4)
    element_manager_3d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 11 in element_manager_3d.elements
    element_data = element_manager_3d.elements[11]
    assert element_data["eleType"] == "20_8_BrickUP"
    assert element_data["eleTag"] == 11
    assert element_data["eleNodes"] == node_ids
    assert element_data["matTag"] == 111
    assert element_data["bulk"] == 3.0e6
    assert element_data["fmass"] == 2.0
    assert element_data["permX"] == 2.0e-4
    assert element_data["permY"] == 2.1e-4
    assert element_data["permZ"] == 2.2e-4


def test_handle_20_8_BrickUP_with_options(element_manager_3d: ElementManager) -> None:
    """测试带可选参数的二十八节点砖u-p元素的数据处理"""
    cmd = "element"
    node_ids = list(range(121, 141))  # 20个节点：121-140
    args = ("20_8_BrickUP", 12, *node_ids, 112, 3.1e6, 2.1, 2.1e-4, 2.2e-4, 2.3e-4, 0.8, 0.9, 1.0)
    element_manager_3d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 12 in element_manager_3d.elements
    element_data = element_manager_3d.elements[12]
    assert element_data["eleType"] == "20_8_BrickUP"
    assert element_data["eleTag"] == 12
    assert element_data["eleNodes"] == node_ids
    assert element_data["matTag"] == 112
    assert element_data["bulk"] == 3.1e6
    assert element_data["fmass"] == 2.1
    assert element_data["permX"] == 2.1e-4
    assert element_data["permY"] == 2.2e-4
    assert element_data["permZ"] == 2.3e-4
    assert element_data["bX"] == 0.8
    assert element_data["bY"] == 0.9
    assert element_data["bZ"] == 1.0


def test_handle_unknown_UCSDUp(element_manager_3d: ElementManager) -> None:
    """测试处理未知的UCSD UP元素类型"""
    cmd = "element"
    # 使用一个不存在的UCSD UP元素类型
    args = ("customUP", 13, *[141, 142, 143, 144, 145, 146, 147, 148], 113, 3.2e6, 2.2, 2.2e-4, 2.3e-4, 2.4e-4)
    element_manager_3d.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 13 in element_manager_3d.elements
    element_data = element_manager_3d.elements[13]
    assert element_data["eleType"] == "customUP"
    assert element_data["eleTag"] == 13
    assert "args" in element_data  # 未知元素应该将额外参数保存在args中
