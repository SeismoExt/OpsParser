import openseespy.opensees as ops
import pytest

from opsparser import MaterialManager


@pytest.fixture
def material_manager() -> MaterialManager:
    """每个测试前初始化一个MaterialManager实例"""
    ops.wipe()
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    return MaterialManager()


def test_handle_Hardening(material_manager: MaterialManager) -> None:
    """测试Hardening材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Hardening", 1, 30000.0, 20.0, 10.0, 5.0, 0.3)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 1 in material_manager.materials
    material_data = material_manager.materials[1]
    assert material_data["matType"] == "Hardening"
    assert material_data["matTag"] == 1
    assert material_data["E"] == 30000.0
    assert material_data["sigmaY"] == 20.0
    assert material_data["H_iso"] == 10.0
    assert material_data["H_kin"] == 5.0
    assert material_data["eta"] == 0.3



def test_handle_Cast(material_manager: MaterialManager) -> None:
    """测试Cast材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Cast", 2, 29000.0, 0.03, 0.04, 500.0, 29000.0, 1.0, 0.3, 0.4, 1.0, 2.0, 0.05, 500.0, 0.2, 2.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 2 in material_manager.materials
    material_data = material_manager.materials[2]
    assert material_data["matType"] == "Cast"
    assert material_data["matTag"] == 2
    assert material_data["n"] == 29000.0
    assert material_data["bo"] == 0.03
    assert material_data["h"] == 0.04
    assert material_data["fy"] == 500.0
    assert material_data["E"] == 29000.0
    assert material_data["L"] == 1.0
    assert material_data["b"] == 0.3
    assert material_data["Ro"] == 0.4
    assert material_data["cR1"] == 1.0
    assert material_data["cR2"] == 2.0
    assert material_data["a1"] == 0.05
    assert material_data["a2"] == 500.0
    assert material_data["a3"] == 0.2
    assert material_data["a4"] == 2.0



def test_handle_ViscousDamper(material_manager: MaterialManager) -> None:
    """测试ViscousDamper材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ViscousDamper", 3, 1.5, 1.0, 0.5, 0.5, 0.5, 2.0, 0.7)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 3 in material_manager.materials
    material_data = material_manager.materials[3]
    assert material_data["matType"] == "ViscousDamper"
    assert material_data["matTag"] == 3
    assert material_data["K_el"] == 1.5
    assert material_data["Cd"] == 1.0
    assert material_data["alpha"] == 0.5
    assert material_data["LGap"] == 0.5
    assert material_data["NM"] == 0.5
    assert material_data["RelTol"] == 2.0
    assert material_data["AbsTol"] == 0.7



def test_handle_BilinearOilDamper(material_manager: MaterialManager) -> None:
    """测试BilinearOilDamper材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("BilinearOilDamper", 4, 100.0, 20.0, 200.0, 10.0, 0.5, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 0.8, 2.0, 0.2)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 4 in material_manager.materials
    material_data = material_manager.materials[4]
    assert material_data["matType"] == "BilinearOilDamper"
    assert material_data["matTag"] == 4
    assert material_data["K_el"] == 100.0
    assert material_data["Cd"] == 20.0
    assert material_data["Fr"] == 200.0
    assert material_data["p"] == 10.0



def test_handle_Viscous(material_manager: MaterialManager) -> None:
    """测试Viscous材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Viscous", 5, 15.0, 0.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 5 in material_manager.materials
    material_data = material_manager.materials[5]
    assert material_data["matType"] == "Viscous"
    assert material_data["matTag"] == 5
    assert material_data["C"] == 15.0
    assert material_data["alpha"] == 0.5



def test_handle_BoucWen(material_manager: MaterialManager) -> None:
    """测试BoucWen材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("BoucWen", 3, 2000.0, 50.0, 2.0, 0.75, 0.5, 0.5, 0.5, 10.0, 0.2)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 3 in material_manager.materials
    material_data = material_manager.materials[3]
    assert material_data["matType"] == "BoucWen"
    assert material_data["matTag"] == 3
    assert material_data["alpha"] == 2000.0
    assert material_data["ko"] == 50.0
    assert material_data["n"] == 2.0
    assert material_data["gamma"] == 0.75
    assert material_data["beta"] == 0.5
    assert material_data["Ao"] == 0.5
    assert material_data["deltaA"] == 0.5
    assert material_data["deltaNu"] == 10.0
    assert material_data["deltaEta"] == 0.2



