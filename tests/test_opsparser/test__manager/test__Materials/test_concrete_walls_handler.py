import openseespy.opensees as ops
import pytest

from opsparser import MaterialManager


@pytest.fixture
def material_manager() -> MaterialManager:
    """每个测试前初始化一个MaterialManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return MaterialManager()


def test_handle_PlateFromPlaneStress(material_manager: MaterialManager) -> None:
    """测试PlateFromPlaneStress材料的数据处理"""
    cmd = "nDMaterial"
    args = ("PlateFromPlaneStress", 1, 100, 2000.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 1 in material_manager.materials
    material_data = material_manager.materials[1]
    assert material_data["matType"] == "PlateFromPlaneStress"
    assert material_data["matTag"] == 1
    assert material_data["pre_def_matTag"] == 100
    assert material_data["OutofPlaneModulus"] == 2000.0
    assert material_data["materialCommandType"] == "nDMaterial"


def test_handle_PlateRebar(material_manager: MaterialManager) -> None:
    """测试PlateRebar材料的数据处理"""
    cmd = "nDMaterial"
    args = ("PlateRebar", 2, 101, 90.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 2 in material_manager.materials
    material_data = material_manager.materials[2]
    assert material_data["matType"] == "PlateRebar"
    assert material_data["matTag"] == 2
    assert material_data["pre_def_matTag"] == 101
    assert material_data["sita"] == 90.0
    assert material_data["materialCommandType"] == "nDMaterial"

    # 测试横向钢筋
    args = ("PlateRebar", 3, 102, 0.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})
    material_data = material_manager.materials[3]
    assert material_data["matType"] == "PlateRebar"
    assert material_data["sita"] == 0.0


def test_handle_PlasticDamageConcretePlaneStress(material_manager: MaterialManager) -> None:
    """测试PlasticDamageConcretePlaneStress材料的数据处理"""
    cmd = "nDMaterial"
    # 基本参数测试
    args = ("PlasticDamageConcretePlaneStress", 4, 30000.0, 0.2, 3.0, 30.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 4 in material_manager.materials
    material_data = material_manager.materials[4]
    assert material_data["matType"] == "PlasticDamageConcretePlaneStress"
    assert material_data["matTag"] == 4
    assert material_data["E"] == 30000.0
    assert material_data["nu"] == 0.2
    assert material_data["ft"] == 3.0
    assert material_data["fc"] == 30.0
    assert material_data["materialCommandType"] == "nDMaterial"

    # 测试带可选参数的情况
    args = ("PlasticDamageConcretePlaneStress", 5, 32000.0, 0.2, 3.5, 35.0, 0.6, 0.5, 0.4, 0.3)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})
    material_data = material_manager.materials[5]
    assert material_data["matType"] == "PlasticDamageConcretePlaneStress"
    assert material_data["E"] == 32000.0
    assert material_data["beta"] == 0.6
    assert material_data["Ap"] == 0.5
    assert material_data["An"] == 0.4
    assert material_data["Bn"] == 0.3


def test_handle_unknown_concrete_wall_model(material_manager: MaterialManager) -> None:
    """测试处理未知的混凝土墙体材料模型"""
    cmd = "nDMaterial"
    args = ("CustomConcreteWallModel", 6, 10.0, 20.0, 30.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 6 in material_manager.materials
    material_data = material_manager.materials[6]
    assert material_data["matType"] == "CustomConcreteWallModel"
    assert material_data["matTag"] == 6
    assert material_data["materialType"] == cmd
    assert "args" in material_data  # 未知材料应该将额外参数保存在args中
