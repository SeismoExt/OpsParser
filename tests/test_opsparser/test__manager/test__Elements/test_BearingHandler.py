import openseespy.opensees as ops
import pytest

from opsparser import ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return ElementManager()


def test_handle_elastomericBearingPlasticity_2D(element_manager: ElementManager) -> None:
    """测试2D elastomericBearingPlasticity支座元素的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    cmd = "element"
    args = ("elastomericBearingPlasticity", 1, *[1, 2], 1000.0, 10.0, 0.5, 0.2, 0.05, "-P", 101, "-Mz", 102)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager.elements
    element_data = element_manager.elements[1]
    assert element_data["eleType"] == "elastomericBearingPlasticity"
    assert element_data["eleTag"] == 1
    assert element_data["eleNodes"] == [1, 2]
    assert element_data["kInit"] == 1000.0
    assert element_data["qd"] == 10.0
    assert element_data["alpha1"] == 0.5
    assert element_data["alpha2"] == 0.2
    assert element_data["mu"] == 0.05
    assert element_data["PMatTag"] == 101
    assert element_data["MzMatTag"] == 102


def test_handle_elastomericBearingPlasticity_2D_with_options(element_manager: ElementManager) -> None:
    """测试带选项的2D elastomericBearingPlasticity支座元素的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    cmd = "element"
    args = ("elastomericBearingPlasticity", 2, *[3, 4], 1200.0, 12.0, 0.6, 0.3, 0.06, 
            "-P", 103, "-Mz", 104, "-orient", *[1, 0, 0, 0, 1, 0], 
            "-shearDist", 0.5, "-doRayleigh", "-mass", 1.5)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 2 in element_manager.elements
    element_data = element_manager.elements[2]
    assert element_data["eleType"] == "elastomericBearingPlasticity"
    assert element_data["eleTag"] == 2
    assert element_data["eleNodes"] == [3, 4]
    assert element_data["kInit"] == 1200.0
    assert element_data["qd"] == 12.0
    assert element_data["alpha1"] == 0.6
    assert element_data["alpha2"] == 0.3
    assert element_data["mu"] == 0.06
    assert element_data["PMatTag"] == 103
    assert element_data["MzMatTag"] == 104
    assert element_data["orientVals"] == [1, 0, 0, 0, 1, 0]
    assert element_data["sDratio"] == 0.5
    assert "doRayleigh" in element_data
    assert element_data["m"] == 1.5


def test_handle_elastomericBearingPlasticity_3D(element_manager: ElementManager) -> None:
    """测试3D elastomericBearingPlasticity支座元素的数据处理"""
    cmd = "element"
    args = ("elastomericBearingPlasticity", 3, *[5, 6], 1500.0, 15.0, 0.55, 0.25, 0.07, 
            "-P", 105, "-T", 106, "-My", 107, "-Mz", 108)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 3 in element_manager.elements
    element_data = element_manager.elements[3]
    assert element_data["eleType"] == "elastomericBearingPlasticity"
    assert element_data["eleTag"] == 3
    assert element_data["eleNodes"] == [5, 6]
    assert element_data["kInit"] == 1500.0
    assert element_data["qd"] == 15.0
    assert element_data["alpha1"] == 0.55
    assert element_data["alpha2"] == 0.25
    assert element_data["mu"] == 0.07
    assert element_data["PMatTag"] == 105
    assert element_data["TMatTag"] == 106
    assert element_data["MyMatTag"] == 107
    assert element_data["MzMatTag"] == 108


