import openseespy.opensees as ops
import pytest

from opsparser import MaterialManager


@pytest.fixture
def material_manager() -> MaterialManager:
    """每个测试前初始化一个MaterialManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return MaterialManager()


def test_handle_PressureIndependMultiYield(material_manager: MaterialManager) -> None:
    """测试PressureIndependMultiYield材料的数据处理"""
    cmd = "nDMaterial"
    args = ("PressureIndependMultiYield", 1, 3, 1600.0, 9.0e4, 2.2e5, 70.0, 0.1)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 1 in material_manager.materials
    material_data = material_manager.materials[1]
    assert material_data["matType"] == "PressureIndependMultiYield"
    assert material_data["matTag"] == 1
    assert material_data["nd"] == 3
    assert material_data["rho"] == 1600.0
    assert material_data["refShearModul"] == 9.0e4
    assert material_data["refBulkModul"] == 2.2e5
    assert material_data["cohesi"] == 70.0
    assert material_data["peakShearStra"] == 0.1
    assert material_data["materialCommandType"] == "nDMaterial"

    # 测试包含可选参数
    args = ("PressureIndependMultiYield", 2, 2, 1500.0, 8.0e4, 2.0e5, 65.0, 0.08, 32.0, 101.3, 0.5, 15)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})
    material_data = material_manager.materials[2]
    assert material_data["matType"] == "PressureIndependMultiYield"
    assert material_data["matTag"] == 2
    assert material_data["nd"] == 2
    assert material_data["frictionAng"] == 32.0
    assert material_data["refPress"] == 101.3
    assert material_data["pressDependCoe"] == 0.5
    assert material_data["noYieldSurf"] == 15


def test_handle_PressureDependMultiYield(material_manager: MaterialManager) -> None:
    """测试PressureDependMultiYield材料的数据处理"""
    cmd = "nDMaterial"
    # 基本测试
    args = ("PressureDependMultiYield", 3, 2, 1800.0, 1.0e5, 2.4e5, 33.0, 0.15, 
            100.0, 0.5, 27.0, 0.07, [0.3, 0.0], [1.0, 0.0])
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 3 in material_manager.materials
    material_data = material_manager.materials[3]
    assert material_data["matType"] == "PressureDependMultiYield"
    assert material_data["matTag"] == 3
    assert material_data["nd"] == 2
    assert material_data["rho"] == 1800.0
    assert material_data["refShearModul"] == 1.0e5
    assert material_data["refBulkModul"] == 2.4e5
    assert material_data["frictionAng"] == 33.0
    assert material_data["peakShearStra"] == 0.15
    assert material_data["refPress"] == 100.0
    assert material_data["pressDependCoe"] == 0.5
    assert material_data["PTAng"] == 27.0
    assert material_data["contrac"] == 0.07
    assert material_data["dilat"] == [0.3, 0.0]
    assert material_data["liquefac"] == [1.0, 0.0]
    assert material_data["materialCommandType"] == "nDMaterial"

    # 测试带可选参数
    args = ("PressureDependMultiYield", 4, 3, 1850.0, 1.1e5, 2.5e5, 34.0, 0.16, 
            101.3, 0.6, 28.0, 0.08, [0.4, 0.1], [1.1, 0.1], 18, [], 0.7, [0.95, 0.03, 0.75, 101.0], 0.4)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})
    material_data = material_manager.materials[4]
    assert material_data["matType"] == "PressureDependMultiYield"
    assert material_data["matTag"] == 4
    assert material_data["noYieldSurf"] == 18
    assert material_data["e"] == 0.7
    assert material_data["params"] == [0.95, 0.03, 0.75, 101.0]
    assert material_data["c"] == 0.4


def test_handle_PressureDependMultiYield02(material_manager: MaterialManager) -> None:
    """测试PressureDependMultiYield02材料的数据处理"""
    cmd = "nDMaterial"
    # 基本测试
    args = ("PressureDependMultiYield02", 5, 3, 1900.0, 1.2e5, 2.6e5, 35.0, 0.17, 
            102.0, 0.7, 29.0, 0.09, 0.02, 0.5, 0.03)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 5 in material_manager.materials
    material_data = material_manager.materials[5]
    assert material_data["matType"] == "PressureDependMultiYield02"
    assert material_data["matTag"] == 5
    assert material_data["nd"] == 3
    assert material_data["rho"] == 1900.0
    assert material_data["refShearModul"] == 1.2e5
    assert material_data["refBulkModul"] == 2.6e5
    assert material_data["frictionAng"] == 35.0
    assert material_data["peakShearStra"] == 0.17
    assert material_data["refPress"] == 102.0
    assert material_data["pressDependCoe"] == 0.7
    assert material_data["PTAng"] == 29.0
    assert material_data["contrac1"] == 0.09
    assert material_data["contrac3"] == 0.02
    assert material_data["dilat1"] == 0.5
    assert material_data["dilat3"] == 0.03
    assert material_data["materialCommandType"] == "nDMaterial"

    # 测试带可选参数
    args = ("PressureDependMultiYield02", 6, 2, 1950.0, 1.3e5, 2.7e5, 36.0, 0.18, 
            102.5, 0.75, 30.0, 0.1, 0.03, 0.6, 0.04, 19, [], 5.5, 3.5, 
            [1.2, 0.1], 0.65, [0.96, 0.035, 0.76, 102.0], 0.15)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})
    material_data = material_manager.materials[6]
    assert material_data["matType"] == "PressureDependMultiYield02"
    assert material_data["matTag"] == 6
    assert material_data["noYieldSurf"] == 19
    assert material_data["contrac2"] == 5.5
    assert material_data["dilat2"] == 3.5
    assert material_data["liquefac"] == [1.2, 0.1]
    assert material_data["e"] == 0.65
    assert material_data["params"] == [0.96, 0.035, 0.76, 102.0]
    assert material_data["c"] == 0.15


def test_handle_PressureDependMultiYield03(material_manager: MaterialManager) -> None:
    """测试PressureDependMultiYield03材料的数据处理"""
    cmd = "nDMaterial"
    # 基本测试
    args = ("PressureDependMultiYield03", 7, 2, 2000.0, 1.4e5, 2.8e5, 37.0, 0.19, 
            103.0, 0.8, 31.0, 0.12, 0.05, 0.08, 0.1, 0.15, 0.7, 0.5, 0.3)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 7 in material_manager.materials
    material_data = material_manager.materials[7]
    assert material_data["matType"] == "PressureDependMultiYield03"
    assert material_data["matTag"] == 7
    assert material_data["nd"] == 2
    assert material_data["rho"] == 2000.0
    assert material_data["refShearModul"] == 1.4e5
    assert material_data["refBulkModul"] == 2.8e5
    assert material_data["frictionAng"] == 37.0
    assert material_data["peakShearStra"] == 0.19
    assert material_data["refPress"] == 103.0
    assert material_data["pressDependCoe"] == 0.8
    assert material_data["PTAng"] == 31.0
    assert material_data["ca"] == 0.12
    assert material_data["cb"] == 0.05
    assert material_data["cc"] == 0.08
    assert material_data["cd"] == 0.1
    assert material_data["ce"] == 0.15
    assert material_data["da"] == 0.7
    assert material_data["db"] == 0.5
    assert material_data["dc"] == 0.3
    assert material_data["materialCommandType"] == "nDMaterial"

    # 测试带可选参数
    args = ("PressureDependMultiYield03", 8, 3, 2050.0, 1.5e5, 2.9e5, 38.0, 0.2, 
            103.5, 0.85, 32.0, 0.13, 0.06, 0.09, 0.11, 0.16, 0.75, 0.55, 0.35, 
            20, [], 1.1, 0.2, 102.0, 1.75)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})
    material_data = material_manager.materials[8]
    assert material_data["matType"] == "PressureDependMultiYield03"
    assert material_data["matTag"] == 8
    assert material_data["noYieldSurf"] == 20
    assert material_data["liquefac1"] == 1.1
    assert material_data["liquefac2"] == 0.2
    assert material_data["pa"] == 102.0
    assert material_data["s0"] == 1.75


def test_handle_unknown_ucsd_soil_model(material_manager: MaterialManager) -> None:
    """测试处理未知的UC San Diego土壤模型"""
    cmd = "nDMaterial"
    args = ("CustomUCSDSoilModel", 9, 3, 2100.0, 1.6e5, 3.0e5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 9 in material_manager.materials
    material_data = material_manager.materials[9]
    assert material_data["matType"] == "CustomUCSDSoilModel"
    assert material_data["matTag"] == 9
    assert material_data["materialType"] == cmd
    assert "args" in material_data  # 未知材料应该将额外参数保存在args中
