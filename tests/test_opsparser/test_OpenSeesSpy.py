# tests/test_opensees/test_spy/test__OpenSeesParser.py
"""
测试OpenSeesParser类
"""
import pytest
import openseespy.opensees as ops
from opsparser import OpenSeesParser, OpenSeesCommand
from opsparser._manager import NodeManager # 显式导入以便类型提示

# 使用 pytest fixture 进行 setup 和 teardown
@pytest.fixture
def spy_instance() -> OpenSeesParser:
    """创建一个 OpenSeesParser 实例并挂钩所有命令"""
    # 清理之前的 OpenSees 模型状态，确保测试隔离
    ops.wipe()
    spy = OpenSeesParser(ops)
    spy.hook_all()
    yield spy # 提供 spy 实例给测试函数
    # 测试结束后取消挂钩
    spy.restore_all()
    ops.wipe() # 再次清理，确保环境干净


def test_model_command(spy_instance: OpenSeesParser):
    """测试 model 命令是否被正确处理"""
    # 模拟调用 ops.model 命令
    ops.model("basic", "-ndm", 3, "-ndf", 6)

    # 检查 spy 的 NodeManager 是否正确记录了模型维度和自由度
    node_manager: NodeManager = OpenSeesCommand.NODE.instance # 获取 NodeManager 实例
    assert node_manager.ndm == 3, "模型维度应为 3"
    assert node_manager.ndf == 6, "模型自由度应为 6"

# TODO: 在这里添加更多测试用例，例如 test_node_command, test_element_command 等
def test_node_command(spy_instance: OpenSeesParser):
    """测试 node 命令是否被正确处理"""
    ops.model("basic", "-ndm", 3, "-ndf", 6)
    # 模拟调用 ops.node 命令
    ops.node(1, 0.0, 0.0, 0.1)

    # 检查 spy 的 NodeManager 是否正确记录了节点信息
    node_manager: NodeManager = OpenSeesCommand.NODE.instance # 获取 NodeManager 实例
    assert len(node_manager.nodes) == 1, "应该有一个节点"
    node = node_manager.nodes[1]
    assert node["coords"] == [0.0, 0.0, 0.1], "节点坐标应为 [0.0, 0.0, 0.1]"
    assert node["ndf"] == 6, "节点自由度应为 2"