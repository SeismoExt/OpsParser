import openseespy.opensees as ops
import pytest

from opsparser import ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return ElementManager()


def test_handle_quad(element_manager: ElementManager) -> None:
    """测试四节点四边形单元的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # 创建quad单元
    cmd = "element"
    args = ("quad", 1, *[1, 2, 3, 4], 0.1, "PlaneStress", 101)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager.elements
    element_data = element_manager.elements[1]
    assert element_data["eleType"] == "quad"
    assert element_data["eleTag"] == 1
    assert element_data["eleNodes"] == [1, 2, 3, 4]
    assert element_data["thick"] == 0.1
    assert element_data["type"] == "PlaneStress"
    assert element_data["matTag"] == 101


def test_handle_quad_with_options(element_manager: ElementManager) -> None:
    """测试带选项的四节点四边形单元的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # 创建带选项的quad单元
    cmd = "element"
    args = ("quad", 2, *[5, 6, 7, 8], 0.15, "PlaneStrain", 102, "pressure", 10.0, "rho", 2500.0, "b1", 0.5, "b2", 0.5)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 2 in element_manager.elements
    element_data = element_manager.elements[2]
    assert element_data["eleType"] == "quad"
    assert element_data["eleTag"] == 2
    assert element_data["eleNodes"] == [5, 6, 7, 8]
    assert element_data["thick"] == 0.15
    assert element_data["type"] == "PlaneStrain"
    assert element_data["matTag"] == 102
    assert element_data["pressure"] == 10.0
    assert element_data["rho"] == 2500.0
    assert element_data["b1"] == 0.5
    assert element_data["b2"] == 0.5


def test_handle_ShellMITC4(element_manager: ElementManager) -> None:
    """测试MITC4壳单元的数据处理"""

    # 创建ShellMITC4单元
    cmd = "element"
    args = ("ShellMITC4", 3, *[9, 10, 11, 12], 201)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 3 in element_manager.elements
    element_data = element_manager.elements[3]
    assert element_data["eleType"] == "ShellMITC4"
    assert element_data["eleTag"] == 3
    assert element_data["eleNodes"] == [9, 10, 11, 12]
    assert element_data["secTag"] == 201


def test_handle_ShellDKGQ(element_manager: ElementManager) -> None:
    """测试DKGQ壳单元的数据处理"""
    # 创建ShellDKGQ单元
    cmd = "element"
    args = ("ShellDKGQ", 4, *[13, 14, 15, 16], 202)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 4 in element_manager.elements
    element_data = element_manager.elements[4]
    assert element_data["eleType"] == "ShellDKGQ"
    assert element_data["eleTag"] == 4
    assert element_data["eleNodes"] == [13, 14, 15, 16]
    assert element_data["secTag"] == 202


def test_handle_ShellDKGT(element_manager: ElementManager) -> None:
    """测试DKGT三角形壳单元的数据处理"""
    # 创建ShellDKGT单元
    cmd = "element"
    args = ("ShellDKGT", 5, *[17, 18, 19], 203)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 5 in element_manager.elements
    element_data = element_manager.elements[5]
    assert element_data["eleType"] == "ShellDKGT"
    assert element_data["eleTag"] == 5
    assert element_data["eleNodes"] == [17, 18, 19]
    assert element_data["secTag"] == 203


def test_handle_ShellNLDKGQ(element_manager: ElementManager) -> None:
    """测试非线性DKGQ壳单元的数据处理"""
    # 创建ShellNLDKGQ单元
    cmd = "element"
    args = ("ShellNLDKGQ", 6, *[20, 21, 22, 23], 204)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 6 in element_manager.elements
    element_data = element_manager.elements[6]
    assert element_data["eleType"] == "ShellNLDKGQ"
    assert element_data["eleTag"] == 6
    assert element_data["eleNodes"] == [20, 21, 22, 23]
    assert element_data["secTag"] == 204


def test_handle_ShellNLDKGT(element_manager: ElementManager) -> None:
    """测试非线性DKGT三角形壳单元的数据处理"""
    # 创建ShellNLDKGT单元
    cmd = "element"
    args = ("ShellNLDKGT", 7, *[24, 25, 26], 205)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 7 in element_manager.elements
    element_data = element_manager.elements[7]
    assert element_data["eleType"] == "ShellNLDKGT"
    assert element_data["eleTag"] == 7
    assert element_data["eleNodes"] == [24, 25, 26]
    assert element_data["secTag"] == 205


def test_handle_ShellNL(element_manager: ElementManager) -> None:
    """测试ShellNL壳单元的数据处理"""
    # 创建ShellNL单元
    cmd = "element"
    args = ("ShellNL", 8, *[27, 28, 29, 30, 31, 32, 33, 34, 35], 206)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 8 in element_manager.elements
    element_data = element_manager.elements[8]
    assert element_data["eleType"] == "ShellNL"
    assert element_data["eleTag"] == 8
    assert element_data["eleNodes"] == [27, 28, 29, 30, 31, 32, 33, 34, 35]
    assert element_data["secTag"] == 206