def test_handle_elastomericBearingBoucWen_2D(element_manager: ElementManager) -> None:
    """测试2D elastomericBearingBoucWen支座元素的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    cmd = "element"
    args = ("elastomericBearingBoucWen", 4, *[7, 8], 1800.0, 18.0, 0.65, 0.35, 0.08, 
            1.0, 0.5, 0.5, "-P", 109, "-Mz", 110)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 4 in element_manager.elements
    element_data = element_manager.elements[4]
    assert element_data["eleType"] == "elastomericBearingBoucWen"
    assert element_data["eleTag"] == 4
    assert element_data["eleNodes"] == [7, 8]
    assert element_data["kInit"] == 1800.0
    assert element_data["qd"] == 18.0
    assert element_data["alpha1"] == 0.65
    assert element_data["alpha2"] == 0.35
    assert element_data["mu"] == 0.08
    assert element_data["eta"] == 1.0
    assert element_data["beta"] == 0.5
    assert element_data["gamma"] == 0.5
    assert element_data["PMatTag"] == 109
    assert element_data["MzMatTag"] == 110


def test_handle_elastomericBearingBoucWen_3D(element_manager: ElementManager) -> None:
    """测试3D elastomericBearingBoucWen支座元素的数据处理"""
    cmd = "element"
    args = ("elastomericBearingBoucWen", 5, *[9, 10], 2000.0, 20.0, 0.7, 0.4, 0.1, 
            1.0, 0.6, 0.4, "-P", 111, "-T", 112, "-My", 113, "-Mz", 114)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 5 in element_manager.elements
    element_data = element_manager.elements[5]
    assert element_data["eleType"] == "elastomericBearingBoucWen"
    assert element_data["eleTag"] == 5
    assert element_data["eleNodes"] == [9, 10]
    assert element_data["kInit"] == 2000.0
    assert element_data["qd"] == 20.0
    assert element_data["alpha1"] == 0.7
    assert element_data["alpha2"] == 0.4
    assert element_data["mu"] == 0.1
    assert element_data["eta"] == 1.0
    assert element_data["beta"] == 0.6
    assert element_data["gamma"] == 0.4
    assert element_data["PMatTag"] == 111
    assert element_data["TMatTag"] == 112
    assert element_data["MyMatTag"] == 113
    assert element_data["MzMatTag"] == 114


def test_handle_flatSliderBearing_2D(element_manager: ElementManager) -> None:
    """测试2D flatSliderBearing支座元素的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    cmd = "element"
    args = ("flatSliderBearing", 6, *[11, 12], 201, 2200.0, "-P", 115, "-Mz", 116)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 6 in element_manager.elements
    element_data = element_manager.elements[6]
    assert element_data["eleType"] == "flatSliderBearing"
    assert element_data["eleTag"] == 6
    assert element_data["eleNodes"] == [11, 12]
    assert element_data["frnMdlTag"] == 201
    assert element_data["kInit"] == 2200.0
    assert element_data["PMatTag"] == 115
    assert element_data["MzMatTag"] == 116


def test_handle_singleFPBearing_3D(element_manager: ElementManager) -> None:
    """测试3D singleFPBearing支座元素的数据处理"""
    cmd = "element"
    args = ("singleFPBearing", 7, *[13, 14], 202, 1.0, 2500.0, 
            "-P", 117, "-T", 118, "-My", 119, "-Mz", 120, 
            "-orient", *[1, 0, 0, 0, 1, 0, 0, 0, 1], 
            "-shearDist", 0.0, "-doRayleigh", "-mass", 2.0, 
            "-iter", 25, 1.0e-10)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 7 in element_manager.elements
    element_data = element_manager.elements[7]
    assert element_data["eleType"] == "singleFPBearing"
    assert element_data["eleTag"] == 7
    assert element_data["eleNodes"] == [13, 14]
    assert element_data["frnMdlTag"] == 202
    assert element_data["Reff"] == 1.0
    assert element_data["kInit"] == 2500.0
    assert element_data["PMatTag"] == 117
    assert element_data["TMatTag"] == 118
    assert element_data["MyMatTag"] == 119
    assert element_data["MzMatTag"] == 120
    assert element_data["orientVals"] == [1, 0, 0, 0, 1, 0, 0, 0, 1]
    assert element_data["sDratio"] == 0.0
    assert "doRayleigh" in element_data
    assert element_data["m"] == 2.0
    assert element_data["maxIter"] == 25
    assert element_data["tol"] == 1.0e-10


