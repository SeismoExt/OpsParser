import openseespy.opensees as ops
import pytest

from opsparser import ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return ElementManager()


def test_handle_beamColumnJoint(element_manager: ElementManager) -> None:
    """测试beamColumnJoint元素的数据处理"""
    # 使用基本参数
    cmd = "element"
    args = (
        "beamColumnJoint", 1, *[1, 2, 3, 4],
        101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager.elements
    element_data = element_manager.elements[1]
    assert element_data["eleType"] == "beamColumnJoint"
    assert element_data["eleTag"] == 1
    assert element_data["eleNodes"] == [1, 2, 3, 4]
    assert element_data["Mat1Tag"] == 101
    assert element_data["Mat2Tag"] == 102
    assert element_data["Mat3Tag"] == 103
    assert element_data["Mat4Tag"] == 104
    assert element_data["Mat5Tag"] == 105
    assert element_data["Mat6Tag"] == 106
    assert element_data["Mat7Tag"] == 107
    assert element_data["Mat8Tag"] == 108
    assert element_data["Mat9Tag"] == 109
    assert element_data["Mat10Tag"] == 110
    assert element_data["Mat11Tag"] == 111
    assert element_data["Mat12Tag"] == 112
    assert element_data["Mat13Tag"] == 113


def test_handle_beamColumnJoint_with_options(element_manager: ElementManager) -> None:
    """测试带选项的beamColumnJoint元素的数据处理"""
    # 使用带选项的情况
    cmd = "element"
    args = (
        "beamColumnJoint", 2, *[5, 6, 7, 8], 
        201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213,
        0.8, 0.9  # eleHeightFac和eleWidthFac
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 2 in element_manager.elements
    element_data = element_manager.elements[2]
    assert element_data["eleType"] == "beamColumnJoint"
    assert element_data["eleTag"] == 2
    assert element_data["eleNodes"] == [5, 6, 7, 8]
    assert element_data["Mat1Tag"] == 201
    assert element_data["Mat2Tag"] == 202
    assert element_data["Mat3Tag"] == 203
    assert element_data["Mat4Tag"] == 204
    assert element_data["Mat5Tag"] == 205
    assert element_data["Mat6Tag"] == 206
    assert element_data["Mat7Tag"] == 207
    assert element_data["Mat8Tag"] == 208
    assert element_data["Mat9Tag"] == 209
    assert element_data["Mat10Tag"] == 210
    assert element_data["Mat11Tag"] == 211
    assert element_data["Mat12Tag"] == 212
    assert element_data["Mat13Tag"] == 213
    assert element_data["eleHeightFac"] == 0.8
    assert element_data["eleWidthFac"] == 0.9


def test_handle_ElasticTubularJoint(element_manager: ElementManager) -> None:
    """测试ElasticTubularJoint元素的数据处理"""
    # 使用基本参数
    cmd = "element"
    args = (
        "ElasticTubularJoint", 3, *[9, 10],
        0.5,    # Brace_Diameter
        45.0,   # Brace_Angle
        29000.0,# E
        1.0,    # Chord_Diameter
        0.1,    # Chord_Thickness
        90.0    # Chord_Angle
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 3 in element_manager.elements
    element_data = element_manager.elements[3]
    assert element_data["eleType"] == "ElasticTubularJoint"
    assert element_data["eleTag"] == 3
    assert element_data["eleNodes"] == [9, 10]
    assert element_data["Brace_Diameter"] == 0.5
    assert element_data["Brace_Angle"] == 45.0
    assert element_data["E"] == 29000.0
    assert element_data["Chord_Diameter"] == 1.0
    assert element_data["Chord_Thickness"] == 0.1
    assert element_data["Chord_Angle"] == 90.0


def test_handle_Joint2D_basic(element_manager: ElementManager) -> None:
    """测试基本的Joint2D元素的数据处理"""
    # 使用基本参数
    cmd = "element"
    args = (
        "Joint2D", 4, *[11, 12, 13, 14, 15],  # eleNodes
        301,  # MatC
        0     # LrgDspTag
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 4 in element_manager.elements
    element_data = element_manager.elements[4]
    assert element_data["eleType"] == "Joint2D"
    assert element_data["eleTag"] == 4
    assert element_data["eleNodes"] == [11, 12, 13, 14, 15]
    assert element_data["MatC"] == 301
    assert element_data["LrgDspTag"] == 0


def test_handle_Joint2D_with_interface_springs(element_manager: ElementManager) -> None:
    """测试带界面弹簧的Joint2D元素的数据处理"""
    # 使用带界面弹簧的情况
    cmd = "element"
    args = (
        "Joint2D", 5, *[16, 17, 18, 19, 20],  # eleNodes
        401, 402, 403, 404,  # Mat1, Mat2, Mat3, Mat4 (界面弹簧)
        501,  # MatC
        1     # LrgDspTag
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 5 in element_manager.elements
    element_data = element_manager.elements[5]
    assert element_data["eleType"] == "Joint2D"
    assert element_data["eleTag"] == 5
    assert element_data["eleNodes"] == [16, 17, 18, 19, 20]
    assert element_data["Mat1"] == 401
    assert element_data["Mat2"] == 402
    assert element_data["Mat3"] == 403
    assert element_data["Mat4"] == 404
    assert element_data["MatC"] == 501
    assert element_data["LrgDspTag"] == 1


def test_handle_Joint2D_with_damage_tag(element_manager: ElementManager) -> None:
    """测试带损伤标签的Joint2D元素的数据处理"""
    # 使用带单一损伤标签的情况
    cmd = "element"
    args = (
        "Joint2D", 6, *[21, 22, 23, 24, 25],  # eleNodes
        601,  # MatC
        2,    # LrgDspTag
        "-damage", 701  # DmgTag
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 6 in element_manager.elements
    element_data = element_manager.elements[6]
    assert element_data["eleType"] == "Joint2D"
    assert element_data["eleTag"] == 6
    assert element_data["eleNodes"] == [21, 22, 23, 24, 25]
    assert element_data["MatC"] == 601
    assert element_data["LrgDspTag"] == 2
    assert element_data["DmgTag"] == 701


def test_handle_Joint2D_with_detailed_damage(element_manager: ElementManager) -> None:
    """测试带详细损伤参数的Joint2D元素的数据处理"""
    # 使用带详细损伤参数的情况
    cmd = "element"
    args = (
        "Joint2D", 7, *[26, 27, 28, 29, 30],  # eleNodes
        701,  # MatC
        2,    # LrgDspTag
        "-damage", 801, 802, 803, 804, 805  # Dmg1, Dmg2, Dmg3, Dmg4, DmgC
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 7 in element_manager.elements
    element_data = element_manager.elements[7]
    assert element_data["eleType"] == "Joint2D"
    assert element_data["eleTag"] == 7
    assert element_data["eleNodes"] == [26, 27, 28, 29, 30]
    assert element_data["MatC"] == 701
    assert element_data["LrgDspTag"] == 2
    assert element_data["Dmg1"] == 801
    assert element_data["Dmg2"] == 802
    assert element_data["Dmg3"] == 803
    assert element_data["Dmg4"] == 804
    assert element_data["DmgC"] == 805


def test_handle_unknown_Joint(element_manager: ElementManager) -> None:
    """测试处理未知的Joint元素"""
    cmd = "element"
    args = ("customJoint", 8, *[31, 32, 33, 34], 901, 902, 903)
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 8 in element_manager.elements
    element_data = element_manager.elements[8]
    assert element_data["eleType"] == "customJoint"
    assert element_data["eleTag"] == 8
    assert "args" in element_data  # 未知元素应该将额外参数保存在args中