def test_handle_BWBN(material_manager: MaterialManager) -> None:
    """测试BWBN材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("BWBN", 4, 100.0, 1.0, 1.0, 1.5, 0.5, 0.5, 0.5, 0.05, 1.0, 0.2, 0.3, 0.4, 0.5, 10)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 4 in material_manager.materials
    material_data = material_manager.materials[4]
    assert material_data["matType"] == "BWBN"
    assert material_data["matTag"] == 4
    assert material_data["alpha"] == 100.0
    assert material_data["ko"] == 1.0
    assert material_data["n"] == 1.0
    assert material_data["gamma"] == 1.5
    assert material_data["beta"] == 0.5
    assert material_data["Ao"] == 0.5
    assert material_data["q"] == 0.5
    assert material_data["zetas"] == 0.05
    assert material_data["p"] == 1.0
    assert material_data["Shi"] == 0.2
    assert material_data["deltaShi"] == 0.3
    assert material_data["lambda"] == 0.4
    assert material_data["tol"] == 0.5
    assert material_data["maxIter"] == 10



def test_handle_Bilin(material_manager: MaterialManager) -> None:
    """测试Bilin材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Bilin", 6, 29000.0, 0.02, 0.1, 0.1, 1.0, 0.02, 0.3, 0.3, 1.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 6 in material_manager.materials
    material_data = material_manager.materials[6]
    assert material_data["matType"] == "Bilin"
    assert material_data["matTag"] == 6
    assert material_data["K0"] == 29000.0
    assert material_data["as_Plus"] == 0.02
    assert material_data["as_Neg"] == 0.1
    assert material_data["My_Plus"] == 0.1
    assert material_data["My_Neg"] == 1.0