def test_handle_TFP(element_manager: ElementManager) -> None:
    """测试TFP (Triple Friction Pendulum)支座元素的数据处理"""
    cmd = "element"
    args = ("TFP", 8, *[15, 16], 
            2.0, 2.1, 2.2, 2.3,  # R1, R2, R3, R4
            0.4, 0.41, 0.42, 0.43,  # Db1, Db2, Db3, Db4
            0.1, 0.11, 0.12, 0.13,  # d1, d2, d3, d4
            0.05, 0.06, 0.07, 0.08,  # mu1, mu2, mu3, mu4
            0.2, 0.21, 0.22, 0.23,  # h1, h2, h3, h4
            0.5, 1000.0)  # H0, colLoad
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 8 in element_manager.elements
    element_data = element_manager.elements[8]
    assert element_data["eleType"] == "TFP"
    assert element_data["eleTag"] == 8
    assert element_data["eleNodes"] == [15, 16]
    assert element_data["R1"] == 2.0
    assert element_data["R2"] == 2.1
    assert element_data["R3"] == 2.2
    assert element_data["R4"] == 2.3
    assert element_data["Db1"] == 0.4
    assert element_data["Db2"] == 0.41
    assert element_data["Db3"] == 0.42
    assert element_data["Db4"] == 0.43
    assert element_data["d1"] == 0.1
    assert element_data["d2"] == 0.11
    assert element_data["d3"] == 0.12
    assert element_data["d4"] == 0.13
    assert element_data["mu1"] == 0.05
    assert element_data["mu2"] == 0.06
    assert element_data["mu3"] == 0.07
    assert element_data["mu4"] == 0.08
    assert element_data["h1"] == 0.2
    assert element_data["h2"] == 0.21
    assert element_data["h3"] == 0.22
    assert element_data["h4"] == 0.23
    assert element_data["H0"] == 0.5
    assert element_data["colLoad"] == 1000.0


def test_handle_multipleShearSpring(element_manager: ElementManager) -> None:
    """测试multipleShearSpring支座元素的数据处理"""
    cmd = "element"
    args = ("multipleShearSpring", 9, *[17, 18], 8, "-mat", 121, "-lim", 0.01, 
            "-orient", *[1, 0, 0, 0, 1, 0], "-mass", 1.8)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 9 in element_manager.elements
    element_data = element_manager.elements[9]
    assert element_data["eleType"] == "multipleShearSpring"
    assert element_data["eleTag"] == 9
    assert element_data["eleNodes"] == [17, 18]
    assert element_data["nSpring"] == 8
    assert element_data["matTag"] == 121
    assert element_data["lim"] == 0.01
    assert element_data["orientVals"] == [1, 0, 0, 0, 1, 0]
    assert element_data["mass"] == 1.8


def test_handle_KikuchiBearing(element_manager: ElementManager) -> None:
    """测试KikuchiBearing支座元素的数据处理"""
    cmd = "element"
    args = ("KikuchiBearing", 10, *[19, 20], "-shape", "round", "-size", 0.5, 0.1, 
            "-nMSS", 10, "-matMSS", 122, "-nMNS", 4,
            "-matMNS", 123)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 10 in element_manager.elements
    element_data = element_manager.elements[10]
    assert element_data["eleType"] == "KikuchiBearing"
    assert element_data["eleTag"] == 10
    assert element_data["eleNodes"] == [19, 20]
    assert element_data["shape"] == "round"
    assert element_data["size"] == 0.5
    assert element_data["totalRubber"] == 0.1
    assert element_data["nMSS"] == 10
    assert element_data["matMSSTag"] == 122
    assert element_data["nMNS"] == 4
    assert element_data["matMNSTag"] == 123


