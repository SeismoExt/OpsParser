import openseespy.opensees as ops
import pytest

from opsparser import ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return ElementManager()


def test_handle_PFEMElementBubble_2D(element_manager: ElementManager) -> None:
    """测试2D模式下PFEMElementBubble元素的数据处理"""
    # 设置模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # PFEMElementBubble 2D参数: eleTag, *eleNodes(3个节点), rho, mu, b1, b2, thickness, kappa(可选)
    cmd = "element"
    args = (
        "PFEMElementBubble", 1, 1, 2, 3, 1000.0, 1.0e-3, 0.0, -9.81, 0.1, 2.2e9
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager.elements
    element_data = element_manager.elements[1]
    assert element_data["eleType"] == "PFEMElementBubble"
    assert element_data["eleTag"] == 1
    assert element_data["eleNodes"] == [1, 2, 3]
    assert element_data["rho"] == 1000.0
    assert element_data["mu"] == 1.0e-3
    assert element_data["b1"] == 0.0
    assert element_data["b2"] == -9.81
    assert element_data["thickness"] == 0.1
    assert element_data["kappa"] == 2.2e9


def test_handle_PFEMElementBubble_3D(element_manager: ElementManager) -> None:
    """测试3D模式下PFEMElementBubble元素的数据处理"""
    # 设置模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 4)

    # PFEMElementBubble 3D参数: eleTag, *eleNodes(4个节点), rho, mu, b1, b2, b3, kappa(可选)
    cmd = "element"
    args = (
        "PFEMElementBubble", 2, 4, 5, 6, 7, 1000.0, 1.0e-3, 0.0, 0.0, -9.81, 2.2e9
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 2 in element_manager.elements
    element_data = element_manager.elements[2]
    assert element_data["eleType"] == "PFEMElementBubble"
    assert element_data["eleTag"] == 2
    assert element_data["eleNodes"] == [4, 5, 6, 7]
    assert element_data["rho"] == 1000.0
    assert element_data["mu"] == 1.0e-3
    assert element_data["b1"] == 0.0
    assert element_data["b2"] == 0.0
    assert element_data["b3"] == -9.81
    assert element_data["kappa"] == 2.2e9


def test_handle_PFEMElementBubble_without_kappa(element_manager: ElementManager) -> None:
    """测试PFEMElementBubble元素不带kappa参数的数据处理"""
    # 设置模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # PFEMElementBubble不带kappa: eleTag, *eleNodes(3个节点), rho, mu, b1, b2, thickness
    cmd = "element"
    args = (
        "PFEMElementBubble", 3, 8, 9, 10, 1000.0, 1.0e-3, 0.0, -9.81, 0.1
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 3 in element_manager.elements
    element_data = element_manager.elements[3]
    assert element_data["eleType"] == "PFEMElementBubble"
    assert element_data["eleTag"] == 3
    assert element_data["eleNodes"] == [8, 9, 10]
    assert element_data["rho"] == 1000.0
    assert element_data["mu"] == 1.0e-3
    assert element_data["b1"] == 0.0
    assert element_data["b2"] == -9.81
    assert element_data["thickness"] == 0.1
    assert "kappa" not in element_data


def test_handle_PFEMElementCompressible(element_manager: ElementManager) -> None:
    """测试PFEMElementCompressible元素的数据处理"""
    # 设置模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # PFEMElementCompressible参数: eleTag, *eleNodes(4个节点), rho, mu, b1, b2, thickness(可选), kappa(可选)
    cmd = "element"
    args = (
        "PFEMElementCompressible", 4, 11, 12, 13, 14, 1000.0, 1.0e-3, 0.0, -9.81, 0.1, 2.2e9
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 4 in element_manager.elements
    element_data = element_manager.elements[4]
    assert element_data["eleType"] == "PFEMElementCompressible"
    assert element_data["eleTag"] == 4
    assert element_data["eleNodes"] == [11, 12, 13, 14]
    assert element_data["rho"] == 1000.0
    assert element_data["mu"] == 1.0e-3
    assert element_data["b1"] == 0.0
    assert element_data["b2"] == -9.81
    assert element_data["thickness"] == 0.1
    assert element_data["kappa"] == 2.2e9


def test_handle_PFEMElementCompressible_without_optionals(element_manager: ElementManager) -> None:
    """测试PFEMElementCompressible元素不带可选参数的数据处理"""
    # 设置模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # PFEMElementCompressible不带可选参数: eleTag, *eleNodes(4个节点), rho, mu, b1, b2
    cmd = "element"
    args = (
        "PFEMElementCompressible", 5, 15, 16, 17, 18, 1000.0, 1.0e-3, 0.0, -9.81
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 5 in element_manager.elements
    element_data = element_manager.elements[5]
    assert element_data["eleType"] == "PFEMElementCompressible"
    assert element_data["eleTag"] == 5
    assert element_data["eleNodes"] == [15, 16, 17, 18]
    assert element_data["rho"] == 1000.0
    assert element_data["mu"] == 1.0e-3
    assert element_data["b1"] == 0.0
    assert element_data["b2"] == -9.81
    assert "thickness" not in element_data
    assert "kappa" not in element_data


def test_handle_PFEMElementCompressible_3D_error(element_manager: ElementManager) -> None:
    """测试PFEMElementCompressible元素在3D模式下的错误处理"""
    # 设置模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 4)

    # PFEMElementCompressible在3D模式下不支持
    cmd = "element"
    args = (
        "PFEMElementCompressible", 6, 19, 20, 21, 22, 1000.0, 1.0e-3, 0.0, 0.0, -9.81
    )

    # 应该抛出KeyError异常
    with pytest.raises(KeyError):
        element_manager.handle(cmd, {"args": args, "kwargs": {}})


def test_handle_unknown_PFEM(element_manager: ElementManager) -> None:
    """测试处理未知的PFEM元素"""
    cmd = "element"
    args = ("customPFEM", 7, 23, 24, 25, 1000.0, 1.0e-3, 0.0, -9.81)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 7 in element_manager.elements
    element_data = element_manager.elements[7]
    assert element_data["eleType"] == "customPFEM"
    assert element_data["eleTag"] == 7
    assert "args" in element_data  # 未知元素应该将额外参数保存在args中
