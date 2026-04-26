# business/services/search_service.py

import math
from typing import List, Optional, Dict
from business.models.graph import City, Node


class SearchService:
    """خدمات البحث داخل SmartCity graph"""

    def __init__(self, city: City):
        self.city = city

    # =========================
    # Search by Type
    # =========================
    def find_nodes_by_type(self, node_type: str) -> List[Node]:
        if not self.city or not self.city.nodes:
            return []

        return [
            node for node in self.city.nodes.values()
            if node.type == node_type
        ]

    # =========================
    # Search by Name
    # =========================
    def search_nodes_by_name(self, query: str, exact: bool = False) -> List[Node]:

        if not query:
            return []

        q = query.strip().lower()

        return [
            node for node in self.city.nodes.values()
            if (node.name.lower() == q if exact else q in node.name.lower())
        ]

    # =========================
    # Nearest Node
    # =========================
    def find_nearest_node(
        self,
        x: float,
        y: float,
        node_type: Optional[str] = None
    ) -> Optional[Node]:

        nearest = None
        min_dist = float("inf")

        for node in self.city.nodes.values():

            if node_type and node.type != node_type:
                continue

            dist = math.hypot(node.x - x, node.y - y)

            if dist < min_dist:
                min_dist = dist
                nearest = node

        return nearest

    # =========================
    # Stats
    # =========================
    def get_node_type_counts(self) -> Dict[str, int]:

        if not self.city or not self.city.nodes:
            return {}

        counts = {}

        for node in self.city.nodes.values():
            counts[node.type] = counts.get(node.type, 0) + 1

        return counts