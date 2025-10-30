#!/bin/bash

# clone-venv.sh - 克隆 Python venv 虚拟环境（通过重建方式）

set -e  # 遇到错误立即退出

# 检查参数数量
if [ "$#" -ne 2 ]; then
    echo "用法: $0 <源虚拟环境路径> <目标虚拟环境路径>"
    echo "示例: $0 /opt/venv /opt/my_new_env"
    exit 1
fi

OLD_VENV="$1"
NEW_VENV="$2"

# 检查源环境是否存在
if [ ! -d "$OLD_VENV" ]; then
    echo "❌ 错误: 源虚拟环境不存在: $OLD_VENV"
    exit 1
fi

# 检查源环境是否包含 Python 可执行文件
if [ ! -f "$OLD_VENV/bin/python" ]; then
    echo "❌ 错误: $OLD_VENV 不是一个有效的 venv 环境（缺少 bin/python）"
    exit 1
fi

# 检查目标路径是否已存在
if [ -e "$NEW_VENV" ]; then
    echo "❌ 错误: 目标路径已存在: $NEW_VENV"
    echo "请先删除或选择其他名称。"
    exit 1
fi

echo "📦 正在从 $OLD_VENV 克隆到 $NEW_VENV ..."

# 导出依赖
echo "1️⃣ 导出依赖包列表..."
"$OLD_VENV/bin/python" -m pip freeze > /tmp/venv-requirements.txt

# 创建新环境
echo "2️⃣ 创建新的虚拟环境..."
python3 -m venv "$NEW_VENV"

# 安装依赖
echo "3️⃣ 安装依赖包..."
"$NEW_VENV/bin/python" -m pip install -r /tmp/venv-requirements.txt

# 清理临时文件
rm -f /tmp/venv-requirements.txt

echo "✅ 虚拟环境克隆成功！"
echo "👉 激活新环境: source $NEW_VENV/bin/activate"