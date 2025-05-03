import openseespy.opensees as ops
import pytest

from opsparser import MaterialManager


@pytest.fixture
def material_manager() -> MaterialManager:
    """每个测试前初始化一个MaterialManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return MaterialManager()


def test_handle_ElasticIsotropic(material_manager: MaterialManager) -> None:
    """测试ElasticIsotropic材料的数据处理"""
    cmd = "nDMaterial"
    args = ("ElasticIsotropic", 1, 2000.0, 0.3, 1.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 1 in material_manager.materials
    material_data = material_manager.materials[1]
    assert material_data["matType"] == "ElasticIsotropic"
    assert material_data["matTag"] == 1
    assert material_data["E"] == 2000.0
    assert material_data["nu"] == 0.3
    assert material_data["rho"] == 1.5

    # 测试可选参数缺失的情况
    args = ("ElasticIsotropic", 2, 3000.0, 0.25)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})
    material_data = material_manager.materials[2]
    assert material_data["matType"] == "ElasticIsotropic"
    assert material_data["matTag"] == 2
    assert material_data["E"] == 3000.0
    assert material_data["nu"] == 0.25
    assert "rho" not in material_data  # 没有提供rho参数


def test_handle_ElasticOrthotropic(material_manager: MaterialManager) -> None:
    """测试ElasticOrthotropic材料的数据处理"""
    cmd = "nDMaterial"
    args = ("ElasticOrthotropic", 3, 3000.0, 2000.0, 1500.0, 0.3, 0.2, 0.25, 1200.0, 1100.0, 1050.0, 2.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 3 in material_manager.materials
    material_data = material_manager.materials[3]
    assert material_data["matType"] == "ElasticOrthotropic"
    assert material_data["matTag"] == 3
    assert material_data["Ex"] == 3000.0
    assert material_data["Ey"] == 2000.0
    assert material_data["Ez"] == 1500.0
    assert material_data["nu_xy"] == 0.3
    assert material_data["nu_yz"] == 0.2
    assert material_data["nu_zx"] == 0.25
    assert material_data["Gxy"] == 1200.0
    assert material_data["Gyz"] == 1100.0
    assert material_data["Gzx"] == 1050.0
    assert material_data["rho"] == 2.0

    # 测试可选参数缺失的情况
    args = ("ElasticOrthotropic", 4, 3500.0, 2500.0, 2000.0, 0.35, 0.25, 0.3, 1300.0, 1200.0, 1150.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})
    material_data = material_manager.materials[4]
    assert material_data["matType"] == "ElasticOrthotropic"
    assert material_data["matTag"] == 4
    assert material_data["Ez"] == 2000.0
    assert material_data["Gzx"] == 1150.0
    assert "rho" not in material_data  # 没有提供rho参数


def test_handle_J2Plasticity(material_manager: MaterialManager) -> None:
    """测试J2Plasticity材料的数据处理"""
    cmd = "nDMaterial"
    args = ("J2Plasticity", 5, 160.0, 80.0, 0.5, 0.8, 0.15, 1.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 5 in material_manager.materials
    material_data = material_manager.materials[5]
    assert material_data["matType"] == "J2Plasticity"
    assert material_data["matTag"] == 5
    assert material_data["K"] == 160.0
    assert material_data["G"] == 80.0
    assert material_data["sig0"] == 0.5
    assert material_data["sigInf"] == 0.8
    assert material_data["delta"] == 0.15
    assert material_data["H"] == 1.5


def test_handle_DruckerPrager(material_manager: MaterialManager) -> None:
    """测试DruckerPrager材料的数据处理"""
    cmd = "nDMaterial"
    args = ("DruckerPrager", 6, 160.0, 80.0, 0.7, 0.2, 0.3, 0.4, 0.5, 0.15, 0.25, 1.0, 0.8, 2.0, 101.3)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 6 in material_manager.materials
    material_data = material_manager.materials[6]
    assert material_data["matType"] == "DruckerPrager"
    assert material_data["matTag"] == 6
    assert material_data["K"] == 160.0
    assert material_data["G"] == 80.0
    assert material_data["sigmaY"] == 0.7
    assert material_data["rho"] == 0.2
    assert material_data["rhoBar"] == 0.3
    assert material_data["Kinf"] == 0.4
    assert material_data["Ko"] == 0.5
    assert material_data["delta1"] == 0.15
    assert material_data["delta2"] == 0.25
    assert material_data["H"] == 1.0
    assert material_data["theta"] == 0.8
    assert material_data["density"] == 2.0
    assert material_data["atmPressure"] == 101.3

    # 测试可选参数缺失的情况
    args = ("DruckerPrager", 7, 165.0, 85.0, 0.8, 0.25, 0.35, 0.45, 0.55, 0.2, 0.3, 1.1, 0.9, 2.1)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})
    material_data = material_manager.materials[7]
    assert material_data["matType"] == "DruckerPrager"
    assert material_data["matTag"] == 7
    assert material_data["density"] == 2.1
    assert "atmPressure" not in material_data  # 没有提供atmPressure参数


def test_handle_PlaneStress(material_manager: MaterialManager) -> None:
    """测试PlaneStress材料的数据处理"""
    cmd = "nDMaterial"
    args = ("PlaneStress", 8, 5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 8 in material_manager.materials
    material_data = material_manager.materials[8]
    assert material_data["matType"] == "PlaneStress"
    assert material_data["matTag"] == 8
    assert material_data["mat3DTag"] == 5


def test_handle_PlaneStrain(material_manager: MaterialManager) -> None:
    """测试PlaneStrain材料的数据处理"""
    cmd = "nDMaterial"
    args = ("PlaneStrain", 9, 6)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 9 in material_manager.materials
    material_data = material_manager.materials[9]
    assert material_data["matType"] == "PlaneStrain"
    assert material_data["matTag"] == 9
    assert material_data["mat3DTag"] == 6


def test_handle_MultiaxialCyclicPlasticity(material_manager: MaterialManager) -> None:
    """测试MultiaxialCyclicPlasticity材料的数据处理"""
    cmd = "nDMaterial"
    args = ("MultiaxialCyclicPlasticity", 10, 2.0, 160.0, 80.0, 0.5, 0.6, 0.7, 0.8, 0.5, 0.6)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 10 in material_manager.materials
    material_data = material_manager.materials[10]
    assert material_data["matType"] == "MultiaxialCyclicPlasticity"
    assert material_data["matTag"] == 10
    assert material_data["rho"] == 2.0
    assert material_data["K"] == 160.0
    assert material_data["G"] == 80.0
    assert material_data["Su"] == 0.5
    assert material_data["Ho"] == 0.6
    assert material_data["h"] == 0.7
    assert material_data["m"] == 0.8
    assert material_data["beta"] == 0.5
    assert material_data["KCoeff"] == 0.6


def test_handle_BoundingCamClay(material_manager: MaterialManager) -> None:
    """测试BoundingCamClay材料的数据处理"""
    cmd = "nDMaterial"
    args = ("BoundingCamClay", 11, 2.0, 1.2, 160.0, 1.5, 0.3, 0.1, 0.12, 0.5, 0.8)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 11 in material_manager.materials
    material_data = material_manager.materials[11]
    assert material_data["matType"] == "BoundingCamClay"
    assert material_data["matTag"] == 11
    assert material_data["massDensity"] == 2.0
    assert material_data["C"] == 1.2
    assert material_data["bulkMod"] == 160.0
    assert material_data["OCR"] == 1.5
    assert material_data["mu_o"] == 0.3
    assert material_data["alpha"] == 0.1
    assert material_data["lambda"] == 0.12
    assert material_data["h"] == 0.5
    assert material_data["m"] == 0.8


def test_handle_PlateFiber(material_manager: MaterialManager) -> None:
    """测试PlateFiber材料的数据处理"""
    cmd = "nDMaterial"
    args = ("PlateFiber", 12, 7)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 12 in material_manager.materials
    material_data = material_manager.materials[12]
    assert material_data["matType"] == "PlateFiber"
    assert material_data["matTag"] == 12
    assert material_data["threeDTag"] == 7


def test_handle_FSAM(material_manager: MaterialManager) -> None:
    """测试FSAM材料的数据处理"""
    cmd = "nDMaterial"
    args = ("FSAM", 13, 2.0, 201, 202, 203, 0.01, 0.02, 0.3, 0.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 13 in material_manager.materials
    material_data = material_manager.materials[13]
    assert material_data["matType"] == "FSAM"
    assert material_data["matTag"] == 13
    assert material_data["rho"] == 2.0
    assert material_data["sXTag"] == 201
    assert material_data["sYTag"] == 202
    assert material_data["concTag"] == 203
    assert material_data["rouX"] == 0.01
    assert material_data["rouY"] == 0.02
    assert material_data["nu"] == 0.3
    assert material_data["alfadow"] == 0.5


def test_handle_ManzariDafalias(material_manager: MaterialManager) -> None:
    """测试ManzariDafalias材料的数据处理"""
    cmd = "nDMaterial"
    args = ("ManzariDafalias", 14, 125.0, 0.3, 0.8, 1.25, 0.7, 0.01, 0.9, 0.1, 101.3, 0.01, 5.0, 0.9, 1.1, 0.7, 3.5, 4.0, 600.0, 2.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 14 in material_manager.materials
    material_data = material_manager.materials[14]
    assert material_data["matType"] == "ManzariDafalias"
    assert material_data["matTag"] == 14
    assert material_data["G0"] == 125.0
    assert material_data["nu"] == 0.3
    assert material_data["e_init"] == 0.8
    assert material_data["Mc"] == 1.25
    assert material_data["c"] == 0.7
    assert material_data["lambda_c"] == 0.01
    assert material_data["e0"] == 0.9
    assert material_data["ksi"] == 0.1
    assert material_data["P_atm"] == 101.3
    assert material_data["m"] == 0.01
    assert material_data["h0"] == 5.0
    assert material_data["ch"] == 0.9
    assert material_data["nb"] == 1.1
    assert material_data["A0"] == 0.7
    assert material_data["nd"] == 3.5
    assert material_data["z_max"] == 4.0
    assert material_data["cz"] == 600.0
    assert material_data["Den"] == 2.0


def test_handle_PM4Sand(material_manager: MaterialManager) -> None:
    """测试PM4Sand材料的数据处理"""
    cmd = "nDMaterial"
    # 基本参数测试
    args = ("PM4Sand", 15, 0.45, 476.0, 0.7, 1.8)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 15 in material_manager.materials
    material_data = material_manager.materials[15]
    assert material_data["matType"] == "PM4Sand"
    assert material_data["matTag"] == 15
    assert material_data["D_r"] == 0.45
    assert material_data["G_o"] == 476.0
    assert material_data["h_po"] == 0.7
    assert material_data["Den"] == 1.8

    # 测试含可选参数
    args = ("PM4Sand", 16, 0.5, 500.0, 0.75, 1.9, 101.3, 0.6, 0.9, 0.6, 0.65, 0.35, 0.8, 8.0, 250.0, 0.5, 32.0, 0.3, 1.0, 0.1, 4.0, 10.0, 1.5, 0.01, 0.3, 0.1)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 16 in material_manager.materials
    material_data = material_manager.materials[16]
    assert material_data["matType"] == "PM4Sand"
    assert material_data["matTag"] == 16
    assert material_data["D_r"] == 0.5
    assert material_data["G_o"] == 500.0
    assert material_data["h_po"] == 0.75
    assert material_data["Den"] == 1.9
    assert material_data["P_atm"] == 101.3
    assert material_data["h_o"] == 0.6
    assert material_data["e_max"] == 0.9
    assert material_data["e_min"] == 0.6
    assert material_data["n_b"] == 0.65
    assert material_data["n_d"] == 0.35
    assert material_data["A_do"] == 0.8
    assert material_data["z_max"] == 8.0
    assert material_data["c_z"] == 250.0
    assert material_data["c_e"] == 0.5
    assert material_data["phi_cv"] == 32.0
    assert material_data["nu"] == 0.3
    assert material_data["g_degr"] == 1.0
    assert material_data["c_dr"] == 0.1
    assert material_data["c_kaf"] == 4.0
    assert material_data["Q_bolt"] == 10.0
    assert material_data["R_bolt"] == 1.5
    assert material_data["m_par"] == 0.01
    assert material_data["F_sed"] == 0.3
    assert material_data["p_sed"] == 0.1


def test_handle_PM4Silt(material_manager: MaterialManager) -> None:
    """测试PM4Silt材料的数据处理"""
    cmd = "nDMaterial"
    # 基本参数测试
    args = ("PM4Silt", 17, 70.0, 0.25, 500.0, 0.5, 1.7)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 17 in material_manager.materials
    material_data = material_manager.materials[17]
    assert material_data["matType"] == "PM4Silt"
    assert material_data["matTag"] == 17
    assert material_data["S_u"] == 70.0
    assert material_data["Su_Rat"] == 0.25
    assert material_data["G_o"] == 500.0
    assert material_data["h_po"] == 0.5
    assert material_data["Den"] == 1.7

    # 测试含可选参数
    args = ("PM4Silt", 18, 75.0, 0.3, 550.0, 0.55, 1.8, 0.8, 101.3, 0.3, 0.75, 0.5, 0.9, 0.06, 32.0, 0.8, 0.5, 0.3, 0.8, 0.98, 5.0, 100.0, 0.8, 3.0, 4.0, 0.01, 2.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 18 in material_manager.materials
    material_data = material_manager.materials[18]
    assert material_data["matType"] == "PM4Silt"
    assert material_data["matTag"] == 18
    assert material_data["S_u"] == 75.0
    assert material_data["Su_Rat"] == 0.3
    assert material_data["G_o"] == 550.0
    assert material_data["h_po"] == 0.55
    assert material_data["Den"] == 1.8
    assert material_data["Su_factor"] == 0.8
    assert material_data["P_atm"] == 101.3
    assert material_data["nu"] == 0.3
    assert material_data["nG"] == 0.75
    assert material_data["h0"] == 0.5
    assert material_data["eInit"] == 0.9
    assert material_data["lambda"] == 0.06
    assert material_data["phicv"] == 32.0
    assert material_data["nb_wet"] == 0.8
    assert material_data["nb_dry"] == 0.5
    assert material_data["nd"] == 0.3
    assert material_data["Ado"] == 0.8
    assert material_data["ru_max"] == 0.98
    assert material_data["z_max"] == 5.0
    assert material_data["cz"] == 100.0
    assert material_data["ce"] == 0.8
    assert material_data["cgd"] == 3.0
    assert material_data["ckaf"] == 4.0
    assert material_data["m_m"] == 0.01
    assert material_data["CG_consol"] == 2.0


def test_handle_StressDensityModel(material_manager: MaterialManager) -> None:
    """测试StressDensityModel材料的数据处理"""
    cmd = "nDMaterial"
    # 基本参数测试, 包括处理ssls*数组参数和其他特殊参数
    args = ("StressDensityModel", 19, 1.7, 0.8, 400.0, 0.5, 0.3, 0.9, 0.1, 0.7, 0.2, 0.8, 0.3, 0.4, 0.5, 0.03, 0.6, 1.2, 101.3, [0.877, 0.877, 0.873, 0.870, 0.860, 0.850, 0.833], 0.895, 1.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 19 in material_manager.materials
    material_data = material_manager.materials[19]
    assert material_data["matType"] == "StressDensityModel"
    assert material_data["matTag"] == 19
    assert material_data["mDen"] == 1.7
    assert material_data["eNot"] == 0.8
    assert material_data["A"] == 400.0
    assert material_data["n"] == 0.5
    assert material_data["nu"] == 0.3
    assert material_data["a1"] == 0.9
    assert material_data["b1"] == 0.1
    assert material_data["a2"] == 0.7
    assert material_data["b2"] == 0.2
    assert material_data["a3"] == 0.8
    assert material_data["b3"] == 0.3
    assert material_data["fd"] == 0.4
    assert material_data["muNot"] == 0.5
    assert material_data["muCyc"] == 0.03
    assert material_data["sc"] == 0.6
    assert material_data["M"] == 1.2
    assert material_data["patm"] == 101.3
    assert material_data["ssls"] == [0.877, 0.877, 0.873, 0.870, 0.860, 0.850, 0.833]
    assert material_data["hsl"] == 0.895
    assert material_data["p1"] == 1.0


def test_handle_AcousticMedium(material_manager: MaterialManager) -> None:
    """测试AcousticMedium材料的数据处理"""
    cmd = "nDMaterial"
    args = ("AcousticMedium", 20, 2.2e9, 1000.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 20 in material_manager.materials
    material_data = material_manager.materials[20]
    assert material_data["matType"] == "AcousticMedium"
    assert material_data["matTag"] == 20
    assert material_data["K"] == 2.2e9
    assert material_data["rho"] == 1000.0


def test_handle_unknown_standard_model(material_manager: MaterialManager) -> None:
    """测试处理未知的标准材料模型"""
    cmd = "nDMaterial"
    args = ("CustomStandardModel", 21, 10.0, 20.0, 30.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 21 in material_manager.materials
    material_data = material_manager.materials[21]
    assert material_data["matType"] == "CustomStandardModel"
    assert material_data["matTag"] == 21
    assert material_data["materialType"] == cmd
    assert "args" in material_data  # 未知材料应该将额外参数保存在args中
