import openseespy.opensees as ops
import pytest

from opsparser import ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return ElementManager()


def test_handle_elasticBeamColumn_2D(element_manager: ElementManager) -> None:
    """测试2D elasticBeamColumn元素的数据处理(直接参数形式)"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # 使用直接参数的情况 (command_type=2)
    cmd = "element"
    args = ("elasticBeamColumn", 1, *[1, 2], 100.0, 29000.0, 1000.0, 200)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager.elements
    element_data = element_manager.elements[1]
    assert element_data["eleType"] == "elasticBeamColumn"
    assert element_data["eleTag"] == 1
    assert element_data["eleNodes"] == [1, 2]
    assert element_data["Area"] == 100.0
    assert element_data["E_mod"] == 29000.0
    assert element_data["Iz"] == 1000.0
    assert element_data["transfTag"] == 200


def test_handle_elasticBeamColumn_2D_with_options(element_manager: ElementManager) -> None:
    """测试带选项的2D elasticBeamColumn元素的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # 使用带选项的情况
    cmd = "element"
    args = ("elasticBeamColumn", 2, *[3, 4], 120.0, 29000.0, 1200.0, 201, "-mass", 0.5, "-cMass", "-release", 1)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 2 in element_manager.elements
    element_data = element_manager.elements[2]
    assert element_data["eleType"] == "elasticBeamColumn"
    assert element_data["eleTag"] == 2
    assert element_data["eleNodes"] == [3, 4]
    assert element_data["Area"] == 120.0
    assert element_data["E_mod"] == 29000.0
    assert element_data["Iz"] == 1200.0
    assert element_data["transfTag"] == 201
    assert element_data["massDens"] == 0.5
    assert "cMass" in element_data
    assert element_data["releaseCode"] == 1


def test_handle_elasticBeamColumn_3D(element_manager: ElementManager) -> None:
    """测试3D elasticBeamColumn元素的数据处理"""
    # 带3D参数的情况(command_type=2)
    cmd = "element"
    args = ("elasticBeamColumn", 3, *[5, 6], 150.0, 29000.0, 11500.0, 1000.0, 2000.0, 1500.0, 202)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 3 in element_manager.elements
    element_data = element_manager.elements[3]
    assert element_data["eleType"] == "elasticBeamColumn"
    assert element_data["eleTag"] == 3
    assert element_data["eleNodes"] == [5, 6]
    assert element_data["Area"] == 150.0
    assert element_data["E_mod"] == 29000.0
    assert element_data["G_mod"] == 11500.0
    assert element_data["Jxx"] == 1000.0
    assert element_data["Iy"] == 2000.0
    assert element_data["Iz"] == 1500.0
    assert element_data["transfTag"] == 202


def test_handle_elasticBeamColumn_with_section(element_manager: ElementManager) -> None:
    """测试使用截面的elasticBeamColumn元素的数据处理(secTag形式)"""
    # 设置模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    # 使用截面标签的情况 (command_type=1)
    cmd = "element"
    args = ("elasticBeamColumn", 4, *[7, 8], 501, 203)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 4 in element_manager.elements
    element_data = element_manager.elements[4]
    assert element_data["eleType"] == "elasticBeamColumn"
    assert element_data["eleTag"] == 4
    assert element_data["eleNodes"] == [7, 8]
    assert element_data["secTag"] == 501
    assert element_data["transfTag"] == 203


def test_handle_ModElasticBeam2d(element_manager: ElementManager) -> None:
    """测试ModElasticBeam2d元素的数据处理"""
    cmd = "element"
    args = ("ModElasticBeam2d", 5, *[9, 10], 100.0, 29000.0, 1000.0, 0.8, 0.9, 0.7, 204)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 5 in element_manager.elements
    element_data = element_manager.elements[5]
    assert element_data["eleType"] == "ModElasticBeam2d"
    assert element_data["eleTag"] == 5
    assert element_data["eleNodes"] == [9, 10]
    assert element_data["Area"] == 100.0
    assert element_data["E_mod"] == 29000.0
    assert element_data["Iz"] == 1000.0
    assert element_data["K11"] == 0.8
    assert element_data["K33"] == 0.9
    assert element_data["K44"] == 0.7
    assert element_data["transfTag"] == 204