def test_handle_KikuchiBearing_with_options(element_manager: ElementManager) -> None:
    """测试带选项的KikuchiBearing支座元素的数据处理"""
    cmd = "element"
    args = ("KikuchiBearing", 11, *[21, 22], "-shape", "square", "-size", 0.6, 0.12,
            "-totalHeight", 0.2, "-nMSS", 12, "-matMSS", 124, 
            "-limDisp", 0.05, "-nMNS", 6, "-matMNS", 125, "-lambda", 0.7,
            "-orient", *[1, 0, 0, 0, 1, 0], "-mass", 2.0, "-noPDInput", "-noTilt",
            "-adjustPDOutput", 0.4, 0.6, "-doBalance", 1.0e-3, 1.0e-4, 100)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 11 in element_manager.elements
    element_data = element_manager.elements[11]
    assert element_data["eleType"] == "KikuchiBearing"
    assert element_data["eleTag"] == 11
    assert element_data["eleNodes"] == [21, 22]
    assert element_data["shape"] == "square"
    assert element_data["size"] == 0.6
    assert element_data["totalRubber"] == 0.12
    assert element_data["totalHeight"] == 0.2
    assert element_data["nMSS"] == 12
    assert element_data["matMSSTag"] == 124
    assert element_data["limDisp"] == 0.05
    assert element_data["nMNS"] == 6
    assert element_data["matMNSTag"] == 125
    assert element_data["lambda"] == 0.7
    assert element_data["vecx"] == [1, 0, 0]
    assert element_data["vecyp"] == [0, 1, 0]
    assert element_data["m"] == 2.0
    assert "noPDInput" in element_data
    assert "noTilt" in element_data
    assert element_data["ci"] == 0.4
    assert element_data["cj"] == 0.6
    assert element_data["limFo"] == 1.0e-3
    assert element_data["limFi"] == 1.0e-4
    assert element_data["nIter"] == 100


def test_handle_YamamotoBiaxialHDR(element_manager: ElementManager) -> None:
    """测试YamamotoBiaxialHDR支座元素的数据处理"""
    cmd = "element"
    args = ("YamamotoBiaxialHDR", 12, *[23, 24], 1, 0.4, 0.1, 0.05)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 12 in element_manager.elements
    element_data = element_manager.elements[12]
    assert element_data["eleType"] == "YamamotoBiaxialHDR"
    assert element_data["eleTag"] == 12
    assert element_data["eleNodes"] == [23, 24]
    assert element_data["Tp"] == 1
    assert element_data["DDo"] == 0.4
    assert element_data["DDi"] == 0.1
    assert element_data["Hr"] == 0.05


def test_handle_ElastomericX(element_manager: ElementManager) -> None:
    """测试ElastomericX支座元素的数据处理"""
    cmd = "element"
    args = ("ElastomericX", 13, *[25, 26], 100.0, 0.1, 0.7, 2000.0, 0.1, 0.4, 0.01, 0.02, 5)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 13 in element_manager.elements
    element_data = element_manager.elements[13]
    assert element_data["eleType"] == "ElastomericX"
    assert element_data["eleTag"] == 13
    assert element_data["eleNodes"] == [25, 26]
    assert element_data["Fy"] == 100.0
    assert element_data["alpha"] == 0.1
    assert element_data["Gr"] == 0.7
    assert element_data["Kbulk"] == 2000.0
    assert element_data["D1"] == 0.1
    assert element_data["D2"] == 0.4
    assert element_data["ts"] == 0.01
    assert element_data["tr"] == 0.02
    assert element_data["n"] == 5


def test_handle_ElastomericX_with_options(element_manager: ElementManager) -> None:
    """测试带选项的ElastomericX支座元素的数据处理"""
    cmd = "element"
    args = ("ElastomericX", 14, *[27, 28], 120.0, 0.15, 0.8, 2200.0, 0.15, 0.45, 0.015, 0.025, 6,
            "orient", *[1, 0, 0, 0, 1, 0], "kc", 5.0, "PhiM", 0.5, "ac", 1.0, "sDratio", 0.5,
            "m", 1.0, "cd", 0.01, "tc", 0.05, "tag1", 1, "tag2", 1, "tag3", 1, "tag4", 1)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 14 in element_manager.elements
    element_data = element_manager.elements[14]
    assert element_data["eleType"] == "ElastomericX"
    assert element_data["eleTag"] == 14
    assert element_data["eleNodes"] == [27, 28]
    assert element_data["Fy"] == 120.0
    assert element_data["alpha"] == 0.15
    assert element_data["Gr"] == 0.8
    assert element_data["Kbulk"] == 2200.0
    assert element_data["D1"] == 0.15
    assert element_data["D2"] == 0.45
    assert element_data["ts"] == 0.015
    assert element_data["tr"] == 0.025
    assert element_data["n"] == 6
    assert element_data["orientVals"] == [1, 0, 0, 0, 1, 0]
    assert element_data["kc"] == 5.0
    assert element_data["PhiM"] == 0.5
    assert element_data["ac"] == 1.0
    assert element_data["sDratio"] == 0.5
    assert element_data["m"] == 1.0
    assert element_data["cd"] == 0.01
    assert element_data["tc"] == 0.05
    assert element_data["tag1"] == 1
    assert element_data["tag2"] == 1
    assert element_data["tag3"] == 1
    assert element_data["tag4"] == 1


