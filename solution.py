"""
AHC010 - Loop Lines (ALGO ARTIS Programming Contest 2022)
解法思路：贪心旋转合并环路
  - 每块瓷砖有固定的连线结构，可旋转 0/1/2/3 次（每次逆时针 90°）
  - 用并查集追踪当前各环路/路径的连通情况
  - 对每块瓷砖，枚举 4 种旋转，选择能合并最多不同连通分量（即延伸环路）的旋转
  - 最终找到最大环路，输出每块瓷砖的旋转次数

瓷砖编号说明（输入给出的是旋转前的编号 0~7）：
  0~3: 一条弯曲线（L 形），旋转后分别连接 (上,右),(右,下),(下,左),(左,上)
  4,5: 两条弯曲线，4 连接 (上,右)+(下,左)，5 连接 (上,左)+(下,右)
  6,7: 一条直线，6 连接 (上,下)，7 连接 (左,右)

连接方向编码：0=上, 1=右, 2=下, 3=左
"""

import sys
from collections import defaultdict

input = sys.stdin.readline

# 每种瓷砖旋转 0 次时的连接对 [(方向a, 方向b), ...]
# 旋转 1 次（逆时针 90°）：方向 d -> (d+1)%4
TILE_CONNECTIONS = {
    0: [(0, 1)],          # 上-右
    1: [(1, 2)],          # 右-下
    2: [(2, 3)],          # 下-左
    3: [(3, 0)],          # 左-上
    4: [(0, 1), (2, 3)],  # 上-右 + 下-左
    5: [(0, 3), (1, 2)],  # 上-左 + 右-下
    6: [(0, 2)],          # 上-下
    7: [(1, 3)],          # 左-右
}

# 旋转后瓷砖编号（逆时针 90°）
ROTATE_MAP = [1, 2, 3, 0, 5, 4, 7, 6]


def get_connections(tile_type, rot):
    """获取旋转 rot 次后的连接对（方向编码）"""
    t = tile_type
    for _ in range(rot):
        t = ROTATE_MAP[t]
    # 旋转方向偏移
    return [((a + rot) % 4, (b + rot) % 4) for a, b in TILE_CONNECTIONS[tile_type]]


def solve():
    N = int(input())
    grid = []
    for _ in range(N):
        row = list(map(int, input().split()))
        grid.append(row)

    # 每格有 4 个端口，节点编号：(r, c, dir) -> r*N*4 + c*4 + dir
    def node_id(r, c, d):
        return (r * N + c) * 4 + d

    total_nodes = N * N * 4
    parent = list(range(total_nodes))
    rank = [0] * total_nodes

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1
        return True

    # 相邻格子之间的端口连接（物理连接，固定不变）
    # 上方格子的"下"端口 = 当前格子的"上"端口
    # 方向：0=上, 1=右, 2=下, 3=左；对面方向 = (d+2)%4
    OPPOSITE = [2, 3, 0, 1]
    DR = [-1, 0, 1, 0]
    DC = [0, 1, 0, -1]

    def connect_neighbors():
        """将相邻格子互相对应的端口连入同一并查集节点"""
        for r in range(N):
            for c in range(N):
                for d in range(4):
                    nr, nc = r + DR[d], c + DC[d]
                    if 0 <= nr < N and 0 <= nc < N:
                        union(node_id(r, c, d), node_id(nr, nc, OPPOSITE[d]))

    connect_neighbors()

    # 对每块瓷砖，选择旋转次数
    rotations = [[0] * N for _ in range(N)]

    for r in range(N):
        for c in range(N):
            tile = grid[r][c]
            best_rot = 0
            best_score = -1
            for rot in range(4):
                conns = get_connections(tile, rot)
                score = 0
                for a, b in conns:
                    na, nb = find(node_id(r, c, a)), find(node_id(r, c, b))
                    if na != nb:
                        score += 1
                if score > best_score:
                    best_score = score
                    best_rot = rot

            rotations[r][c] = best_rot
            # 应用选定的旋转，合并端口
            for a, b in get_connections(tile, best_rot):
                union(node_id(r, c, a), node_id(r, c, b))

    # 输出：每行 N 个旋转次数
    for r in range(N):
        print(*rotations[r])


solve()