def test_handle_ModElasticBeam2d_with_options(element_manager: ElementManager) -> None:
    """测试带选项的ModElasticBeam2d元素的数据处理"""
    cmd = "element"
    args = ("ModElasticBeam2d", 6, *[11, 12], 120.0, 29000.0, 1200.0, 0.85, 0.95, 0.75, 205, "-mass", 0.6, "-cMass")
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 6 in element_manager.elements
    element_data = element_manager.elements[6]
    assert element_data["eleType"] == "ModElasticBeam2d"
    assert element_data["eleTag"] == 6
    assert element_data["eleNodes"] == [11, 12]
    assert element_data["Area"] == 120.0
    assert element_data["E_mod"] == 29000.0
    assert element_data["Iz"] == 1200.0
    assert element_data["K11"] == 0.85
    assert element_data["K33"] == 0.95
    assert element_data["K44"] == 0.75
    assert element_data["transfTag"] == 205
    assert element_data["massDens"] == 0.6


def test_handle_ElasticTimoshenkoBeam_2D(element_manager: ElementManager) -> None:
    """测试2D ElasticTimoshenkoBeam元素的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    cmd = "element"
    args = ("ElasticTimoshenkoBeam", 7, *[13, 14], 29000.0, 11500.0, 130.0, 1400.0, 65.0, 205)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 7 in element_manager.elements
    element_data = element_manager.elements[7]
    assert element_data["eleType"] == "ElasticTimoshenkoBeam"
    assert element_data["eleTag"] == 7
    assert element_data["eleNodes"] == [13, 14]
    assert element_data["E_mod"] == 29000.0
    assert element_data["G_mod"] == 11500.0
    assert element_data["Area"] == 130.0
    assert element_data["Iz"] == 1400.0
    assert element_data["Avy"] == 65.0
    assert element_data["transfTag"] == 205


def test_handle_ElasticTimoshenkoBeam_3D(element_manager: ElementManager) -> None:
    """测试3D ElasticTimoshenkoBeam元素的数据处理"""
    cmd = "element"
    args = ("ElasticTimoshenkoBeam", 8, *[15, 16], 29000.0, 11500.0, 120.0, 1000.0, 2000.0, 1500.0, 60.0, 60.0, 207)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 8 in element_manager.elements
    element_data = element_manager.elements[8]
    assert element_data["eleType"] == "ElasticTimoshenkoBeam"
    assert element_data["eleTag"] == 8
    assert element_data["eleNodes"] == [15, 16]
    assert element_data["E_mod"] == 29000.0
    assert element_data["G_mod"] == 11500.0
    assert element_data["Area"] == 120.0
    assert element_data["Jxx"] == 1000.0
    assert element_data["Iy"] == 2000.0
    assert element_data["Iz"] == 1500.0
    assert element_data["Avy"] == 60.0
    assert element_data["Avz"] == 60.0
    assert element_data["transfTag"] == 207


def test_handle_ElasticTimoshenkoBeam_with_options(element_manager: ElementManager) -> None:
    """测试带选项的ElasticTimoshenkoBeam元素的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    cmd = "element"
    args = ("ElasticTimoshenkoBeam", 9, *[17, 18], 29000.0, 11500.0, 110.0, 900.0, 55.0, 208, "-mass", 0.6, "-cMass")
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 9 in element_manager.elements
    element_data = element_manager.elements[9]
    assert element_data["eleType"] == "ElasticTimoshenkoBeam"
    assert element_data["eleTag"] == 9
    assert element_data["eleNodes"] == [17, 18]
    assert element_data["E_mod"] == 29000.0
    assert element_data["G_mod"] == 11500.0
    assert element_data["Area"] == 110.0
    assert element_data["Iz"] == 900.0
    assert element_data["Avy"] == 55.0
    assert element_data["transfTag"] == 208
    assert element_data["massDens"] == 0.6
    assert "cMass" in element_data


def test_handle_dispBeamColumn(element_manager: ElementManager) -> None:
    """测试dispBeamColumn元素的数据处理"""
    cmd = "element"
    args = ("dispBeamColumn", 10, *[19, 20], 209, 301)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 10 in element_manager.elements
    element_data = element_manager.elements[10]
    assert element_data["eleType"] == "dispBeamColumn"
    assert element_data["eleTag"] == 10
    assert element_data["eleNodes"] == [19, 20]
    assert element_data["transfTag"] == 209
    assert element_data["integrationTag"] == 301


def test_handle_dispBeamColumn_with_options(element_manager: ElementManager) -> None:
    """测试带选项的dispBeamColumn元素的数据处理"""
    cmd = "element"
    args = ("dispBeamColumn", 11, *[21, 22], 210, 302, "-cMass", "-mass", 0.7)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 11 in element_manager.elements
    element_data = element_manager.elements[11]
    assert element_data["eleType"] == "dispBeamColumn"
    assert element_data["eleTag"] == 11
    assert element_data["eleNodes"] == [21, 22]
    assert element_data["transfTag"] == 210
    assert element_data["integrationTag"] == 302
    assert "cMass" in element_data
    assert element_data["mass"] == 0.7


