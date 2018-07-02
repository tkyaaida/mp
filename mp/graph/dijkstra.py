import numpy as np


class Dijkstra:
    def __init__(self, graph):
        """

        :param graph: 隣接行列
        """
        self.graph = graph
        self.num_nodes = graph.shape[0]

    def explore(self, i, distances, optimal_prev_nodes):
        """ノードiを探索"""
        next_nodes = self.get_possible_routes(i)
        for next_node in next_nodes:
            self.step(i, next_node, distances, optimal_prev_nodes)

    def step(self, i, j, distances, optimal_prev_nodes):
        """i->jに移動する場合の値を更新"""
        current_distance = distances[j]
        calculated_distance = distances[i] + self.graph[i, j]
        if current_distance > calculated_distance:
            distances[j] = calculated_distance  # 距離を更新
            optimal_prev_nodes[j] = i  # ノードjにはノードiからが最適経路

    def get_possible_routes(self, i):
        """ノードiから移動可能なノードのリストを取得"""
        # 隣接行列の(i, j)成分が0でなければ移動可能
        possible_routes = list(np.argwhere(self.graph[i] != 0)[:, 0])
        return possible_routes

    def select_next_node(self, nodes, distances):
        """未探索nodeの中から距離が最小のノードを返す"""
        min_node = 0
        min_value = np.inf
        for node in nodes:
            if distances[node] < min_value:
                min_value = distances[node]
                min_node = node
        return min_node

    def solve(self, i, j):
        """ノードiからノードjへの最短ルートをダイクストラ法で解く"""
        nodes = list(range(self.num_nodes))

        # 最初は始点nodeの距離を0, それ以外は無限大
        distances = np.ones(self.num_nodes) * np.inf
        distances[i] = 0

        # 各インデックスのノードがどのノードから来るかが最適かを表すリスト
        optimal_prev_nodes = [0] * self.num_nodes

        while len(nodes) >= 1:
            node = self.select_next_node(nodes, distances)
            self.explore(node, distances, optimal_prev_nodes)
            nodes.remove(node)

        # jまでの最適な経路を表示
        route = [j]
        cur_node = j
        while route[-1] != i:
            prev_node = optimal_prev_nodes[cur_node]
            route.append(prev_node)
            cur_node = prev_node

        route.reverse()

        print('最適な経路')
        print(' -> '.join([str(x) for x in route]))


if __name__ == '__main__':
    graph = np.array([
        [0, 50, 80, 0, 0],
        [0, 0, 20, 15, 0],
        [0, 0, 0, 10, 15],
        [0, 0, 0, 0, 30],
        [0, 0, 0, 0, 0]
    ])
    print('隣接行列')
    print(graph)
    dijkstra = Dijkstra(graph)
    dijkstra.solve(0, 4)
