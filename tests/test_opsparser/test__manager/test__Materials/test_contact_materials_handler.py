import openseespy.opensees as ops
import pytest

from opsparser import MaterialManager


@pytest.fixture
def material_manager() -> MaterialManager:
    """每个测试前初始化一个MaterialManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return MaterialManager()


def test_handle_ContactMaterial2D(material_manager: MaterialManager) -> None:
    """测试ContactMaterial2D材料的数据处理"""
    cmd = "nDMaterial"
    args = ("ContactMaterial2D", 1, 0.3, 1000.0, 5.0, 2.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 1 in material_manager.materials
    material_data = material_manager.materials[1]
    assert material_data["matType"] == "ContactMaterial2D"
    assert material_data["matTag"] == 1
    assert material_data["mu"] == 0.3
    assert material_data["G"] == 1000.0
    assert material_data["c"] == 5.0
    assert material_data["t"] == 2.0
    assert material_data["materialCommandType"] == "nDMaterial"


def test_handle_ContactMaterial3D(material_manager: MaterialManager) -> None:
    """测试ContactMaterial3D材料的数据处理"""
    cmd = "nDMaterial"
    args = ("ContactMaterial3D", 2, 0.4, 1200.0, 6.0, 3.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 2 in material_manager.materials
    material_data = material_manager.materials[2]
    assert material_data["matType"] == "ContactMaterial3D"
    assert material_data["matTag"] == 2
    assert material_data["mu"] == 0.4
    assert material_data["G"] == 1200.0
    assert material_data["c"] == 6.0
    assert material_data["t"] == 3.0
    assert material_data["materialCommandType"] == "nDMaterial"


def test_handle_unknown_contact_material(material_manager: MaterialManager) -> None:
    """测试处理未知的接触材料模型"""
    cmd = "nDMaterial"
    args = ("CustomContactMaterial", 3, 0.5, 1500.0, 7.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 3 in material_manager.materials
    material_data = material_manager.materials[3]
    assert material_data["matType"] == "CustomContactMaterial"
    assert material_data["matTag"] == 3
    assert material_data["materialType"] == cmd
    assert "args" in material_data  # 未知材料应该将额外参数保存在args中
