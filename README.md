# AHC010 - Loop Lines Solver

ALGO ARTIS Programming Contest 2022（AtCoder Heuristic Contest 010）的 Python 解法与评测脚本。

## 题目概述

- N×N 的网格，每格放有一块瓷砖（共 8 种类型）
- 每块瓷砖上有线路（弯曲线或直线），可以旋转 0/1/2/3 次（每次逆时针 90°）
- 线路无分叉，每条线是路径（path）或环路（cycle）的一部分
- 目标：通过选择每块瓷砖的旋转方式，最大化最长环路（cycle）的长度

## 瓷砖类型

| 编号 | 说明 |
|------|------|
| 0~3 | 一条弯曲线（L 形），旋转后连接不同方向角 |
| 4, 5 | 两条弯曲线，可将两个不同环路合并 |
| 6, 7 | 一条直线，连接对边 |

## 环境要求

- Python 3.10 ~ 3.14
- ale_bench（ALE-Bench 工具包）
- Docker（运行评测容器）
- WSL2（Windows 用户需要）

## 安装

### Linux / WSL

**1. 安装 Docker**

按照 [docker.com 官方文档](https://docs.docker.com/engine/install/) 安装 Docker。

**2. 安装 CairoSVG 系统依赖**

```bash
# Linux / WSL
sudo apt install libcairo2-dev libffi-dev
```

**3. 安装 ALE-Bench Toolkit**

```bash
# 克隆 ALE-Bench 仓库并安装
git clone https://github.com/SakanaAI/ALE-Bench.git ~/ALE-Bench
cd ~/ALE-Bench

# 创建虚拟环境
python3 -m venv ~/ale-bench-env
source ~/ale-bench-env/bin/activate

# 安装（含评测依赖）
pip install ".[eval]"
```

**4. 构建 Docker 镜像**

```bash
cd ~/ALE-Bench

# 构建所有评测镜像
bash ./scripts/docker_build_all.sh $(id -u) $(id -g)

# 或仅构建指定版本
bash ./scripts/docker_build_202301.sh $(id -u) $(id -g)
```

## 使用方法

### Linux / WSL（在终端内）

```bash
# 激活环境
source ~/ale-bench-env/bin/activate

cd /path/to/ahc010-solver

# 完整评测（full 版，50 个 case，8 workers）默认
python3 eval.py
```

### Windows（通过 CMD 或 PowerShell 直接调用 WSL）

无需打开 WSL 终端，在 Windows 的 CMD / PowerShell / Terminal 中直接运行：

```powershell
# 完整评测（full 版，50 个 case，8 workers）默认
wsl -e bash -lc "source ~/ale-bench-env/bin/activate && cd /path/to/ahc010-solver && python3 eval.py"
```

> **说明：**
> - `wsl -e bash -lc` 会启动一个 WSL login shell 并执行引号内的命令
> - 将 `/path/to/ahc010-solver` 替换为项目在 WSL 中的实际路径（例如 `/mnt/d/86134/Documents/GitHub/ahc010-solver`）
> - 确保 WSL 中已安装 ale_bench 虚拟环境（见上方安装步骤）

## 解法说明

贪心旋转 + 并查集合并：

1. **端口建模**：每个格子有 4 个方向端口（上/右/下/左），相邻格子之间的对应端口通过并查集预先合并（物理连接）
2. **逐格旋转选择**：对每块瓷砖枚举 4 种旋转，选择能将最多不同连通分量合并（即延伸/合并环路）的旋转方式
3. **贪心应用**：按从左到右、从上到下的顺序处理，每次选最优旋转并立即更新并查集

## 文件结构

```
ahc010-solver/
├── solution.py   # 解法主程序（由 ale_bench 调用）
├── eval.py       # 评测脚本
└── README.md     # 说明文档
```