def test_handle_SelfCentering(material_manager: MaterialManager) -> None:
    """测试SelfCentering材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("SelfCentering", 7, 100.0, 20.0, 0.5, 0.6, 0.2, 0.3, 80.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 7 in material_manager.materials
    material_data = material_manager.materials[7]
    assert material_data["matType"] == "SelfCentering"
    assert material_data["matTag"] == 7
    assert material_data["k1"] == 100.0
    assert material_data["k2"] == 20.0
    assert material_data["sigAct"] == 0.5
    assert material_data["beta"] == 0.6
    assert material_data["epsSlip"] == 0.2
    assert material_data["epsBear"] == 0.3
    assert material_data["rBear"] == 80.0



def test_handle_KikuchiAikenHDR(material_manager: MaterialManager) -> None:
    """测试KikuchiAikenHDR材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("KikuchiAikenHDR", 8, 1, 200.0, 20.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 8 in material_manager.materials
    material_data = material_manager.materials[8]
    assert material_data["matType"] == "KikuchiAikenHDR"
    assert material_data["matTag"] == 8
    assert material_data["tp"] == 1
    assert material_data["ar"] == 200.0
    assert material_data["hr"] == 20.0

    # 测试带选项的情况
    args = ("KikuchiAikenHDR", 9, 2, 250.0, 25.0, "-coGHU", 2, 250.0, 25.0, "-coMSS", 1.5, 12.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 9 in material_manager.materials
    material_data = material_manager.materials[9]
    assert material_data["matType"] == "KikuchiAikenHDR"
    assert material_data["matTag"] == 9
    assert material_data["tp"] == 2
    assert material_data["ar"] == 250.0
    assert material_data["hr"] == 25.0
    assert material_data["cg"] == 2
    assert material_data["ch"] == 250.0
    assert material_data["cu"] == 25.0
    assert material_data["rs"] == 1.5
    assert material_data["rf"] == 12.0



def test_handle_Pipe(material_manager: MaterialManager) -> None:
    """测试Pipe材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Pipe", 11, 3, 20.0, 200000.0, 0.3, 1.2e-5, 100.0, 180000.0, 0.3, 1.3e-5, 200.0, 160000.0, 0.28, 1.4e-5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 11 in material_manager.materials
    material_data = material_manager.materials[11]
    assert material_data["matType"] == "Pipe"
    assert material_data["matTag"] == 11
    assert material_data["nt"] == 3
    assert material_data["T1"] == 20.0
    assert material_data["E1"] == 200000.0
    assert material_data["xnu1"] == 0.3
    assert material_data["alpT1"] == 1.2e-5
    assert material_data["T2"] == 100.0
    assert material_data["E2"] == 180000.0
    assert material_data["xnu2"] == 0.3
    assert material_data["alpT2"] == 1.3e-5
    assert material_data["T3"] == 200.0
    assert material_data["E3"] == 160000.0
    assert material_data["xnu3"] == 0.28
    assert material_data["alpT3"] == 1.4e-5



def test_handle_Backbone(material_manager: MaterialManager) -> None:
    """测试Backbone材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Backbone", 12, 13)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 12 in material_manager.materials
    material_data = material_manager.materials[12]
    assert material_data["matType"] == "Backbone"
    assert material_data["matTag"] == 12
    assert material_data["backboneTag"] == 13



def test_handle_PinchingLimitStateMaterial(material_manager: MaterialManager) -> None:
    """测试PinchingLimitStateMaterial材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("PinchingLimitStateMaterial", 14, 1, 2, 3, 4, 5, 6, 0.7, 0.8, 0.9, 0.1, 0.2, 0.3, 
            0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 
            1.0, 1.1, 1.2)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 14 in material_manager.materials
    material_data = material_manager.materials[14]
    assert material_data["matType"] == "PinchingLimitStateMaterial"
    assert material_data["matTag"] == 14
    assert material_data["nodeT"] == 1
    assert material_data["nodeB"] == 2
    assert material_data["driftAxis"] == 3
    assert material_data["Kelas"] == 4
    assert material_data["crvTyp"] == 5
    assert material_data["crvTag"] == 6
    assert material_data["YpinchUPN"] == 0.7
    assert material_data["YpinchRPN"] == 0.8
    assert material_data["XpinchRPN"] == 0.9
    assert material_data["YpinchUNP"] == 0.1
    assert material_data["YpinchRNP"] == 0.2
    assert material_data["XpinchRNP"] == 0.3
    assert material_data["dmgStrsLimE"] == 0.4
    assert material_data["dmgDispMax"] == 0.5
    assert material_data["dmgE1"] == 0.6
    assert material_data["dmgE2"] == 0.7
    assert material_data["dmgE3"] == 0.8
    assert material_data["dmgE4"] == 0.9
    assert material_data["dmgELim"] == 1.0
    assert material_data["dmgR1"] == 0.1
    assert material_data["dmgR2"] == 0.2
    assert material_data["dmgR3"] == 0.3
    assert material_data["dmgR4"] == 0.4
    assert material_data["dmgRLim"] == 0.5
    assert material_data["dmgRCyc"] == 0.6
    assert material_data["dmgS1"] == 0.7
    assert material_data["dmgS2"] == 0.8
    assert material_data["dmgS3"] == 0.9
    assert material_data["dmgS4"] == 1.0
    assert material_data["dmgSLim"] == 1.1
    assert material_data["dmgSCyc"] == 1.2



def test_handle_unknown_other_uniaxial_material(material_manager: MaterialManager) -> None:
    """测试处理未知的单轴材料"""
    cmd = "uniaxialMaterial"
    args = ("CustomUniaxialMaterial", 20, 10.0, 20.0, 30.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 20 in material_manager.materials
    material_data = material_manager.materials[20]
    assert material_data["matType"] == "CustomUniaxialMaterial"
    assert material_data["matTag"] == 20
    assert material_data["materialType"] == cmd
    assert "args" in material_data  # 未知材料应该将额外参数保存在args中


def test_handle_CFSWSWP(material_manager: MaterialManager) -> None:
    """测试CFSWSWP材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("CFSWSWP", 15, 100.0, 1.0, 0.5, 0.7, 0.3, 2.5, 0.6, 0.8, 0.2, 0.15, 0.3, 0.2, 0.1, 0.2, 0.15)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 15 in material_manager.materials
    material_data = material_manager.materials[15]
    assert material_data["matType"] == "CFSWSWP"
    assert material_data["matTag"] == 15
    assert material_data["height"] == 100.0
    assert material_data["width"] == 1.0
    assert material_data["fut"] == 0.5
    assert material_data["tf"] == 0.7
    assert material_data["Ife"] == 0.3
    assert material_data["Ifi"] == 2.5
    assert material_data["ts"] == 0.6
    assert material_data["np"] == 0.8
    assert material_data["ds"] == 0.2
    assert material_data["Vs"] == 0.15
    assert material_data["sc"] == 0.3
    assert material_data["nc"] == 0.2
    assert material_data["type"] == 0.1
    assert material_data["openingArea"] == 0.2
    assert material_data["openingLength"] == 0.15



def test_handle_CFSSSWP(material_manager: MaterialManager) -> None:
    """测试CFSSSWP材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("CFSSSWP", 16, 100.0, 200.0, 500.0, 350.0, 0.5, 1.5, 400.0, 250.0, 0.6, 20, 0.15, 0.3, 0.2, 0.1, 0.25, 0.35)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 16 in material_manager.materials
    material_data = material_manager.materials[16]
    assert material_data["matType"] == "CFSSSWP"
    assert material_data["matTag"] == 16
    assert material_data["height"] == 100.0
    assert material_data["width"] == 200.0
    assert material_data["fuf"] == 500.0
    assert material_data["fyf"] == 350.0
    assert material_data["tf"] == 0.5
    assert material_data["Af"] == 1.5
    assert material_data["fus"] == 400.0
    assert material_data["fys"] == 250.0
    assert material_data["ts"] == 0.6
    assert material_data["np"] == 20
    assert material_data["ds"] == 0.15
    assert material_data["Vs"] == 0.3
    assert material_data["sc"] == 0.2
    assert material_data["dt"] == 0.1
    assert material_data["openingArea"] == 0.25
    assert material_data["openingLength"] == 0.35



def test_handle_Masonry(material_manager: MaterialManager) -> None:
    """测试Masonry材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Masonry", 17, -1000.0, 200.0, -0.002, -0.01, 0.002, 30000.0, 1.0, 1.0, 0.5, 
            -0.003, -0.008, 0.4, 0.3, 1.8, 0.6, 2.0, 0.6, 1.3, 1.8, 1.2, 0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 17 in material_manager.materials
    material_data = material_manager.materials[17]
    assert material_data["matType"] == "Masonry"
    assert material_data["matTag"] == 17
    assert material_data["Fm"] == -1000.0
    assert material_data["Ft"] == 200.0
    assert material_data["Um"] == -0.002
    assert material_data["Uult"] == -0.01
    assert material_data["Ucl"] == 0.002
    assert material_data["Emo"] == 30000.0
    assert material_data["L"] == 1.0
    assert material_data["a1"] == 1.0
    assert material_data["a2"] == 0.5
    assert material_data["D1"] == -0.003
    assert material_data["D2"] == -0.008
    assert material_data["Ach"] == 0.4
    assert material_data["Are"] == 0.3
    assert material_data["Ba"] == 1.8
    assert material_data["Bch"] == 0.6
    assert material_data["Gun"] == 2.0
    assert material_data["Gplu"] == 0.6
    assert material_data["Gplr"] == 1.3
    assert material_data["Exp1"] == 1.8
    assert material_data["Exp2"] == 1.2
    assert material_data["IENV"] == 0



def test_handle_ModIMKPeakOriented(material_manager: MaterialManager) -> None:
    """测试ModIMKPeakOriented材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ModIMKPeakOriented", 21, 29000.0, 0.02, 0.1, 0.1, 1.0, 0.02, 0.3, 0.3, 1.0, 
            0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 21 in material_manager.materials
    material_data = material_manager.materials[21]
    assert material_data["matType"] == "ModIMKPeakOriented"
    assert material_data["matTag"] == 21
    assert material_data["K0"] == 29000.0
    assert material_data["as_Plus"] == 0.02
    assert material_data["as_Neg"] == 0.1
    assert material_data["My_Plus"] == 0.1
    assert material_data["My_Neg"] == 1.0
    assert material_data["Lamda_S"] == 0.02
    assert material_data["Lamda_C"] == 0.3
    assert material_data["Lamda_A"] == 0.3
    assert material_data["Lamda_K"] == 1.0
    assert material_data["c_S"] == 0.1
    assert material_data["c_C"] == 0.2
    assert material_data["c_A"] == 0.3
    assert material_data["c_K"] == 0.4
    assert material_data["theta_p_Plus"] == 0.5
    assert material_data["theta_p_Neg"] == 0.6
    assert material_data["theta_pc_Plus"] == 0.7
    assert material_data["theta_pc_Neg"] == 0.8
    assert material_data["Res_Pos"] == 0.9
    assert material_data["Res_Neg"] == 1.0
    assert material_data["theta_u_Plus"] == 1.1
    assert material_data["theta_u_Neg"] == 1.2
    assert material_data["D_Plus"] == 1.3
    assert material_data["D_Neg"] == 1.4



def test_handle_ModIMKPinching(material_manager: MaterialManager) -> None:
    """测试ModIMKPinching材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ModIMKPinching", 22, 29000.0, 0.02, 0.1, 0.1, 1.0, 0.02, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 22 in material_manager.materials
    material_data = material_manager.materials[22]
    assert material_data["matType"] == "ModIMKPinching"
    assert material_data["matTag"] == 22
    assert material_data["K0"] == 29000.0
    assert material_data["as_Plus"] == 0.02
    assert material_data["as_Neg"] == 0.1
    assert material_data["My_Plus"] == 0.1
    assert material_data["My_Neg"] == 1.0
    assert material_data["FprPos"] == 0.02
    assert material_data["FprNeg"] == 0.3
    assert material_data["A_pinch"] == 0.4
    assert material_data["Lamda_S"] == 0.5
    assert material_data["Lamda_C"] == 0.6
    assert material_data["Lamda_A"] == 0.7
    assert material_data["Lamda_K"] == 0.8
    assert material_data["c_S"] == 0.9
    assert material_data["c_C"] == 1.0
    assert material_data["c_A"] == 1.1
    assert material_data["c_K"] == 1.2
    assert material_data["theta_p_Plus"] == 1.3
    assert material_data["theta_p_Neg"] == 1.4
    assert material_data["theta_pc_Plus"] == 1.5
    assert material_data["theta_pc_Neg"] == 1.6
    assert material_data["Res_Pos"] == 1.7
    assert material_data["Res_Neg"] == 1.8
    assert material_data["theta_u_Plus"] == 1.9
    assert material_data["theta_u_Neg"] == 2.0
    assert material_data["D_Plus"] == 2.1
    assert material_data["D_Neg"] == 2.2



def test_handle_SAWS(material_manager: MaterialManager) -> None:
    """测试SAWS材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("SAWS", 23, 1.0, 2.0, 3.0, 4.0, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 23 in material_manager.materials
    material_data = material_manager.materials[23]
    assert material_data["matType"] == "SAWS"
    assert material_data["matTag"] == 23
    assert material_data["F0"] == 1.0
    assert material_data["FI"] == 2.0
    assert material_data["DU"] == 3.0
    assert material_data["S0"] == 4.0
    assert material_data["R1"] == 0.5
    assert material_data["R2"] == 0.6
    assert material_data["R3"] == 0.7
    assert material_data["R4"] == 0.8
    assert material_data["alpha"] == 0.9
    assert material_data["beta"] == 0.1



def test_handle_BarSlip(material_manager: MaterialManager) -> None:
    """测试BarSlip材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("BarSlip", 24, 30.0, 60000.0, 29000.0, 90000.0, 29000.0, 1.0, 24.0, 2, 24.0, 18.0, 1.0, 1, 1, "Damage", "psi")
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 24 in material_manager.materials
    material_data = material_manager.materials[24]
    assert material_data["matType"] == "BarSlip"
    assert material_data["matTag"] == 24
    assert material_data["fc"] == 30.0
    assert material_data["fy"] == 60000.0
    assert material_data["Es"] == 29000.0
    assert material_data["fu"] == 90000.0
    assert material_data["Eh"] == 29000.0
    assert material_data["db"] == 1.0
    assert material_data["ld"] == 24.0
    assert material_data["nb"] == 2
    assert material_data["depth"] == 24.0
    assert material_data["height"] == 18.0
    assert material_data["ancLratio"] == 1.0
    assert material_data["bsFlag"] == 1
    assert material_data["type"] == 1
    assert material_data["damage"] == "Damage"
    assert material_data["unit"] == "psi"



def test_handle_Bond_SP01(material_manager: MaterialManager) -> None:
    """测试Bond_SP01材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Bond_SP01", 25, 600.0, 0.4, 1000.0, 0.9, 0.5, 0.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 25 in material_manager.materials
    material_data = material_manager.materials[25]
    assert material_data["matType"] == "Bond_SP01"
    assert material_data["matTag"] == 25
    assert material_data["Fy"] == 600.0
    assert material_data["Sy"] == 0.4
    assert material_data["Fu"] == 1000.0
    assert material_data["Su"] == 0.9
    assert material_data["b"] == 0.5
    assert material_data["R"] == 0.5



def test_handle_Fatigue(material_manager: MaterialManager) -> None:
    """测试Fatigue材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Fatigue", 26, 1, "-E0", 0.191, "-m", -0.458, "-min", -1e16, "-max", 1e16)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 26 in material_manager.materials
    material_data = material_manager.materials[26]
    assert material_data["matType"] == "Fatigue"
    assert material_data["matTag"] == 26
    assert material_data["otherTag"] == 1
    assert material_data["E0"] == 0.191
    assert material_data["m"] == -0.458
    assert material_data["min"] == -1e16
    assert material_data["max"] == 1e16



def test_handle_ImpactMaterial(material_manager: MaterialManager) -> None:
    """测试ImpactMaterial材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ImpactMaterial", 27, 5.0e6, 5.0e5, 1.0e6, 1.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 27 in material_manager.materials
    material_data = material_manager.materials[27]
    assert material_data["matType"] == "ImpactMaterial"
    assert material_data["matTag"] == 27
    assert material_data["K1"] == 5.0e6
    assert material_data["K2"] == 5.0e5
    assert material_data["sigy"] == 1.0e6
    assert material_data["gap"] == 1.0



def test_handle_HyperbolicGapMaterial(material_manager: MaterialManager) -> None:
    """测试HyperbolicGapMaterial材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("HyperbolicGapMaterial", 28, 1000.0, 500.0, 0.7, 1000.0, 0.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 28 in material_manager.materials
    material_data = material_manager.materials[28]
    assert material_data["matType"] == "HyperbolicGapMaterial"
    assert material_data["matTag"] == 28
    assert material_data["Kmax"] == 1000.0
    assert material_data["Kur"] == 500.0
    assert material_data["Rf"] == 0.7
    assert material_data["Fult"] == 1000.0
    assert material_data["gap"] == 0.5



def test_handle_LimitState(material_manager: MaterialManager) -> None:
    """测试LimitState材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("LimitState", 29, 0.5, 0.01, 0.6, 0.02, 0.1, 0.05, -0.5, -0.01, -0.6, -0.02, -0.1, -0.05, 0.8, 0.8, 0.0, 0.0, 0.0, 0, 0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 29 in material_manager.materials
    material_data = material_manager.materials[29]
    assert material_data["matType"] == "LimitState"
    assert material_data["matTag"] == 29
    assert material_data["s1p"] == 0.5
    assert material_data["e1p"] == 0.01
    assert material_data["s2p"] == 0.6
    assert material_data["e2p"] == 0.02
    assert material_data["s3p"] == 0.1
    assert material_data["e3p"] == 0.05
    assert material_data["s1n"] == -0.5
    assert material_data["e1n"] == -0.01
    assert material_data["s2n"] == -0.6
    assert material_data["e2n"] == -0.02
    assert material_data["s3n"] == -0.1
    assert material_data["e3n"] == -0.05
    assert material_data["pinchX"] == 0.8
    assert material_data["pinchY"] == 0.8
    assert material_data["damage1"] == 0.0
    assert material_data["damage2"] == 0.0
    assert material_data["beta"] == 0.0
    assert material_data["curveTag"] == 0
    assert material_data["curveType"] == 0



def test_handle_MinMax(material_manager: MaterialManager) -> None:
    """测试MinMax材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("MinMax", 30, 1, "-min", -0.01, "-max", 0.01)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 30 in material_manager.materials
    material_data = material_manager.materials[30]
    assert material_data["matType"] == "MinMax"
    assert material_data["matTag"] == 30
    assert material_data["otherTag"] == 1
    assert material_data["minStrain"] == -0.01
    assert material_data["maxStrain"] == 0.01



def test_handle_ElasticBilin(material_manager: MaterialManager) -> None:
    """测试ElasticBilin材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ElasticBilin", 31, 29000.0, 5000.0, 0.01)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 31 in material_manager.materials
    material_data = material_manager.materials[31]
    assert material_data["matType"] == "ElasticBilin"
    assert material_data["matTag"] == 31
    assert material_data["EP1"] == 29000.0
    assert material_data["EP2"] == 5000.0
    assert material_data["epsP2"] == 0.01



def test_handle_ElasticMultiLinear(material_manager: MaterialManager) -> None:
    """测试ElasticMultiLinear材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ElasticMultiLinear", 32, 0.5, "-strain", -0.02, 0.0, 0.02, "-stress", -50.0, 0.0, 50.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 32 in material_manager.materials
    material_data = material_manager.materials[32]
    assert material_data["matType"] == "ElasticMultiLinear"
    assert material_data["matTag"] == 32
    assert material_data["eta"] == 0.5
    assert material_data["strain"] == [-0.02, 0.0, 0.02]
    assert material_data["stress"] == [-50.0, 0.0, 50.0]



def test_handle_MultiLinear(material_manager: MaterialManager) -> None:
    """测试MultiLinear材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("MultiLinear", 33, -0.02, -50.0, 0.0, 0.0, 0.02, 50.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 33 in material_manager.materials
    material_data = material_manager.materials[33]
    assert material_data["matType"] == "MultiLinear"
    assert material_data["matTag"] == 33
    assert material_data["pts"] == [-0.02, -50.0, 0.0, 0.0, 0.02, 50.0]



def test_handle_InitStrainMaterial(material_manager: MaterialManager) -> None:
    """测试InitStrainMaterial材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("InitStrainMaterial", 34, 1, 0.005)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 34 in material_manager.materials
    material_data = material_manager.materials[34]
    assert material_data["matType"] == "InitStrainMaterial"
    assert material_data["matTag"] == 34
    assert material_data["otherTag"] == 1
    assert material_data["initStrain"] == 0.005



def test_handle_InitStressMaterial(material_manager: MaterialManager) -> None:
    """测试InitStressMaterial材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("InitStressMaterial", 35, 1, 100.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 35 in material_manager.materials
    material_data = material_manager.materials[35]
    assert material_data["matType"] == "InitStressMaterial"
    assert material_data["matTag"] == 35
    assert material_data["otherTag"] == 1
    assert material_data["initStress"] == 100.0



def test_handle_PathIndependent(material_manager: MaterialManager) -> None:
    """测试PathIndependent材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("PathIndependent", 36, 1)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 36 in material_manager.materials
    material_data = material_manager.materials[36]
    assert material_data["matType"] == "PathIndependent"
    assert material_data["matTag"] == 36
    assert material_data["OtherTag"] == 1



def test_handle_Pinching4(material_manager: MaterialManager) -> None:
    """测试Pinching4材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("Pinching4", 37, 10.0, 0.1, 15.0, 0.2, 0.5, 0.3, 0.4, 0.4, 
            -10.0, -0.1, -15.0, -0.2, -0.5, -0.3, -0.4, -0.4,
            0.5, 0.6, 0.7, 0.5, 0.6, 0.7,
            1.0, 1.1, 1.2, 1.3, 1.4, 2.0, 2.1, 2.2, 2.3, 2.4,
            3.0, 3.1, 3.2, 3.3, 3.4, 0.8, "cycle")
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 37 in material_manager.materials
    material_data = material_manager.materials[37]
    assert material_data["matType"] == "Pinching4"
    assert material_data["matTag"] == 37
    # Positive envelope points
    assert material_data["ePf1"] == 10.0
    assert material_data["ePd1"] == 0.1
    assert material_data["ePf2"] == 15.0
    assert material_data["ePd2"] == 0.2
    assert material_data["ePf3"] == 0.5
    assert material_data["ePd3"] == 0.3
    assert material_data["ePf4"] == 0.4
    assert material_data["ePd4"] == 0.4
    # Negative envelope points
    assert material_data["eNf1"] == -10.0
    assert material_data["eNd1"] == -0.1
    assert material_data["eNf2"] == -15.0
    assert material_data["eNd2"] == -0.2
    assert material_data["eNf3"] == -0.5
    assert material_data["eNd3"] == -0.3
    assert material_data["eNf4"] == -0.4
    assert material_data["eNd4"] == -0.4
    # Unloading/reloading parameters
    assert material_data["rDispP"] == 0.5
    assert material_data["rForceP"] == 0.6
    assert material_data["uForceP"] == 0.7
    assert material_data["rDispN"] == 0.5
    assert material_data["rForceN"] == 0.6
    assert material_data["uForceN"] == 0.7
    # Degradation parameters
    assert material_data["gK1"] == 1.0
    assert material_data["gK2"] == 1.1
    assert material_data["gK3"] == 1.2
    assert material_data["gK4"] == 1.3
    assert material_data["gKLim"] == 1.4
    assert material_data["gD1"] == 2.0
    assert material_data["gD2"] == 2.1
    assert material_data["gD3"] == 2.2
    assert material_data["gD4"] == 2.3
    assert material_data["gDLim"] == 2.4
    assert material_data["gF1"] == 3.0
    assert material_data["gF2"] == 3.1
    assert material_data["gF3"] == 3.2
    assert material_data["gF4"] == 3.3
    assert material_data["gFLim"] == 3.4
    assert material_data["gE"] == 0.8
    assert material_data["dmgType"] == "cycle"



def test_handle_ECC01(material_manager: MaterialManager) -> None:
    """测试ECC01材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("ECC01", 38, 30.0, 0.002, 35.0, 0.005, 0.01, -40.0, -0.003, -0.01, 0.5, 0.7, 0.3, 0.2, 0.1, 0.4)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 38 in material_manager.materials
    material_data = material_manager.materials[38]
    assert material_data["matType"] == "ECC01"
    assert material_data["matTag"] == 38
    assert material_data["sigt0"] == 30.0
    assert material_data["epst0"] == 0.002
    assert material_data["sigt1"] == 35.0
    assert material_data["epst1"] == 0.005
    assert material_data["epst2"] == 0.01
    assert material_data["sigc0"] == -40.0
    assert material_data["epsc0"] == -0.003
    assert material_data["epsc1"] == -0.01
    assert material_data["alphaT1"] == 0.5
    assert material_data["alphaT2"] == 0.7
    assert material_data["alphaC"] == 0.3
    assert material_data["alphaCU"] == 0.2
    assert material_data["betaT"] == 0.1
    assert material_data["betaC"] == 0.4



def test_handle_KikuchiAikenLRB(material_manager: MaterialManager) -> None:
    """测试KikuchiAikenLRB材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("KikuchiAikenLRB", 39, 1, 100.0, 10.0, 20.0, 0.1, 0.01, 0.5, 2.0)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 39 in material_manager.materials
    material_data = material_manager.materials[39]
    assert material_data["matType"] == "KikuchiAikenLRB"
    assert material_data["matTag"] == 39
    assert material_data["type"] == 1
    assert material_data["ar"] == 100.0
    assert material_data["hr"] == 10.0
    assert material_data["gr"] == 20.0
    assert material_data["ap"] == 0.1
    assert material_data["tp"] == 0.01
    assert material_data["alph"] == 0.5
    assert material_data["beta"] == 2.0

    # 测试带选项的情况
    args = ("KikuchiAikenLRB", 40, 2, 200.0, 20.0, 30.0, 0.2, 0.02, 0.6, 3.0, 
            "-T", 25.0, "-coKQ", 0.8, 0.9, "-coMSS", 1.2, 1.3)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 40 in material_manager.materials
    material_data = material_manager.materials[40]
    assert material_data["matType"] == "KikuchiAikenLRB"
    assert material_data["matTag"] == 40
    assert material_data["type"] == 2
    assert material_data["temp"] == 25.0
    assert material_data["rk"] == 0.8
    assert material_data["rq"] == 0.9
    assert material_data["rs"] == 1.2
    assert material_data["rf"] == 1.3



def test_handle_AxialSp(material_manager: MaterialManager) -> None:
    """测试AxialSp材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("AxialSp", 40, 100.0, 10.0, 1.0, 0.2, 0.3, 0.1, 0.4, 0.5, 0.1, 5, 1.0, 0.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 40 in material_manager.materials
    material_data = material_manager.materials[40]
    assert material_data["matType"] == "AxialSp"
    assert material_data["matTag"] == 40
    assert material_data["sce"] == 100.0
    assert material_data["fty"] == 10.0
    assert material_data["fcy"] == 1.0
    assert material_data["bte"] == 0.2



def test_handle_AxialSpHD(material_manager: MaterialManager) -> None:
    """测试AxialSpHD材料的数据处理"""
    cmd = "uniaxialMaterial"
    args = ("AxialSpHD", 41, 100.0, 10.0, 1.0, 0.2, 0.3, 0.1, 0.4, 0.5, 0.1, 5, 1.0, 0.5, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5)
    material_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 41 in material_manager.materials
    material_data = material_manager.materials[41]
    assert material_data["matType"] == "AxialSpHD"
    assert material_data["matTag"] == 41
    assert material_data["sce"] == 100.0
    assert material_data["fty"] == 10.0
    assert material_data["fcy"] == 1.0
    assert material_data["bte"] == 0.2

