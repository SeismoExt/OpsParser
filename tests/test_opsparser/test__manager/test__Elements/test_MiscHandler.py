import openseespy.opensees as ops
import pytest

from opsparser import ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return ElementManager()


def test_handle_SurfaceLoad(element_manager: ElementManager) -> None:
    """测试SurfaceLoad元素的数据处理"""
    # SurfaceLoad元素需要3D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 3)

    # 创建SurfaceLoad元素
    cmd = "element"
    args = ("SurfaceLoad", 1, *[1, 2, 3, 4], 10.5)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager.elements
    element_data = element_manager.elements[1]
    assert element_data["eleType"] == "SurfaceLoad"
    assert element_data["eleTag"] == 1
    assert element_data["eleNodes"] == [1, 2, 3, 4]
    assert element_data["p"] == 10.5


def test_handle_VS3D4(element_manager: ElementManager) -> None:
    """测试VS3D4元素的数据处理"""
    # 设置3D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 3)

    # 创建VS3D4元素
    cmd = "element"
    args = ("VS3D4", 2, *[5, 6, 7, 8], 29000.0, 11000.0, 7.85e-9, 100.0, 1.0, 0.5)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 2 in element_manager.elements
    element_data = element_manager.elements[2]
    assert element_data["eleType"] == "VS3D4"
    assert element_data["eleTag"] == 2
    assert element_data["eleNodes"] == [5, 6, 7, 8]
    assert element_data["E"] == 29000.0
    assert element_data["G"] == 11000.0
    assert element_data["rho"] == 7.85e-9
    assert element_data["R"] == 100.0
    assert element_data["alphaN"] == 1.0
    assert element_data["alphaT"] == 0.5


def test_handle_AC3D8(element_manager: ElementManager) -> None:
    """测试AC3D8元素的数据处理"""
    # 设置3D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 3)

    # 创建AC3D8元素
    cmd = "element"
    args = ("AC3D8", 3, *[9, 10, 11, 12, 13, 14, 15, 16], 101)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 3 in element_manager.elements
    element_data = element_manager.elements[3]
    assert element_data["eleType"] == "AC3D8"
    assert element_data["eleTag"] == 3
    assert element_data["eleNodes"] == [9, 10, 11, 12, 13, 14, 15, 16]
    assert element_data["matTag"] == 101


def test_handle_ASI3D8(element_manager: ElementManager) -> None:
    """测试ASI3D8元素的数据处理"""
    # 设置3D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 3)

    # 创建ASI3D8元素
    cmd = "element"
    args = ("ASI3D8", 4, *[17, 18, 19, 20], *[21, 22, 23, 24])
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 4 in element_manager.elements
    element_data = element_manager.elements[4]
    assert element_data["eleType"] == "ASI3D8"
    assert element_data["eleTag"] == 4
    assert element_data["eleNodes1"] == [17, 18, 19, 20]
    assert element_data["eleNodes2"] == [21, 22, 23, 24]


def test_handle_AV3D4(element_manager: ElementManager) -> None:
    """测试AV3D4元素的数据处理"""
    # 设置3D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 3)

    # 创建AV3D4元素
    cmd = "element"
    args = ("AV3D4", 5, *[25, 26, 27, 28], 102)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 5 in element_manager.elements
    element_data = element_manager.elements[5]
    assert element_data["eleType"] == "AV3D4"
    assert element_data["eleTag"] == 5
    assert element_data["eleNodes"] == [25, 26, 27, 28]
    assert element_data["matTag"] == 102


def test_handle_MasonPan12(element_manager: ElementManager) -> None:
    """测试MasonPan12元素的数据处理"""
    # 设置2D模型环境 (MasonPan12通常用于二维平面问题)
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # 创建MasonPan12元素
    cmd = "element"
    nodes = list(range(29, 41))  # 12个节点
    args = ("MasonPan12", 6, *nodes, 201, 202, 0.25, 0.15, 0.3)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 6 in element_manager.elements
    element_data = element_manager.elements[6]
    assert element_data["eleType"] == "MasonPan12"
    assert element_data["eleTag"] == 6
    assert element_data["eleNodes"] == nodes
    assert element_data["mat_1"] == 201
    assert element_data["mat_2"] == 202
    assert element_data["thick"] == 0.25
    assert element_data["w_tot"] == 0.15
    assert element_data["w_1"] == 0.3


def test_handle_unknown_MiscHandler(element_manager: ElementManager) -> None:
    """测试处理未知的MiscHandler元素"""
    cmd = "element"
    args = ("customMiscElement", 7, *[42, 43, 44, 45], 1.0, 2.0, 3.0)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 7 in element_manager.elements
    element_data = element_manager.elements[7]
    assert element_data["eleType"] == "customMiscElement"
    assert element_data["eleTag"] == 7
    assert "args" in element_data  # 未知元素应该将额外参数保存在args中
