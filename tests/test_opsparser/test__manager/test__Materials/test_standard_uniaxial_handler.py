import openseespy.opensees as ops
import pytest

from opsparser import MaterialManager


@pytest.fixture
def material_manager() -> MaterialManager:
    """每个测试前初始化一个MaterialManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return MaterialManager()


def test_handle_Elastic(material_manager: MaterialManager) -> None:
    """测试Elastic单轴材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Elastic", 1, 200000.0, 0.02, 180000.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 1 in material_manager.materials
    material_data = material_manager.materials[1]
    assert material_data["matType"] == "Elastic"
    assert material_data["matTag"] == 1
    assert material_data["E"] == 200000.0
    assert material_data["eta"] == 0.02
    assert material_data["Eneg"] == 180000.0
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_ElasticPP(material_manager: MaterialManager) -> None:
    """测试ElasticPP单轴材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ElasticPP", 2, 200000.0, 0.001, -0.0015, 0.0002)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 2 in material_manager.materials
    material_data = material_manager.materials[2]
    assert material_data["matType"] == "ElasticPP"
    assert material_data["matTag"] == 2
    assert material_data["E"] == 200000.0
    assert material_data["epsyP"] == 0.001
    assert material_data["epsyN"] == -0.0015
    assert material_data["eps0"] == 0.0002
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_ElasticPPGap(material_manager: MaterialManager) -> None:
    """测试ElasticPPGap单轴材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ElasticPPGap", 3, 200000.0, 50.0, 0.005, 0.1, "damage")
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 3 in material_manager.materials
    material_data = material_manager.materials[3]
    assert material_data["matType"] == "ElasticPPGap"
    assert material_data["matTag"] == 3
    assert material_data["E"] == 200000.0
    assert material_data["Fy"] == 50.0
    assert material_data["gap"] == 0.005
    assert material_data["eta"] == 0.1
    assert material_data["damage"] == "damage"
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_ENT(material_manager: MaterialManager) -> None:
    """测试ENT单轴材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ENT", 4, 200000.0, 10.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 4 in material_manager.materials
    material_data = material_manager.materials[4]
    assert material_data["matType"] == "ENT"
    assert material_data["matTag"] == 4
    assert material_data["E"] == 200000.0
    assert material_data["minE"] == 10.0
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_Hysteretic(material_manager: MaterialManager) -> None:
    """测试Hysteretic单轴材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Hysteretic", 5, 15.0, 0.005, 25.0, 0.01, 5.0, 0.015, -15.0, -0.005, -25.0, -0.01, -5.0, -0.015, 0.8, 0.7, 0.25, 0.35, 0.1)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 5 in material_manager.materials
    material_data = material_manager.materials[5]
    assert material_data["matType"] == "Hysteretic"
    assert material_data["matTag"] == 5
    assert material_data["s1p"] == 15.0
    assert material_data["e1p"] == 0.005
    assert material_data["s2p"] == 25.0
    assert material_data["e2p"] == 0.01
    assert material_data["s3p"] == 5.0
    assert material_data["e3p"] == 0.015
    assert material_data["s1n"] == -15.0
    assert material_data["e1n"] == -0.005
    assert material_data["s2n"] == -25.0
    assert material_data["e2n"] == -0.01
    assert material_data["s3n"] == -5.0
    assert material_data["e3n"] == -0.015
    assert material_data["pinchX"] == 0.8
    assert material_data["pinchY"] == 0.7
    assert material_data["damage1"] == 0.25
    assert material_data["damage2"] == 0.35
    assert material_data["beta"] == 0.1
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_Parallel(material_manager: MaterialManager) -> None:
    """测试Parallel单轴材料的数据处理"""
    # 先创建几个材料作为Parallel的组成部分
    material_manager.handle("uniaxialMaterial", {"args": ("Elastic", 11, 200000.0), "kwargs": {}})
    material_manager.handle("uniaxialMaterial", {"args": ("Elastic", 12, 150000.0), "kwargs": {}})
    
    # 创建Parallel材料
    cmd = "uniaxialMaterial"
    args = ("Parallel", 6, [11, 12])
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 6 in material_manager.materials
    material_data = material_manager.materials[6]
    assert material_data["matType"] == "Parallel"
    assert material_data["matTag"] == 6
    assert material_data["tags"] == [11, 12]
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_Series(material_manager: MaterialManager) -> None:
    """测试Series单轴材料的数据处理"""
    # 先创建几个材料作为Series的组成部分
    material_manager.handle("uniaxialMaterial", {"args": ("Elastic", 21, 200000.0), "kwargs": {}})
    material_manager.handle("uniaxialMaterial", {"args": ("Elastic", 22, 150000.0), "kwargs": {}})
    
    # 创建Series材料
    cmd = "uniaxialMaterial"
    args = ("Series", 7, [21, 22])
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 7 in material_manager.materials
    material_data = material_manager.materials[7]
    assert material_data["matType"] == "Series"
    assert material_data["matTag"] == 7
    assert material_data["tags"] == [21, 22]
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_Parallel_with_factors(material_manager: MaterialManager) -> None:
    """测试带有factors参数的Parallel单轴材料的数据处理"""
    # 先创建几个材料作为Parallel的组成部分
    material_manager.handle("uniaxialMaterial", {"args": ("Elastic", 31, 200000.0), "kwargs": {}})
    material_manager.handle("uniaxialMaterial", {"args": ("Elastic", 32, 150000.0), "kwargs": {}})
    
    # 创建带factors的Parallel材料
    cmd = "uniaxialMaterial"
    args = ("Parallel", 8, [31, 32])
    kwargs = {"factors": [1.0, 0.5]}
    material_manager.handle(cmd, {"args": args, "kwargs": kwargs})

    # 检查材料是否正确存储
    assert 8 in material_manager.materials
    material_data = material_manager.materials[8]
    assert material_data["matType"] == "Parallel"
    assert material_data["matTag"] == 8
    assert material_data["tags"] == [31, 32]
    assert material_data["factors"] == [1.0, 0.5]
    assert material_data["materialCommandType"] == "uniaxialMaterial"


def test_handle_unknown_standard_uniaxial_material(material_manager: MaterialManager) -> None:
    """测试处理未知的标准单轴材料"""
    cmd = "uniaxialMaterial"
    args = ("CustomStandardMaterial", 9, 200000.0, 0.02)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 9 in material_manager.materials
    material_data = material_manager.materials[9]
    assert material_data["matType"] == "CustomStandardMaterial"
    assert material_data["matTag"] == 9
    assert material_data["materialType"] == cmd
    assert "args" in material_data  # 未知材料应该将额外参数保存在args中