def test_handle_forceBeamColumn(element_manager: ElementManager) -> None:
    """测试forceBeamColumn元素的数据处理"""
    cmd = "element"
    args = ("forceBeamColumn", 12, *[23, 24], 211, 303)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 12 in element_manager.elements
    element_data = element_manager.elements[12]
    assert element_data["eleType"] == "forceBeamColumn"
    assert element_data["eleTag"] == 12
    assert element_data["eleNodes"] == [23, 24]
    assert element_data["transfTag"] == 211
    assert element_data["integrationTag"] == 303


def test_handle_forceBeamColumn_with_options(element_manager: ElementManager) -> None:
    """测试带选项的forceBeamColumn元素的数据处理"""
    cmd = "element"
    args = ("forceBeamColumn", 13, *[25, 26], 212, 304, "-iter", 15, 1e-10, "-mass", 0.9)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 13 in element_manager.elements
    element_data = element_manager.elements[13]
    assert element_data["eleType"] == "forceBeamColumn"
    assert element_data["eleTag"] == 13
    assert element_data["eleNodes"] == [25, 26]
    assert element_data["transfTag"] == 212
    assert element_data["integrationTag"] == 304
    assert element_data["maxIter"] == 15
    assert element_data["tol"] == 1e-10
    assert element_data["mass"] == 0.9


def test_handle_nonlinearBeamColumn(element_manager: ElementManager) -> None:
    """测试nonlinearBeamColumn元素的数据处理"""
    cmd = "element"
    args = ("nonlinearBeamColumn", 14, *[27, 28], 5, 502, 213)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 14 in element_manager.elements
    element_data = element_manager.elements[14]
    assert element_data["eleType"] == "nonlinearBeamColumn"
    assert element_data["eleTag"] == 14
    assert element_data["eleNodes"] == [27, 28]
    assert element_data["numIntgrPts"] == 5
    assert element_data["secTag"] == 502
    assert element_data["transfTag"] == 213


def test_handle_nonlinearBeamColumn_with_options(element_manager: ElementManager) -> None:
    """测试带选项的nonlinearBeamColumn元素的数据处理"""
    cmd = "element"
    args = ("nonlinearBeamColumn", 15, *[29, 30], 7, 503, 214, "-iter", 20, 1e-8, "-mass", 1.0, "-integration", "NewtonCotes")
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 15 in element_manager.elements
    element_data = element_manager.elements[15]
    assert element_data["eleType"] == "nonlinearBeamColumn"
    assert element_data["eleTag"] == 15
    assert element_data["eleNodes"] == [29, 30]
    assert element_data["numIntgrPts"] == 7
    assert element_data["secTag"] == 503
    assert element_data["transfTag"] == 214
    assert element_data["maxIter"] == 20
    assert element_data["tol"] == 1e-8
    assert element_data["mass"] == 1.0
    assert element_data["intType"] == "NewtonCotes"


def test_handle_dispBeamColumnInt(element_manager: ElementManager) -> None:
    """测试dispBeamColumnInt元素的数据处理"""
    cmd = "element"
    args = ("dispBeamColumnInt", 16, *[31, 32], 5, 504, 215, 1.0)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 16 in element_manager.elements
    element_data = element_manager.elements[16]
    assert element_data["eleType"] == "dispBeamColumnInt"
    assert element_data["eleTag"] == 16
    assert element_data["eleNodes"] == [31, 32]
    assert element_data["numIntgrPts"] == 5
    assert element_data["secTag"] == 504
    assert element_data["transfTag"] == 215
    assert element_data["cRot"] == 1.0


def test_handle_dispBeamColumnInt_with_options(element_manager: ElementManager) -> None:
    """测试带选项的dispBeamColumnInt元素的数据处理"""
    cmd = "element"
    args = ("dispBeamColumnInt", 17, *[33, 34], 6, 505, 216, 1.0, "-mass", 1.1)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 17 in element_manager.elements
    element_data = element_manager.elements[17]
    assert element_data["eleType"] == "dispBeamColumnInt"
    assert element_data["eleTag"] == 17
    assert element_data["eleNodes"] == [33, 34]
    assert element_data["numIntgrPts"] == 6
    assert element_data["secTag"] == 505
    assert element_data["transfTag"] == 216
    assert element_data["cRot"] == 1.0
    assert element_data["massDens"] == 1.1


