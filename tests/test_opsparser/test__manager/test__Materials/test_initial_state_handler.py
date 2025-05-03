import openseespy.opensees as ops
import pytest

from opsparser import MaterialManager


@pytest.fixture
def material_manager() -> MaterialManager:
    """每个测试前初始化一个MaterialManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return MaterialManager()


def test_handle_InitialStateAnalysisWrapper(material_manager: MaterialManager) -> None:
    """测试InitialStateAnalysisWrapper材料的数据处理"""
    cmd = "nDMaterial"
    args = ("InitialStateAnalysisWrapper", 1, 100, 2)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 1 in material_manager.materials
    material_data = material_manager.materials[1]
    assert material_data["matType"] == "InitialStateAnalysisWrapper"
    assert material_data["matTag"] == 1
    assert material_data["nDMatTag"] == 100
    assert material_data["nDim"] == 2
    assert material_data["materialCommandType"] == "nDMaterial"


def test_handle_InitStressNDMaterial(material_manager: MaterialManager) -> None:
    """测试InitStressNDMaterial材料的数据处理"""
    cmd = "nDMaterial"
    args = ("InitStressNDMaterial", 2, 101, 200.0, 2)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 2 in material_manager.materials
    material_data = material_manager.materials[2]
    assert material_data["matType"] == "InitStressNDMaterial"
    assert material_data["matTag"] == 2
    assert material_data["otherTag"] == 101
    assert material_data["initStress"] == 200.0
    assert material_data["nDim"] == 2
    assert material_data["materialCommandType"] == "nDMaterial"


def test_handle_InitStrainNDMaterial(material_manager: MaterialManager) -> None:
    """测试InitStrainNDMaterial材料的数据处理"""
    cmd = "nDMaterial"
    args = ("InitStrainNDMaterial", 3, 102, 0.001, 3)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 3 in material_manager.materials
    material_data = material_manager.materials[3]
    assert material_data["matType"] == "InitStrainNDMaterial"
    assert material_data["matTag"] == 3
    assert material_data["otherTag"] == 102
    assert material_data["initStrain"] == 0.001
    assert material_data["nDim"] == 3
    assert material_data["materialCommandType"] == "nDMaterial"


def test_handle_unknown_initial_state_material(material_manager: MaterialManager) -> None:
    """测试处理未知的初始状态分析包装材料"""
    cmd = "nDMaterial"
    args = ("CustomInitialStateMaterial", 4, 103, 0.05)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 4 in material_manager.materials
    material_data = material_manager.materials[4]
    assert material_data["matType"] == "CustomInitialStateMaterial"
    assert material_data["matTag"] == 4
    assert material_data["materialType"] == cmd
    assert "args" in material_data  # 未知材料应该将额外参数保存在args中
