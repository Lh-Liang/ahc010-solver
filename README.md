# AHC010 - Loop Lines Solver

ALGO ARTIS Programming Contest 2022（AtCoder Heuristic Contest 010）「Loop Lines」的 Python 解法与评测脚本。

## 题目概述

- 30×30 的网格，每格一块瓦片（编号 0~7）
- 8 种瓦片类型：
  - 0~3：含一条弯曲线（L 形角）
  - 4~5：含两条弯曲线
  - 6~7：含一条直线
- 每块瓦片可逆时针旋转 0/1/2/3 次（每次 90°），旋转后编号变化规则：`[1,2,3,0,5,4,7,6]`
- 目标：通过选择每格的旋转次数，**最大化最大两个环路（cycle）的长度之和**

## 输入格式

```
N
[N 行，每行 N 个字符，各字符为瓦片编号 0~7]
```

- N=30（固定）
- 最后一行为 N（即 `4675` 对应 N=30... 实际为 N 单独一行后跟 N 行瓦片数据）

## 输出格式

```
[一行长度 N*N=900 的字符串]
```

- 第 `30*i+j` 个字符为格 (i,j) 的旋转次数 r_{i,j}（0~3）

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
sudo apt install libcairo2-dev libffi-dev
```

**3. 安装 ALE-Bench Toolkit**

```bash
git clone https://github.com/SakanaAI/ALE-Bench.git ~/ALE-Bench
cd ~/ALE-Bench
python3 -m venv ~/ale-bench-env
source ~/ale-bench-env/bin/activate
pip install ".[eval]"
```

**4. 构建 Docker 镜像**

```bash
cd ~/ALE-Bench
bash ./scripts/docker_build_all.sh $(id -u) $(id -g)
```

## 使用方法

### Linux / WSL

```bash
source ~/ale-bench-env/bin/activate
cd /path/to/ahc010-solver
python3 eval.py
```

### Windows（PowerShell 调用 WSL）

```powershell
wsl -e bash -lc "source ~/ale-bench-env/bin/activate && cd /path/to/ahc010-solver && python3 eval.py"
```

## 解法说明

贪心旋转 + 并查集合并：

1. **端口建模**：每格 4 个方向端口（上/右/下/左），相邻格对应端口预先通过并查集合并（物理连通）
2. **逐格旋转选择**：枚举 4 种旋转，选能将最多不同连通分量合并的方案
3. **应用并立即更新**：选定旋转后立即合并对应端口，影响后续格子的决策

## 文件结构

```
ahc010-solver/
├── solution.py   # 解法主程序（由 ale_bench 调用）
├── eval.py       # 评测脚本
└── README.md     # 说明文档
```
