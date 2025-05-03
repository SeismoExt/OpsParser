import openseespy.opensees as ops
import pytest

from opsparser import ElementManager


@pytest.fixture
def element_manager() -> ElementManager:
    """每个测试前初始化一个ElementManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return ElementManager()


def test_handle_twoNodeLink_basic(element_manager: ElementManager) -> None:
    """测试基本的twoNodeLink元素的数据处理"""
    # 基本的twoNodeLink元素
    cmd = "element"
    args = (
        "twoNodeLink", 1, *[1, 2],
        "-mat", *[101, 102, 103],
        "-dir", *[1, 2, 3]
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 1 in element_manager.elements
    element_data = element_manager.elements[1]
    assert element_data["eleType"] == "twoNodeLink"
    assert element_data["eleTag"] == 1
    assert element_data["eleNodes"] == [1, 2]
    assert element_data["matTags"] == [101, 102, 103]
    assert element_data["dirs"] == [1, 2, 3]


def test_handle_twoNodeLink_with_orient(element_manager: ElementManager) -> None:
    """测试带有orientation向量的twoNodeLink元素的数据处理"""
    # 带有orientation向量的twoNodeLink元素
    cmd = "element"
    args = (
        "twoNodeLink", 2, *[3, 4],
        "-mat", *[201, 202, 203, 204],
        "-dir", *[1, 2, 3, 4],
        "-orient", *[1.0, 0.0, 0.0, 0.0, 1.0, 0.0]
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 2 in element_manager.elements
    element_data = element_manager.elements[2]
    assert element_data["eleType"] == "twoNodeLink"
    assert element_data["eleTag"] == 2
    assert element_data["eleNodes"] == [3, 4]
    assert element_data["matTags"] == [201, 202, 203, 204]
    assert element_data["dirs"] == [1, 2, 3, 4]
    assert element_data["vecx"] == [1.0, 0.0, 0.0]
    assert element_data["vecyp"] == [0.0, 1.0, 0.0]


def test_handle_twoNodeLink_with_pDelta(element_manager: ElementManager) -> None:
    """测试带有pDelta参数的twoNodeLink元素的数据处理"""
    # 带有pDelta参数的twoNodeLink元素
    cmd = "element"
    args = (
        "twoNodeLink", 3, *[5, 6],
        "-mat", *[301, 302, 303],
        "-dir", *[1, 2, 3],
        "-pDelta", *[0.4, 0.6]
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 3 in element_manager.elements
    element_data = element_manager.elements[3]
    assert element_data["eleType"] == "twoNodeLink"
    assert element_data["eleTag"] == 3
    assert element_data["eleNodes"] == [5, 6]
    assert element_data["matTags"] == [301, 302, 303]
    assert element_data["dirs"] == [1, 2, 3]
    assert element_data["pDeltaVals"] == [0.4, 0.6]


def test_handle_twoNodeLink_with_shearDist(element_manager: ElementManager) -> None:
    """测试带有shearDist参数的twoNodeLink元素的数据处理"""
    # 带有shearDist参数的twoNodeLink元素
    cmd = "element"
    args = (
        "twoNodeLink", 4, *[7, 8],
        "-mat", *[401, 402],
        "-dir", *[1, 2],
        "-shearDist", *[0.7]
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 4 in element_manager.elements
    element_data = element_manager.elements[4]
    assert element_data["eleType"] == "twoNodeLink"
    assert element_data["eleTag"] == 4
    assert element_data["eleNodes"] == [7, 8]
    assert element_data["matTags"] == [401, 402]
    assert element_data["dirs"] == [1, 2]
    assert element_data["sDratios"] == [0.7]


def test_handle_twoNodeLink_with_doRayleigh(element_manager: ElementManager) -> None:
    """测试带有doRayleigh参数的twoNodeLink元素的数据处理"""
    # 带有doRayleigh参数的twoNodeLink元素
    cmd = "element"
    args = (
        "twoNodeLink", 5, *[9, 10],
        "-mat", *[501, 502, 503, 504, 505, 506],
        "-dir", *[1, 2, 3, 4, 5, 6],
        "-doRayleigh"
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 5 in element_manager.elements
    element_data = element_manager.elements[5]
    assert element_data["eleType"] == "twoNodeLink"
    assert element_data["eleTag"] == 5
    assert element_data["eleNodes"] == [9, 10]
    assert element_data["matTags"] == [501, 502, 503, 504, 505, 506]
    assert element_data["dirs"] == [1, 2, 3, 4, 5, 6]
    assert element_data.get("doRayleigh") == True


def test_handle_twoNodeLink_with_mass(element_manager: ElementManager) -> None:
    """测试带有mass参数的twoNodeLink元素的数据处理"""
    # 带有mass参数的twoNodeLink元素
    cmd = "element"
    args = (
        "twoNodeLink", 6, *[11, 12],
        "-mat", *[601, 602],
        "-dir", *[1, 3],
        "-mass", 2.5
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 6 in element_manager.elements
    element_data = element_manager.elements[6]
    assert element_data["eleType"] == "twoNodeLink"
    assert element_data["eleTag"] == 6
    assert element_data["eleNodes"] == [11, 12]
    assert element_data["matTags"] == [601, 602]
    assert element_data["dirs"] == [1, 3]
    assert element_data["mass"] == 2.5


def test_handle_twoNodeLink_with_all_options(element_manager: ElementManager) -> None:
    """测试带有所有可选参数的twoNodeLink元素的数据处理"""
    # 带有所有可选参数的twoNodeLink元素
    cmd = "element"
    args = (
        "twoNodeLink", 7, *[13, 14],
        "-mat", *[701, 702, 703, 704, 705, 706],
        "-dir", *[1, 2, 3, 4, 5, 6],
        "-orient", *[0.0, 1.0, 0.0, -1.0, 0.0, 0.0],
        "-pDelta", *[0.3, 0.3, 0.2, 0.2],
        "-shearDist", *[0.4, 0.6],
        "-doRayleigh",
        "-mass", 3.0
    )
    element_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查元素是否正确存储
    assert 7 in element_manager.elements
    element_data = element_manager.elements[7]
    assert element_data["eleType"] == "twoNodeLink"
    assert element_data["eleTag"] == 7
    assert element_data["eleNodes"] == [13, 14]
    assert element_data["matTags"] == [701, 702, 703, 704, 705, 706]
    assert element_data["dirs"] == [1, 2, 3, 4, 5, 6]
    assert element_data["vecx"] == [0.0, 1.0, 0.0]
    assert element_data["vecyp"] == [-1.0, 0.0, 0.0]
    assert element_data["pDeltaVals"] == [0.3, 0.3, 0.2, 0.2]
    assert element_data["sDratios"] == [0.4, 0.6]
    assert element_data.get("doRayleigh") is True
    assert element_data["mass"] == 3.0
