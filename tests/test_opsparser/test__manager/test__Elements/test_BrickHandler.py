import openseespy.opensees as ops
import pytest

from opsparser import ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 3)  # 砖块元素只能在3D模型中使用
    return ElementManager()


def test_handle_stdBrick(element_manager: ElementManager) -> None:
    """测试标准砖块元素的数据处理"""
    cmd = "element"
    args = ("stdBrick", 1, *[1, 2, 3, 4, 5, 6, 7, 8], 101)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager.elements
    element_data = element_manager.elements[1]
    assert element_data["eleType"] == "stdBrick"
    assert element_data["eleTag"] == 1
    assert element_data["eleNodes"] == [1, 2, 3, 4, 5, 6, 7, 8]
    assert element_data["matTag"] == 101


def test_handle_stdBrick_with_body_forces(element_manager: ElementManager) -> None:
    """测试带体力的标准砖块元素的数据处理"""
    cmd = "element"
    args = ("stdBrick", 2, *[11, 12, 13, 14, 15, 16, 17, 18], 102, 0.5, 1.0, 1.5)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 2 in element_manager.elements
    element_data = element_manager.elements[2]
    assert element_data["eleType"] == "stdBrick"
    assert element_data["eleTag"] == 2
    assert element_data["eleNodes"] == [11, 12, 13, 14, 15, 16, 17, 18]
    assert element_data["matTag"] == 102
    assert element_data["b1"] == 0.5
    assert element_data["b2"] == 1.0
    assert element_data["b3"] == 1.5


def test_handle_bbarBrick(element_manager: ElementManager) -> None:
    """测试bbarBrick元素的数据处理"""
    cmd = "element"
    args = ("bbarBrick", 3, *[21, 22, 23, 24, 25, 26, 27, 28], 103)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 3 in element_manager.elements
    element_data = element_manager.elements[3]
    assert element_data["eleType"] == "bbarBrick"
    assert element_data["eleTag"] == 3
    assert element_data["eleNodes"] == [21, 22, 23, 24, 25, 26, 27, 28]
    assert element_data["matTag"] == 103


def test_handle_bbarBrick_with_body_forces(element_manager: ElementManager) -> None:
    """测试带体力的bbarBrick元素的数据处理"""
    cmd = "element"
    args = ("bbarBrick", 4, *[31, 32, 33, 34, 35, 36, 37, 38], 104, 0.2, 0.3, 0.4)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 4 in element_manager.elements
    element_data = element_manager.elements[4]
    assert element_data["eleType"] == "bbarBrick"
    assert element_data["eleTag"] == 4
    assert element_data["eleNodes"] == [31, 32, 33, 34, 35, 36, 37, 38]
    assert element_data["matTag"] == 104
    assert element_data["b1"] == 0.2
    assert element_data["b2"] == 0.3
    assert element_data["b3"] == 0.4


def test_handle_20NodeBrick(element_manager: ElementManager) -> None:
    """测试20节点砖块元素的数据处理"""
    cmd = "element"
    node_ids = list(range(41, 61))  # 20个节点：41-60
    args = ("20NodeBrick", 5, *node_ids, 105, 0.1, 0.2, 0.3, 2000.0)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 5 in element_manager.elements
    element_data = element_manager.elements[5]
    assert element_data["eleType"] == "20NodeBrick"
    assert element_data["eleTag"] == 5
    assert element_data["eleNodes"] == node_ids
    assert element_data["matTag"] == 105
    assert element_data["bf1"] == 0.1
    assert element_data["bf2"] == 0.2
    assert element_data["bf3"] == 0.3
    assert element_data["massDen"] == 2000.0


def test_handle_SSPbrick(element_manager: ElementManager) -> None:
    """测试SSPbrick元素的数据处理"""
    cmd = "element"
    args = ("SSPbrick", 6, *[61, 62, 63, 64, 65, 66, 67, 68], 106)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 6 in element_manager.elements
    element_data = element_manager.elements[6]
    assert element_data["eleType"] == "SSPbrick"
    assert element_data["eleTag"] == 6
    assert element_data["eleNodes"] == [61, 62, 63, 64, 65, 66, 67, 68]
    assert element_data["matTag"] == 106


def test_handle_SSPbrick_with_body_forces(element_manager: ElementManager) -> None:
    """测试带体力的SSPbrick元素的数据处理"""
    cmd = "element"
    args = ("SSPbrick", 7, *[71, 72, 73, 74, 75, 76, 77, 78], 107, 0.6, 0.7, 0.8)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 7 in element_manager.elements
    element_data = element_manager.elements[7]
    assert element_data["eleType"] == "SSPbrick"
    assert element_data["eleTag"] == 7
    assert element_data["eleNodes"] == [71, 72, 73, 74, 75, 76, 77, 78]
    assert element_data["matTag"] == 107
    assert element_data["b1"] == 0.6
    assert element_data["b2"] == 0.7
    assert element_data["b3"] == 0.8


def test_handle_unknown_Brick(element_manager: ElementManager) -> None:
    """测试处理未知的砖块元素"""
    cmd = "element"
    args = ("customBrick", 8, *[81, 82, 83, 84, 85, 86, 87, 88], 108)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 8 in element_manager.elements
    element_data = element_manager.elements[8]
    assert element_data["eleType"] == "customBrick"
    assert element_data["eleTag"] == 8
    assert "args" in element_data  # 未知元素应该将额外参数保存在args中