def test_handle_LeadRubberX(element_manager: ElementManager) -> None:
    """测试LeadRubberX支座元素的数据处理"""
    cmd = "element"
    args = ("LeadRubberX", 15, *[29, 30], 150.0, 0.2, 0.9, 2500.0, 0.2, 0.5, 0.02, 0.03, 7)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 15 in element_manager.elements
    element_data = element_manager.elements[15]
    assert element_data["eleType"] == "LeadRubberX"
    assert element_data["eleTag"] == 15
    assert element_data["eleNodes"] == [29, 30]
    assert element_data["Fy"] == 150.0
    assert element_data["alpha"] == 0.2
    assert element_data["Gr"] == 0.9
    assert element_data["Kbulk"] == 2500.0
    assert element_data["D1"] == 0.2
    assert element_data["D2"] == 0.5
    assert element_data["ts"] == 0.02
    assert element_data["tr"] == 0.03
    assert element_data["n"] == 7


def test_handle_HDR(element_manager: ElementManager) -> None:
    """测试HDR支座元素的数据处理"""
    cmd = "element"
    args = ("HDR", 16, *[31, 32], 1.0, 3000.0, 0.25, 0.55, 0.025, 0.035, 8,
            0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 16 in element_manager.elements
    element_data = element_manager.elements[16]
    assert element_data["eleType"] == "HDR"
    assert element_data["eleTag"] == 16
    assert element_data["eleNodes"] == [31, 32]
    assert element_data["Gr"] == 1.0
    assert element_data["Kbulk"] == 3000.0
    assert element_data["D1"] == 0.25
    assert element_data["D2"] == 0.55
    assert element_data["ts"] == 0.025
    assert element_data["tr"] == 0.035
    assert element_data["n"] == 8
    assert element_data["a1"] == 0.1
    assert element_data["a2"] == 0.2
    assert element_data["a3"] == 0.3
    assert element_data["b1"] == 0.4
    assert element_data["b2"] == 0.5
    assert element_data["b3"] == 0.6
    assert element_data["c1"] == 0.7
    assert element_data["c2"] == 0.8
    assert element_data["c3"] == 0.9
    assert element_data["c4"] == 1.0


def test_handle_RJWatsonEqsBearing_2D(element_manager: ElementManager) -> None:
    """测试2D RJWatsonEqsBearing支座元素的数据处理"""
    # 设置2D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)

    cmd = "element"
    args = ("RJWatsonEqsBearing", 17, *[33, 34], 203, 3000.0, "-P", 126, "-Vy", 127, "-Mz", 128)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 17 in element_manager.elements
    element_data = element_manager.elements[17]
    assert element_data["eleType"] == "RJWatsonEqsBearing"
    assert element_data["eleTag"] == 17
    assert element_data["eleNodes"] == [33, 34]
    assert element_data["frnMdlTag"] == 203
    assert element_data["kInit"] == 3000.0
    assert element_data["PMatTag"] == 126
    assert element_data["VyMatTag"] == 127
    assert element_data["MzMatTag"] == 128


def test_handle_RJWatsonEqsBearing_3D(element_manager: ElementManager) -> None:
    """测试3D RJWatsonEqsBearing支座元素的数据处理"""
    # 恢复3D模型环境
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)

    cmd = "element"
    args = ("RJWatsonEqsBearing", 18, *[35, 36], 204, 3200.0, "-P", 129, "-Vy", 130,
            "-Vz", 131, "-T", 132, "-My", 133, "-Mz", 134)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 18 in element_manager.elements
    element_data = element_manager.elements[18]
    assert element_data["eleType"] == "RJWatsonEqsBearing"
    assert element_data["eleTag"] == 18
    assert element_data["eleNodes"] == [35, 36]
    assert element_data["frnMdlTag"] == 204
    assert element_data["kInit"] == 3200.0
    assert element_data["PMatTag"] == 129
    assert element_data["VyMatTag"] == 130
    assert element_data["VzMatTag"] == 131
    assert element_data["TMatTag"] == 132
    assert element_data["MyMatTag"] == 133
    assert element_data["MzMatTag"] == 134


