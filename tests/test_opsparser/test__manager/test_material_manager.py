from typing import Any, Optional

import pytest

from opsparser import MaterialManager


@pytest.fixture
def material_manager() -> MaterialManager:
    """每个测试前初始化一个MaterialManager实例, 并添加默认材料"""
    material_manager = MaterialManager()
    material_manager.clear()
    # 添加默认材料1
    func_name = "uniaxialMaterial"
    args = ("Steel01", 1, 420.0, 200000.0, 0.01, 0.5, 1.0, 0.0, 1.0)
    material_manager.handle(func_name, {"args": args, "kwargs": {}})
    
    # 添加默认材料2
    func_name = "nDMaterial"
    args = ("ElasticIsotropic", 2, 2.0e5, 0.3, 7.85e-9)
    material_manager.handle(func_name, {"args": args, "kwargs": {}})
    
    return material_manager

@pytest.fixture
def empty_material_manager() -> MaterialManager:
    """部分测试前初始化一个空的MaterialManager实例"""
    material_manager = MaterialManager()
    material_manager.clear()
    return material_manager

def test_handles(material_manager: MaterialManager):
    """测试handles方法"""
    expected_commands = ["uniaxialMaterial", "nDMaterial"]
    assert sorted(material_manager.handles()) == sorted(expected_commands)

def test_handle_uniaxial_material(empty_material_manager: MaterialManager):
    """测试处理uniaxialMaterial命令"""
    # 模拟参数
    func_name = "uniaxialMaterial"
    args = ("Steel01", 1, 420.0, 200000.0, 0.01, 0.5, 1.0, 0.0, 1.0)
    empty_material_manager.handle(func_name, {"args": args, "kwargs": {}})

    # 检查材料是否正确存储
    assert 1 in empty_material_manager.materials
    material_data = empty_material_manager.materials[1]
    assert material_data["matType"] == "Steel01"
    assert material_data["matTag"] == 1
    assert material_data["Fy"] == 420.0
    assert material_data["E0"] == 200000.0
    assert material_data["b"] == 0.01

def test_handle_nd_material(empty_material_manager: MaterialManager):
    """测试处理nDMaterial命令"""
    # 模拟参数
    func_name = "nDMaterial"
    args = ("ElasticIsotropic", 2, 2.0e5, 0.3, 7.85e-9)

    # 调用待测试方法
    empty_material_manager.handle(func_name, {"args": args, "kwargs": {}})

    # 验证结果
    assert 2 in empty_material_manager.materials
    material = empty_material_manager.materials[2]
    assert material["matType"] == "ElasticIsotropic"
    assert material["matTag"] == 2
    assert material["E"] == 2.0e5
    assert material["nu"] == 0.3
    assert material["rho"] == 7.85e-9

def test_get_material(material_manager: MaterialManager):
    """测试获取材料信息"""
    # 测试获取已有材料
    material = material_manager.get_material(1)
    assert material is not None
    assert material["matType"] == "Steel01"

    # 测试获取不存在的材料
    material = material_manager.get_material(999)
    assert material is None

def test_get_materials_by_type(material_manager: MaterialManager):
    """测试按类型获取材料"""
    # 测试按类型查询
    materials = material_manager.get_materials_by_type("Steel01")
    assert len(materials) == 1
    assert 1 in materials

    # 测试大小写不敏感
    materials = material_manager.get_materials_by_type("steel01")
    assert len(materials) == 1
    assert 1 in materials

    # 测试不存在的类型
    materials = material_manager.get_materials_by_type("NonExistentType")
    assert len(materials) == 0

def test_get_materials_by_command_type(material_manager: MaterialManager):
    """测试按命令类型获取材料"""
    # 测试按命令类型查询
    materials = material_manager.uniaxialMaterial
    assert len(materials) == 1
    assert 1 in materials

    materials = material_manager.nDMaterial
    assert len(materials) == 1
    assert 2 in materials

def test_get_materials(material_manager: MaterialManager):
    """测试获取材料列表"""
    # 测试获取全部材料
    materials = material_manager.materials
    assert len(materials) == 2
    assert 1 in materials
    assert materials[1]["matType"] == "Steel01"
    assert 2 in materials
    assert materials[2]["matType"] == "ElasticIsotropic"


def test_clear(material_manager: MaterialManager):
    """测试清除功能"""
    assert len(material_manager.materials) > 0

    # 清除
    material_manager.clear()
    assert len(material_manager.materials) == 0
