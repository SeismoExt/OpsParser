import openseespy.opensees as ops
import pytest

from opsparser import MaterialManager


@pytest.fixture
def material_manager() -> MaterialManager:
    """每个测试前初始化一个MaterialManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return MaterialManager()


def test_handle_FluidSolidPorous(material_manager: MaterialManager) -> None:
    """测试FluidSolidPorous材料的数据处理"""
    cmd = "nDMaterial"
    # 基本测试, 不含可选参数
    args = ("FluidSolidPorous", 1, 2, 100, 2.2e6)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 1 in material_manager.materials
    material_data = material_manager.materials[1]
    assert material_data["matType"] == "FluidSolidPorous"
    assert material_data["matTag"] == 1
    assert material_data["nd"] == 2
    assert material_data["soilMatTag"] == 100
    assert material_data["combinedBulkModul"] == 2.2e6
    assert material_data["materialCommandType"] == "nDMaterial"

    # 测试带可选参数
    args = ("FluidSolidPorous", 2, 3, 101, 2.4e6, 101.3)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})
    material_data = material_manager.materials[2]
    assert material_data["matType"] == "FluidSolidPorous"
    assert material_data["matTag"] == 2
    assert material_data["nd"] == 3
    assert material_data["soilMatTag"] == 101
    assert material_data["combinedBulkModul"] == 2.4e6
    assert material_data["pa"] == 101.3
    assert material_data["materialCommandType"] == "nDMaterial"


def test_handle_unknown_ucsd_saturated_soil_model(material_manager: MaterialManager) -> None:
    """测试处理未知的UC San Diego饱和非排水土壤模型"""
    cmd = "nDMaterial"
    args = ("CustomUCSDSaturatedSoilModel", 3, 2, 102, 2.5e6)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 3 in material_manager.materials
    material_data = material_manager.materials[3]
    assert material_data["matType"] == "CustomUCSDSaturatedSoilModel"
    assert material_data["matTag"] == 3
    assert material_data["materialType"] == cmd
    assert "args" in material_data  # 未知材料应该将额外参数保存在args中
