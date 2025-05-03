import openseespy.opensees as ops
import pytest

from opsparser import ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return ElementManager()


def test_handle_SimpleContact2D(element_manager: ElementManager) -> None:
    """测试SimpleContact2D元素的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 2)

    cmd = "element"
    args = ("SimpleContact2D", 1, 1, 2, 3, 4, 10, 0.01, 0.001)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager.elements
    element_data = element_manager.elements[1]
    assert element_data["eleType"] == "SimpleContact2D"
    assert element_data["eleTag"] == 1
    assert element_data["iNode"] == 1
    assert element_data["jNode"] == 2
    assert element_data["cNode"] == 3
    assert element_data["lNode"] == 4
    assert element_data["matTag"] == 10
    assert element_data["gTol"] == 0.01
    assert element_data["fTol"] == 0.001


def test_handle_SimpleContact3D(element_manager: ElementManager) -> None:
    """测试SimpleContact3D元素的数据处理"""
    # 设置3D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 3)

    cmd = "element"
    args = ("SimpleContact3D", 2, 1, 2, 3, 4, 5, 6, 20, 0.02, 0.002)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 2 in element_manager.elements
    element_data = element_manager.elements[2]
    assert element_data["eleType"] == "SimpleContact3D"
    assert element_data["eleTag"] == 2
    assert element_data["iNode"] == 1
    assert element_data["jNode"] == 2
    assert element_data["kNode"] == 3
    assert element_data["lNode"] == 4
    assert element_data["cNode"] == 5
    assert element_data["lagr_node"] == 6
    assert element_data["matTag"] == 20
    assert element_data["gTol"] == 0.02
    assert element_data["fTol"] == 0.002


def test_handle_BeamContact2D(element_manager: ElementManager) -> None:
    """测试BeamContact2D元素的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    cmd = "element"
    args = ("BeamContact2D", 3, 1, 2, 3, 4, 30, 0.5, 0.03, 0.003)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 3 in element_manager.elements
    element_data = element_manager.elements[3]
    assert element_data["eleType"] == "BeamContact2D"
    assert element_data["eleTag"] == 3
    assert element_data["iNode"] == 1
    assert element_data["jNode"] == 2
    assert element_data["sNode"] == 3
    assert element_data["lNode"] == 4
    assert element_data["matTag"] == 30
    assert element_data["width"] == 0.5
    assert element_data["gTol"] == 0.03
    assert element_data["fTol"] == 0.003


def test_handle_BeamContact2D_with_options(element_manager: ElementManager) -> None:
    """测试带选项的BeamContact2D元素的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    cmd = "element"
    args = ("BeamContact2D", 4, 5, 6, 7, 8, 31, 0.6, 0.04, 0.004, 1)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 4 in element_manager.elements
    element_data = element_manager.elements[4]
    assert element_data["eleType"] == "BeamContact2D"
    assert element_data["eleTag"] == 4
    assert element_data["iNode"] == 5
    assert element_data["jNode"] == 6
    assert element_data["sNode"] == 7
    assert element_data["lNode"] == 8
    assert element_data["matTag"] == 31
    assert element_data["width"] == 0.6
    assert element_data["gTol"] == 0.04
    assert element_data["fTol"] == 0.004
    assert element_data["cFlag"] == 1


def test_handle_BeamContact3D(element_manager: ElementManager) -> None:
    """测试BeamContact3D元素的数据处理"""
    cmd = "element"
    args = ("BeamContact3D", 5, 1, 2, 3, 4, 0.25, 1, 40, 0.05, 0.005)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 5 in element_manager.elements
    element_data = element_manager.elements[5]
    assert element_data["eleType"] == "BeamContact3D"
    assert element_data["eleTag"] == 5
    assert element_data["iNode"] == 1
    assert element_data["jNode"] == 2
    assert element_data["cNode"] == 3
    assert element_data["lNode"] == 4
    assert element_data["radius"] == 0.25
    assert element_data["crdTransf"] == 1
    assert element_data["matTag"] == 40
    assert element_data["gTol"] == 0.05
    assert element_data["fTol"] == 0.005


def test_handle_BeamContact3D_with_options(element_manager: ElementManager) -> None:
    """测试带选项的BeamContact3D元素的数据处理"""
    cmd = "element"
    args = ("BeamContact3D", 6, 5, 6, 7, 8, 0.30, 2, 41, 0.06, 0.006, 1)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 6 in element_manager.elements
    element_data = element_manager.elements[6]
    assert element_data["eleType"] == "BeamContact3D"
    assert element_data["eleTag"] == 6
    assert element_data["iNode"] == 5
    assert element_data["jNode"] == 6
    assert element_data["cNode"] == 7
    assert element_data["lNode"] == 8
    assert element_data["radius"] == 0.30
    assert element_data["crdTransf"] == 2
    assert element_data["matTag"] == 41
    assert element_data["gTol"] == 0.06
    assert element_data["fTol"] == 0.006
    assert element_data["cFlag"] == 1


def test_handle_BeamEndContact3D(element_manager: ElementManager) -> None:
    """测试BeamEndContact3D元素的数据处理"""
    cmd = "element"
    args = ("BeamEndContact3D", 7, 1, 2, 3, 4, 0.35, 0.07, 0.007)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 7 in element_manager.elements
    element_data = element_manager.elements[7]
    assert element_data["eleType"] == "BeamEndContact3D"
    assert element_data["eleTag"] == 7
    assert element_data["iNode"] == 1
    assert element_data["jNode"] == 2
    assert element_data["cNode"] == 3
    assert element_data["lNode"] == 4
    assert element_data["radius"] == 0.35
    assert element_data["gTol"] == 0.07
    assert element_data["fTol"] == 0.007


def test_handle_BeamEndContact3D_with_options(element_manager: ElementManager) -> None:
    """测试带选项的BeamEndContact3D元素的数据处理"""
    cmd = "element"
    args = ("BeamEndContact3D", 8, 5, 6, 7, 8, 0.40, 0.08, 0.008, 1)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 8 in element_manager.elements
    element_data = element_manager.elements[8]
    assert element_data["eleType"] == "BeamEndContact3D"
    assert element_data["eleTag"] == 8
    assert element_data["iNode"] == 5
    assert element_data["jNode"] == 6
    assert element_data["cNode"] == 7
    assert element_data["lNode"] == 8
    assert element_data["radius"] == 0.40
    assert element_data["gTol"] == 0.08
    assert element_data["fTol"] == 0.008
    assert element_data["cFlag"] == 1


def test_handle_unknown_Contact(element_manager: ElementManager) -> None:
    """测试处理未知的接触元素"""
    cmd = "element"
    args = ("CustomContact", 9, 1, 2, 3, 4, 50, 0.1, 0.01)

    # 未知元素类型将导致异常，这应该被ElementManager.handle_unknown_element捕获并处理
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储为未知元素
    assert 9 in element_manager.elements
    element_data = element_manager.elements[9]
    assert element_data["eleType"] == "CustomContact"
    assert element_data["eleTag"] == 9
    assert "args" in element_data  # 未知元素应该将额外参数保存在args中
