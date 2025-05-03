import openseespy.opensees as ops
import pytest

from opsparser import MaterialManager


@pytest.fixture
def material_manager() -> MaterialManager:
    """每个测试前初始化一个MaterialManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return MaterialManager()


def test_handle_Concrete01(material_manager: MaterialManager) -> None:
    """测试Concrete01材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Concrete01", 1, -30.0, -0.002, -15.0, -0.006)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 1 in material_manager.materials
    material_data = material_manager.materials[1]
    assert material_data["matType"] == "Concrete01"
    assert material_data["matTag"] == 1
    assert material_data["fpc"] == -30.0
    assert material_data["epsc0"] == -0.002
    assert material_data["fpcu"] == -15.0
    assert material_data["epscu"] == -0.006


def test_handle_Concrete02(material_manager: MaterialManager) -> None:
    """测试Concrete02材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Concrete02", 2, -35.0, -0.002, -17.5, -0.008, 0.1, 3.0, 0.05)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 2 in material_manager.materials
    material_data = material_manager.materials[2]
    assert material_data["matType"] == "Concrete02"
    assert material_data["matTag"] == 2
    assert material_data["fpc"] == -35.0
    assert material_data["epsc0"] == -0.002
    assert material_data["fpcu"] == -17.5
    assert material_data["epscu"] == -0.008
    assert material_data["lambda"] == 0.1
    assert material_data["ft"] == 3.0
    assert material_data["Ets"] == 0.05


def test_handle_Concrete04(material_manager: MaterialManager) -> None:
    """测试Concrete04材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Concrete04", 3, -30.0, -0.002, -0.01, 30000.0, 4.0, 0.0001, 0.7)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 3 in material_manager.materials
    material_data = material_manager.materials[3]
    assert material_data["matType"] == "Concrete04"
    assert material_data["matTag"] == 3
    assert material_data["fc"] == -30.0
    assert material_data["epsc"] == -0.002
    assert material_data["epscu"] == -0.01
    assert material_data["Ec"] == 30000.0
    assert material_data["fct"] == 4.0
    assert material_data["et"] == 0.0001
    assert material_data["beta"] == 0.7


def test_handle_Concrete06(material_manager: MaterialManager) -> None:
    """测试Concrete06材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Concrete06", 5, -30.0, -0.002, 0.4, 0.5, 0.75, 3.0, 0.0001, 4.0, 0.8)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 5 in material_manager.materials
    material_data = material_manager.materials[5]
    assert material_data["matType"] == "Concrete06"
    assert material_data["matTag"] == 5
    assert material_data["fc"] == -30.0
    assert material_data["e0"] == -0.002
    assert material_data["n"] == 0.4
    assert material_data["k"] == 0.5
    assert material_data["alpha1"] == 0.75
    assert material_data["fcr"] == 3.0
    assert material_data["ecr"] == 0.0001
    assert material_data["b"] == 4.0
    assert material_data["alpha2"] == 0.8


def test_handle_Concrete07(material_manager: MaterialManager) -> None:
    """测试Concrete07材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Concrete07", 4, -30.0, -0.002, 28000.0, 3.5, 0.0001, 4.0, 15.0, 1.2)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})


def test_handle_Concrete01WithSITC(material_manager: MaterialManager) -> None:
    """测试Concrete01WithSITC材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Concrete01WithSITC", 5, -30.0, -0.002, -15.0, -0.006, 0.01)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 5 in material_manager.materials
    material_data = material_manager.materials[5]
    assert material_data["matType"] == "Concrete01WithSITC"
    assert material_data["matTag"] == 5
    assert material_data["fpc"] == -30.0
    assert material_data["epsc0"] == -0.002
    assert material_data["fpcu"] == -15.0
    assert material_data["epsU"] == -0.006
    assert material_data["endStrainSITC"] == 0.01


def test_handle_ConcreteD(material_manager: MaterialManager) -> None:
    """测试ConcreteD材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ConcreteD", 6, -30.0, -0.002, 3.0, 0.0001, 28000.0, 0.18, 0.32, 0.25, 1.15)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 6 in material_manager.materials
    material_data = material_manager.materials[6]
    assert material_data["matType"] == "ConcreteD"
    assert material_data["matTag"] == 6
    assert material_data["fc"] == -30.0
    assert material_data["epsc"] == -0.002
    assert material_data["ft"] == 3.0
    assert material_data["epst"] == 0.0001
    assert material_data["Ec"] == 28000.0
    assert material_data["alphac"] == 0.18
    assert material_data["alphat"] == 0.32
    assert material_data["cesp"] == 0.25
    assert material_data["etap"] == 1.15


def test_handle_ConcreteCM(material_manager: MaterialManager) -> None:
    """测试ConcreteCM材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ConcreteCM", 7, -30.0, -0.002, 28000.0, 7.0, 1.5, 3.0, 0.0001, 1.0, 3.0, 0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 7 in material_manager.materials
    material_data = material_manager.materials[7]
    assert material_data["matType"] == "ConcreteCM"
    assert material_data["matTag"] == 7
    assert material_data["fpcc"] == -30.0
    assert material_data["epcc"] == -0.002
    assert material_data["Ec"] == 28000.0
    assert material_data["rc"] == 7.0
    assert material_data["xcrn"] == 1.5
    assert material_data["ft"] == 3.0
    assert material_data["et"] == 0.0001
    assert material_data["rt"] == 1.0
    assert material_data["xcrp"] == 3.0
    assert material_data["mon"] == 0


def test_handle_unknown_concrete_material(material_manager: MaterialManager) -> None:
    """测试处理未知的混凝土材料"""
    cmd = "uniaxialMaterial"
    args = ("CustomConcreteMaterial", 8, -30.0, -0.002, 28000.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 8 in material_manager.materials
    material_data = material_manager.materials[8]
    assert material_data["matType"] == "CustomConcreteMaterial"
    assert material_data["matTag"] == 8
    assert material_data["materialType"] == cmd
    assert "args" in material_data  # 未知材料应该将额外参数保存在args中
