"""
AHC010 - Loop Lines
解法思路：贪心旋转 + 并查集合并环路

题目：
  - N×N (N=30) 网格，每格有一块瓦片（编号 0~7）
  - 8 种瓦片：0~3 含一条弯曲线，4~5 含两条弯曲线，6~7 含一条直线
  - 每块瓦片可逆时针旋转 0/1/2/3 次（每次 90°）
  - 旋转后编号变化：[1,2,3,0,5,4,7,6]（逆时针一次）
  - 目标：最大化最长环路（cycle）的长度
  - 得分基于最大的两个环路

策略：
  用并查集追踪端口连通性，逐格枚举 4 种旋转，选能合并最多不同连通分量的旋转

瓦片连接方向：0=上, 1=右, 2=下, 3=左
各瓦片旋转 0 次时的连接对：
  0: (0,1)  1: (1,2)  2: (2,3)  3: (3,0)
  4: (0,1)+(2,3)  5: (0,3)+(1,2)
  6: (0,2)  7: (1,3)

输入格式：
  N 行，每行 N 个字符（瓦片编号 0~7 拼接成字符串）

输出格式：
  一行长度 N*N 的字符串，第 30*i+j 个字符为格 (i,j) 的旋转次数 r_{i,j}
"""

import sys
from collections import deque

input = sys.stdin.readline

# 每种瓦片旋转 0 次时的连接对列表
TILE_CONNECTIONS_BASE = {
    0: [(0, 1)],
    1: [(1, 2)],
    2: [(2, 3)],
    3: [(3, 0)],
    4: [(0, 1), (2, 3)],
    5: [(0, 3), (1, 2)],
    6: [(0, 2)],
    7: [(1, 3)],
}

# 逆时针旋转一次后的瓦片编号
ROTATE_ONCE = [1, 2, 3, 0, 5, 4, 7, 6]


def get_connections(tile_type, rot):
    """获取 tile_type 旋转 rot 次后的连接对（方向编码）"""
    t = tile_type
    for _ in range(rot):
        t = ROTATE_ONCE[t]
    # 每次旋转所有方向 +1 mod 4
    return [((a + rot) % 4, (b + rot) % 4) for a, b in TILE_CONNECTIONS_BASE[tile_type]]


def solve():
    N = int(input())
    grid = []
    for _ in range(N):
        row = list(map(int, list(input().strip())))
        grid.append(row)

    # 并查集：每格 4 个端口，节点编号 = (row*N + col)*4 + dir
    total = N * N * 4
    parent = list(range(total))
    rank_arr = [0] * total

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank_arr[rx] < rank_arr[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank_arr[rx] == rank_arr[ry]:
            rank_arr[rx] += 1
        return True

    def nid(r, c, d):
        return (r * N + c) * 4 + d

    # 方向偏移
    DR = [-1, 0, 1, 0]
    DC = [0, 1, 0, -1]
    OPP = [2, 3, 0, 1]

    # 预先合并相邻格子之间对应端口（物理连接，固定不变）
    for r in range(N):
        for c in range(N):
            for d in range(4):
                nr, nc = r + DR[d], c + DC[d]
                if 0 <= nr < N and 0 <= nc < N:
                    union(nid(r, c, d), nid(nr, nc, OPP[d]))

    # 逐格贪心选旋转次数
    rotations = []
    for r in range(N):
        for c in range(N):
            tile = grid[r][c]
            best_rot = 0
            best_score = -1
            for rot in range(4):
                conns = get_connections(tile, rot)
                score = sum(
                    1 for a, b in conns
                    if find(nid(r, c, a)) != find(nid(r, c, b))
                )
                if score > best_score:
                    best_score = score
                    best_rot = rot
            rotations.append(best_rot)
            # 应用旋转，合并端口
            for a, b in get_connections(tile, best_rot):
                union(nid(r, c, a), nid(r, c, b))

    # 输出：一行 N*N 个字符
    print(''.join(map(str, rotations)))


solve()
