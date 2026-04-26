"""
Analysis Service - Smart City Graph Analytics
- Connected Components (BFS)
- PageRank
- Betweenness Centrality (optimized)
- Degree analysis
"""

from typing import List, Dict
from collections import deque
from heapq import heappush, heappop

from business.models.graph import City
from business.models.dto import AnalysisResult, NodeImportance


class AnalysisService:
    def __init__(self, city: City):
        self.city = city

    # =========================
    # Connected Components
    # =========================
    def find_connected_components(self) -> List[List[str]]:
        visited = set()
        components = []

        for node in self.city.nodes:
            if node in visited:
                continue

            queue = deque([node])
            visited.add(node)
            component = []

            while queue:
                current = queue.popleft()
                component.append(current)

                for neighbor in self.city.get_neighbors(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            components.append(component)

        return components

    # =========================
    # Isolated Nodes
    # =========================
    def find_isolated_nodes(self) -> List[str]:
        connected = set()

        for edge in self.city.edges.values():
            connected.add(edge.source)
            connected.add(edge.target)

        return [n for n in self.city.nodes if n not in connected]

    # =========================
    # Degree
    # =========================
    def calculate_average_degree(self) -> float:
        if not self.city.nodes:
            return 0.0

        total = sum(self.city.degree(n) for n in self.city.nodes)
        return total / len(self.city.nodes)

    # =========================
    # PageRank
    # =========================
    def calculate_page_rank(self, iterations: int = 15, damping: float = 0.85) -> Dict[str, float]:
        nodes = list(self.city.nodes)
        n = len(nodes)

        if n == 0:
            return {}

        rank = {n: 1 / n for n in nodes}

        for _ in range(iterations):
            new_rank = {}

            for node in nodes:
                incoming = 0

                for other in nodes:
                    if node in self.city.get_neighbors(other):
                        deg = self.city.degree(other)
                        if deg:
                            incoming += rank[other] / deg

                new_rank[node] = (1 - damping) / n + damping * incoming

            rank = new_rank

        return rank

    # =========================
    # Betweenness (Optimized slightly)
    # =========================
    def calculate_betweenness_centrality(self) -> Dict[str, float]:
        nodes = list(self.city.nodes)
        score = {n: 0.0 for n in nodes}

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                path = self._shortest_path(nodes[i], nodes[j])

                for node in path[1:-1]:
                    score[node] += 1

        max_val = max(score.values()) if score else 1

        if max_val > 0:
            score = {k: v / max_val for k, v in score.items()}

        return score

    # =========================
    # Shortest Path (Dijkstra)
    # =========================
    def _shortest_path(self, start: str, end: str) -> List[str]:
        pq = [(0, start, [start])]
        visited = set()

        while pq:
            cost, node, path = heappop(pq)

            if node == end:
                return path

            if node in visited:
                continue

            visited.add(node)

            for nb in self.city.get_neighbors(node):
                if nb not in visited:
                    new_cost = cost + self.city.get_edge_weight(node, nb)
                    heappush(pq, (new_cost, nb, path + [nb]))

        return []

    # =========================
    # Main Analysis
    # =========================
    async def analyze_city(self) -> AnalysisResult:
        components = self.find_connected_components()
        isolated = self.find_isolated_nodes()
        avg_degree = self.calculate_average_degree()

        pagerank = self.calculate_page_rank()
        betweenness = self.calculate_betweenness_centrality()

        most_central = (
            max(betweenness, key=betweenness.get)
            if betweenness else None
        )

        top_nodes = sorted(
            pagerank.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        top_important = [
            NodeImportance(
                node_id=n,
                node_name=self.city.nodes[n].name if n in self.city.nodes else n,
                score=round(score, 4)
            )
            for n, score in top_nodes
        ]

        isolated_formatted = [
            {
                "id": n,
                "name": self.city.nodes[n].name if n in self.city.nodes else n
            }
            for n in isolated
        ]

        return AnalysisResult(
            algorithm_used="Graph Analytics (BFS + PageRank + Betweenness)",
            total_nodes=len(self.city.nodes),
            total_edges=len(self.city.edges),
            connected_components=len(components),
            isolated_nodes=isolated_formatted,
            is_fully_connected=(len(components) == 1),
            average_degree=round(avg_degree, 2),
            most_central_node=most_central,
            top_important_nodes=top_important
        )