def test_handle_bbarQuad(element_manager: ElementManager) -> None:
    """测试bbarQuad平面应变四边形单元的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # 创建bbarQuad单元
    cmd = "element"
    args = ("bbarQuad", 9, *[36, 37, 38, 39], 0.2, 301)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 9 in element_manager.elements
    element_data = element_manager.elements[9]
    assert element_data["eleType"] == "bbarQuad"
    assert element_data["eleTag"] == 9
    assert element_data["eleNodes"] == [36, 37, 38, 39]
    assert element_data["thick"] == 0.2
    assert element_data["matTag"] == 301


def test_handle_enhancedQuad(element_manager: ElementManager) -> None:
    """测试enhancedQuad增强应变四边形单元的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # 创建enhancedQuad单元
    cmd = "element"
    args = ("enhancedQuad", 10, *[40, 41, 42, 43], 0.25, "PlaneStress", 302)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 10 in element_manager.elements
    element_data = element_manager.elements[10]
    assert element_data["eleType"] == "enhancedQuad"
    assert element_data["eleTag"] == 10
    assert element_data["eleNodes"] == [40, 41, 42, 43]
    assert element_data["thick"] == 0.25
    assert element_data["type"] == "PlaneStress"
    assert element_data["matTag"] == 302


def test_handle_SSPquad(element_manager: ElementManager) -> None:
    """测试SSPquad稳定单点积分四边形单元的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # 创建SSPquad单元
    cmd = "element"
    args = ("SSPquad", 11, *[44, 45, 46, 47], 303, "PlaneStrain", 0.3)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 11 in element_manager.elements
    element_data = element_manager.elements[11]
    assert element_data["eleType"] == "SSPquad"
    assert element_data["eleTag"] == 11
    assert element_data["eleNodes"] == [44, 45, 46, 47]
    assert element_data["matTag"] == 303
    assert element_data["type"] == "PlaneStrain"
    assert element_data["thick"] == 0.3


def test_handle_SSPquad_with_options(element_manager: ElementManager) -> None:
    """测试带选项的SSPquad稳定单点积分四边形单元的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # 创建带选项的SSPquad单元
    cmd = "element"
    args = ("SSPquad", 12, *[48, 49, 50, 51], 304, "PlaneStress", 0.35, "b1", 0.1, "b2", 0.2)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 12 in element_manager.elements
    element_data = element_manager.elements[12]
    assert element_data["eleType"] == "SSPquad"
    assert element_data["eleTag"] == 12
    assert element_data["eleNodes"] == [48, 49, 50, 51]
    assert element_data["matTag"] == 304
    assert element_data["type"] == "PlaneStress"
    assert element_data["thick"] == 0.35
    assert element_data["b1"] == 0.1
    assert element_data["b2"] == 0.2


def test_handle_MVLEM_3D(element_manager: ElementManager) -> None:
    """测试MVLEM_3D三维多竖直线单元的数据处理"""
    # 创建MVLEM_3D单元
    cmd = "element"
    args = (
        "MVLEM_3D", 13, *[52, 53, 54, 55], 3, 
        "-thick", *[0.2, 0.2, 0.2], 
        "-width", *[0.5, 0.5, 0.5], 
        "-rho", *[0.01, 0.01, 0.01], 
        "-matConcrete", *[401, 402, 403], 
        "-matSteel", *[501, 502, 503], 
        "-matShear", 601, 
        "-CoR", 0.4, 
        "-ThickMod", 0.63, 
        "-Poisson", 0.25, 
        "-Density", 2400.0
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 13 in element_manager.elements
    element_data = element_manager.elements[13]
    assert element_data["eleType"] == "MVLEM_3D"
    assert element_data["eleTag"] == 13
    assert element_data["eleNodes"] == [52, 53, 54, 55]
    assert element_data["m"] == 3
    assert element_data["thick"] == [0.2, 0.2, 0.2]
    assert element_data["widths"] == [0.5, 0.5, 0.5]
    assert element_data["rho"] == [0.01, 0.01, 0.01]
    assert element_data["matConcreteTags"] == [401, 402, 403]
    assert element_data["matSteelTags"] == [501, 502, 503]
    assert element_data["matShearTag"] == 601
    assert element_data["c"] == 0.4
    assert element_data["tMod"] == 0.63
    assert element_data["Nu"] == 0.25
    assert element_data["Dens"] == 2400.0


def test_handle_SFI_MVLEM_3D(element_manager: ElementManager) -> None:
    """测试SFI_MVLEM_3D三维剪切-弯曲相互作用单元的数据处理"""
    # 创建SFI_MVLEM_3D单元
    cmd = "element"
    args = (
        "SFI_MVLEM_3D", 14, *[56, 57, 58, 59], 4, 
        "-thick", *[0.25, 0.25, 0.25, 0.25], 
        "-width", *[0.4, 0.4, 0.4, 0.4], 
        "-mat", *[701, 702, 703, 704], 
        "-CoR", 0.5, 
        "-ThickMod", 0.7, 
        "-Poisson", 0.3, 
        "-Density", 2500.0
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 14 in element_manager.elements
    element_data = element_manager.elements[14]
    assert element_data["eleType"] == "SFI_MVLEM_3D"
    assert element_data["eleTag"] == 14
    assert element_data["eleNodes"] == [56, 57, 58, 59]
    assert element_data["m"] == 4
    assert element_data["thicks"] == [0.25, 0.25, 0.25, 0.25]
    assert element_data["widths"] == [0.4, 0.4, 0.4, 0.4]
    assert element_data["matTags"] == [701, 702, 703, 704]
    assert element_data["c"] == 0.5
    assert element_data["tMod"] == 0.7
    assert element_data["Nu"] == 0.3
    assert element_data["Dens"] == 2500.0


def test_handle_unknown_Quadrilateral(element_manager: ElementManager) -> None:
    """测试处理未知的四边形单元"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # 创建未知类型的四边形单元
    cmd = "element"
    args = ("customQuad", 15, *[60, 61, 62, 63], 0.3, "PlaneStress", 801)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 15 in element_manager.elements
    element_data = element_manager.elements[15]
    assert element_data["eleType"] == "customQuad"
    assert element_data["eleTag"] == 15
    assert "args" in element_data  # 未知元素应该将额外参数保存在args中