def test_handle_FPBearingPTV(element_manager: ElementManager) -> None:
    """测试FPBearingPTV支座元素的数据处理"""
    cmd = "element"
    args = ("FPBearingPTV", 19, *[37, 38], 0.05, 1, 10.0, 1, 1.41e-5, 50.0,
            1, 0.5, 1.0, 0.1, 3500.0, 135, 136, 137, 138, 1, 0, 0, 0, 1, 0,
            0.0, 0, 1.0, 20, 1.0e-10, 1)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 19 in element_manager.elements
    element_data = element_manager.elements[19]
    assert element_data["eleType"] == "FPBearingPTV"
    assert element_data["eleTag"] == 19
    assert element_data["eleNodes"] == [37, 38]
    assert element_data["MuRef"] == 0.05
    assert element_data["IsPressureDependent"] == 1
    assert element_data["pRef"] == 10.0
    assert element_data["IsTemperatureDependent"] == 1
    assert element_data["Diffusivity"] == 1.41e-5
    assert element_data["Conductivity"] == 50.0
    assert element_data["IsVelocityDependent"] == 1
    assert element_data["rateParameter"] == 0.5
    assert element_data["ReffectiveFP"] == 1.0
    assert element_data["Radius_Contact"] == 0.1
    assert element_data["kInitial"] == 3500.0
    assert element_data["theMaterialA"] == 135
    assert element_data["theMaterialB"] == 136
    assert element_data["theMaterialC"] == 137
    assert element_data["theMaterialD"] == 138


def test_handle_TripleFrictionPendulum(element_manager: ElementManager) -> None:
    """测试TripleFrictionPendulum支座元素的数据处理"""
    cmd = "element"
    args = ("TripleFrictionPendulum", 20, *[39, 40], 205, 206, 207, 140, 141, 142, 143,
            1.1, 1.2, 1.3, 0.11, 0.12, 0.13, 100.0, 0.01, 0.1, 0.01, 1.0e-10)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 20 in element_manager.elements
    element_data = element_manager.elements[20]
    assert element_data["eleType"] == "TripleFrictionPendulum"
    assert element_data["eleTag"] == 20
    assert element_data["eleNodes"] == [39, 40]
    assert element_data["frnTag1"] == 205
    assert element_data["frnTag2"] == 206
    assert element_data["frnTag3"] == 207
    assert element_data["vertMatTag"] == 140
    assert element_data["rotZMatTag"] == 141
    assert element_data["rotXMatTag"] == 142
    assert element_data["rotYMatTag"] == 143
    assert element_data["L1"] == 1.1
    assert element_data["L2"] == 1.2
    assert element_data["L3"] == 1.3
    assert element_data["d1"] == 0.11
    assert element_data["d2"] == 0.12
    assert element_data["d3"] == 0.13
    assert element_data["W"] == 100.0
    assert element_data["uy"] == 0.01
    assert element_data["kvt"] == 0.1
    assert element_data["minFv"] == 0.01
    assert element_data["tol"] == 1.0e-10


def test_handle_unknown_bearing(element_manager: ElementManager) -> None:
    """测试处理未知的支座元素"""
    cmd = "element"
    args = ("customBearing", 21, *[41, 42], 1000.0, 10.0, 0.5, 0.2, 0.05)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 21 in element_manager.elements
    element_data = element_manager.elements[21]
    assert element_data["eleType"] == "customBearing"
    assert element_data["eleTag"] == 21
    assert "args" in element_data  # 未知元素应该将额外参数保存在args中
