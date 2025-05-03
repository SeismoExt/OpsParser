import sys
from pathlib import Path

# 将项目根目录添加到 sys.path
project_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(project_root))

print(f"Added {project_root} to sys.path") # 添加打印语句方便调试