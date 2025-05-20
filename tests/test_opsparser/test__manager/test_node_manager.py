from typing import Any, Dict, List, Optional

import pytest

from opsparser import BaseHandler, NodeManager


@pytest.fixture
def node_manager() -> NodeManager:
    """每个测试前初始化一个NodeManager实例"""
    node_manager = NodeManager()
    node_manager.clear()
    return node_manager

def test_handle_node(node_manager: NodeManager) -> None:
    """测试节点数据处理功能"""
    # 2D节点情况
    cmd = "node"
    args = (1, 10.0, 20.0)
    node_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查节点是否正确存储
    assert 1 in node_manager.nodes
    node_data = node_manager.nodes[1]
    assert node_data["coords"] == [10.0, 20.0]

    # 3D节点情况
    cmd = "node"
    args = (2, 10.0, 20.0, 30.0, "-ndf", 6)
    node_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查节点是否正确存储
    assert 2 in node_manager.nodes
    node_data = node_manager.nodes[2]
    assert node_data["coords"] == [10.0, 20.0, 30.0]
    assert node_data["ndf"] == 6


def test_node_with_additional_params(node_manager: NodeManager) -> None:
    """测试带有额外参数的节点处理"""
    cmd = "node"
    # 节点带有质量、位移、速度和加速度参数
    args = (3, 10.0, 20.0, 30.0, "-ndf", 3, "-mass", 1.0, 2.0, 3.0, 
            "-disp", 0.1, 0.2, 0.3, "-vel", 0.01, 0.02, 0.03, "-accel", 0.001, 0.002, 0.003)
    node_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查节点是否正确存储所有参数
    assert 3 in node_manager.nodes
    node_data = node_manager.nodes[3]
    assert node_data["coords"] == [10.0, 20.0, 30.0]
    assert node_data["ndf"] == 3
    assert node_data["mass"] == [1.0, 2.0, 3.0]
    assert node_data["disp"] == [0.1, 0.2, 0.3]
    assert node_data["vel"] == [0.01, 0.02, 0.03]
    assert node_data["accel"] == [0.001, 0.002, 0.003]


def test_handle_mass(node_manager: NodeManager) -> None:
    """测试质量处理功能"""
    # 先创建节点
    cmd = "node"
    args = (1, 10.0, 20.0)
    node_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 添加质量
    cmd = "mass"
    args = (1, 1.5, 2.5, 3.5)
    node_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查质量是否正确存储
    assert 1 in node_manager.nodes
    node_data = node_manager.nodes[1]
    assert "mass" in node_data
    assert node_data["mass"] == [1.5, 2.5, 3.5]


def test_handle_model(node_manager: NodeManager) -> None:
    """测试模型设置处理功能"""
    cmd = "model"
    args = ("basic", "-ndm", 3, "-ndf", 6)
    node_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 检查模型维度和自由度是否正确设置
    assert node_manager.ndm == 3
    assert node_manager.ndf == 6


def test_get_node_coords(node_manager: NodeManager) -> None:
    """测试获取节点坐标功能"""
    # 创建测试节点
    cmd = "node"
    args = (1, 10.0, 20.0, 30.0)
    node_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 测试获取坐标
    coords = node_manager.get_node_coords(1)
    assert coords == [10.0, 20.0, 30.0]

    # 测试获取不存在节点的坐标
    coords = node_manager.get_node_coords(999)
    assert coords == []


def test_get_node_mass(node_manager: NodeManager) -> None:
    """测试获取节点质量功能"""
    # 先创建模型
    cmd = "model"
    args = ("basic", "-ndm", 2, "-ndf", 3)
    node_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 创建节点并设置质量
    cmd = "node"
    args = (1, 10.0, 20.0, "-mass", *[1.5, 2.5, 0])
    node_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 测试获取质量
    mass = node_manager.get_node_mass(1)
    assert mass == [1.5, 2.5, 0]

    # 测试获取不存在节点的质量
    mass = node_manager.get_node_mass(999)
    assert mass == []

    # 测试获取没有质量属性的节点
    cmd = "node"
    args = (2, 10.0, 20.0)
    node_manager.handle(cmd, {"args": args, "kwargs": {}})

    mass = node_manager.get_node_mass(2)
    assert mass == []


def test_get_nodes_by_coords(node_manager: NodeManager) -> None:
    """测试通过坐标查找节点功能"""
    # 创建测试节点
    cmd = "node"
    args1 = (1, 10.0, 20.0, 30.0)
    args2 = (2, 10.0, 20.0, 40.0)
    args3 = (3, 20.0, 30.0, 40.0)

    for args in [args1, args2, args3]:
        node_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 测试通过x坐标查询
    nodes = node_manager.get_nodes_by_coords(x=10.0)
    assert set(nodes) == {1, 2}

    # 测试通过x,y坐标查询
    nodes = node_manager.get_nodes_by_coords(x=10.0, y=20.0)
    assert set(nodes) == {1, 2}

    # 测试通过完整坐标查询
    nodes = node_manager.get_nodes_by_coords(x=10.0, y=20.0, z=30.0)
    assert set(nodes) == {1}

    # 测试无匹配情况
    nodes = node_manager.get_nodes_by_coords(x=99.0)
    assert nodes == []


def test_clear(node_manager: NodeManager) -> None:
    """测试清除功能"""
    # 先创建一些节点和设置模型参数
    cmd = "model"
    args = ("basic", "-ndm", 3, "-ndf", 6)
    node_manager.handle(cmd, {"args": args, "kwargs": {}})

    cmd = "node"
    args = (1, 10.0, 20.0, 30.0)
    node_manager.handle(cmd, {"args": args, "kwargs": {}})

    # 验证数据存在
    assert node_manager.ndm == 3
    assert node_manager.ndf == 6
    assert len(node_manager.nodes) == 1

    # 清除数据
    node_manager.clear()

    # 验证数据被清除
    assert node_manager.ndm == 0
    assert node_manager.ndf == 0
    assert len(node_manager.nodes) == 0


def test_handles(node_manager: NodeManager) -> None:
    """测试handles方法"""
    handles = node_manager.handles()
    assert isinstance(handles, list)
    assert "node" in handles
    assert "mass" in handles
    assert "model" in handles