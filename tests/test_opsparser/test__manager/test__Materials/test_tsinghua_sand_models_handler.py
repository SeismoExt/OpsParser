import openseespy.opensees as ops
import pytest

from opsparser import MaterialManager


@pytest.fixture
def material_manager() -> MaterialManager:
    """每个测试前初始化一个MaterialManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return MaterialManager()


def test_handle_CycLiqCP(material_manager: MaterialManager) -> None:
    """测试CycLiqCP材料的数据处理"""
    cmd = "nDMaterial"
    args = ("CycLiqCP", 1, 100.0, 130.0, 0.7, 1.4, 0.2, 1.0, 0.5, 0.3, 0.7, 0.5, 0.8, 2000.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 1 in material_manager.materials
    material_data = material_manager.materials[1]
    assert material_data["matType"] == "CycLiqCP"
    assert material_data["matTag"] == 1
    assert material_data["G0"] == 100.0
    assert material_data["kappa"] == 130.0
    assert material_data["h"] == 0.7
    assert material_data["Mfc"] == 1.4
    assert material_data["dre1"] == 0.2
    assert material_data["Mdc"] == 1.0
    assert material_data["dre2"] == 0.5
    assert material_data["rdr"] == 0.3
    assert material_data["alpha"] == 0.7
    assert material_data["dir"] == 0.5
    assert material_data["ein"] == 0.8
    assert material_data["rho"] == 2000.0
    assert material_data["materialCommandType"] == "nDMaterial"


def test_handle_CycLiqCPSP(material_manager: MaterialManager) -> None:
    """测试CycLiqCPSP材料的数据处理"""
    cmd = "nDMaterial"
    args = ("CycLiqCPSP", 2, 110.0, 140.0, 0.8, 1.5, 0.3, 0.6, 0.4, 0.8, 0.6, 0.02, 0.7, 0.9, 0.4, 0.5, 0.85, 2100.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 2 in material_manager.materials
    material_data = material_manager.materials[2]
    assert material_data["matType"] == "CycLiqCPSP"
    assert material_data["matTag"] == 2
    assert material_data["G0"] == 110.0
    assert material_data["kappa"] == 140.0
    assert material_data["h"] == 0.8
    assert material_data["M"] == 1.5
    assert material_data["dre1"] == 0.3
    assert material_data["dre2"] == 0.6
    assert material_data["rdr"] == 0.4
    assert material_data["alpha"] == 0.8
    assert material_data["dir"] == 0.6
    assert material_data["lambdac"] == 0.02
    assert material_data["ksi"] == 0.7
    assert material_data["e0"] == 0.9
    assert material_data["np"] == 0.4
    assert material_data["nd"] == 0.5
    assert material_data["ein"] == 0.85
    assert material_data["rho"] == 2100.0
    assert material_data["materialCommandType"] == "nDMaterial"


def test_handle_unknown_tsinghua_sand_model(material_manager: MaterialManager) -> None:
    """测试处理未知的清华沙土模型"""
    cmd = "nDMaterial"
    args = ("CustomTsinghuaSandModel", 3, 10.0, 20.0, 30.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 3 in material_manager.materials
    material_data = material_manager.materials[3]
    assert material_data["matType"] == "CustomTsinghuaSandModel"
    assert material_data["matTag"] == 3
    assert material_data["materialType"] == cmd
    assert "args" in material_data  # 未知材料应该将额外参数保存在args中