def test_handle_MVLEM(element_manager: ElementManager) -> None:
    """测试MVLEM元素的数据处理"""
    # 设置模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    cmd = "element"
    args = (
        "MVLEM", 18, 0.01, *[35, 36], 3, 0.4, 
        "-thick", *[0.1, 0.1, 0.1], 
        "-width", *[0.3, 0.4, 0.3], 
        "-rho", *[0.01, 0.02, 0.01], 
        "-matConcrete", *[601, 602, 603], 
        "-matSteel", *[701, 702, 703], 
        "-matShear", 801
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 18 in element_manager.elements
    element_data = element_manager.elements[18]
    assert element_data["eleType"] == "MVLEM"
    assert element_data["eleTag"] == 18
    assert element_data["Dens"] == 0.01
    assert element_data["eleNodes"] == [35, 36]
    assert element_data["m"] == 3
    assert element_data["c"] == 0.4
    assert element_data["thick"] == [0.1, 0.1, 0.1]
    assert element_data["widths"] == [0.3, 0.4, 0.3]
    assert element_data["rho"] == [0.01, 0.02, 0.01]
    assert element_data["matConcreteTags"] == [601, 602, 603]
    assert element_data["matSteelTags"] == [701, 702, 703]
    assert element_data["matShearTag"] == 801


def test_handle_SFI_MVLEM(element_manager: ElementManager) -> None:
    """测试SFI_MVLEM元素的数据处理"""
    # 设置模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    cmd = "element"
    args = (
        "SFI_MVLEM", 19, *[37, 38], 4, 0.5, 
        "-thick", *[0.15, 0.15, 0.15, 0.15], 
        "-width", *[0.25, 0.25, 0.25, 0.25], 
        "-mat", *[901, 902, 903, 904]
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 19 in element_manager.elements
    element_data = element_manager.elements[19]
    assert element_data["eleType"] == "SFI_MVLEM"
    assert element_data["eleTag"] == 19
    assert element_data["eleNodes"] == [37, 38]
    assert element_data["m"] == 4
    assert element_data["c"] == 0.5
    assert element_data["thick"] == [0.15, 0.15, 0.15, 0.15]
    assert element_data["widths"] == [0.25, 0.25, 0.25, 0.25]
    assert element_data["mat_tags"] == [901, 902, 903, 904]


def test_handle_Pipe_straight(element_manager: ElementManager) -> None:
    """测试直管Pipe元素的数据处理"""
    cmd = "element"
    args = ("Pipe", 20, *[39, 40], 1001, 1101)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 20 in element_manager.elements
    element_data = element_manager.elements[20]
    assert element_data["eleType"] == "Pipe"
    assert element_data["eleTag"] == 20
    assert element_data["eleNodes"] == [39, 40]
    assert element_data["pipeMatTag"] == 1001
    assert element_data["pipeSecTag"] == 1101


def test_handle_Pipe_with_options(element_manager: ElementManager) -> None:
    """测试带选项的Pipe元素的数据处理"""
    cmd = "element"
    args = ("Pipe", 21, *[41, 42], 1002, 1102, "-T0", 20.0, "-p", 10.0, "-noThermalLoad", "-noPressureLoad")
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 21 in element_manager.elements
    element_data = element_manager.elements[21]
    assert element_data["eleType"] == "Pipe"
    assert element_data["eleTag"] == 21
    assert element_data["eleNodes"] == [41, 42]
    assert element_data["pipeMatTag"] == 1002
    assert element_data["pipeSecTag"] == 1102
    assert element_data["T0"] == 20.0
    assert element_data["p"] == 10.0


def test_handle_Pipe_curved(element_manager: ElementManager) -> None:
    """测试曲管Pipe元素的数据处理"""
    cmd = "element"
    args = ("Pipe", 22, *[43, 44], 1003, 1103, 1.0, 1.0, 0.0, "-Ti", "-tolWall", 0.05)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 22 in element_manager.elements
    element_data = element_manager.elements[22]
    assert element_data["eleType"] == "Pipe"
    assert element_data["eleTag"] == 22
    assert element_data["eleNodes"] == [43, 44]
    assert element_data["pipeMatTag"] == 1003
    assert element_data["pipeSecTag"] == 1103
    assert element_data["xC"] == 1.0
    assert element_data["yC"] == 1.0
    assert element_data["zC"] == 0.0
    assert element_data["tolWall"] == 0.05


def test_handle_unknown_BeamColumn(element_manager: ElementManager) -> None:
    """测试处理未知的梁柱元素"""
    cmd = "element"
    args = ("customBeamColumn", 23, *[45, 46], 100.0, 29000.0, 1000.0, 217)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 23 in element_manager.elements
    element_data = element_manager.elements[23]
    assert element_data["eleType"] == "customBeamColumn"
    assert element_data["eleTag"] == 23
    assert "args" in element_data  # 未知元素应该将额外参数保存在args中
