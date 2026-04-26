# business/models/graph.py
"""
نماذج الرسم البياني للمدينة الذكية
تحتوي على: Node, Edge, City
"""

from typing import List, Dict, Optional
from pydantic import BaseModel


class Node(BaseModel):
    """
    العقدة - تمثل نقطة على الخريطة
    
    مثال:
    Node(
        id="A",
        name="المنزل",
        type="house",
        x=220,
        y=320
    )
    """
    id: str           # معرف فريد (A, B, C, I1, I2, ...)
    name: str         # الاسم الظاهر للمستخدم (المنزل, المستشفى, ...)
    type: str         # نوع العقدة (house, hospital, school, gas, intersection)
    x: float          # الإحداثي X على الخريطة
    y: float          # الإحداثي Y على الخريطة
    user_id: Optional[str] = None  # معرف المستخدم (للتخزين في قاعدة البيانات)


class Edge(BaseModel):
    """
    الحافة - تمثل طريق بين عقدتين
    
    مثال:
    Edge(
        id="A-I1",
        source="A",
        target="I1",
        weight=2.3,
        congestion=0.7
    )
    """
    id: str           # معرف فريد (A-I1, I1-C, ...)
    source: str       # معرف العقدة المصدر (من أين يبدأ الطريق)
    target: str       # معرف العقدة الهدف (إلى أين يصل الطريق)
    weight: float     # وزن الحافة = المسافة بالكيلومترات
    congestion: float = 0.0  # مستوى الازدحام (0 = خالي، 1 = زحمة شديدة)
    user_id: Optional[str] = None  # معرف المستخدم (للتخزين في قاعدة البيانات)


class City:
    """
    المدينة - تحتوي على جميع العقد والحواف
    
    هذه هي الحاوية الرئيسية التي تدير الرسم البياني بأكمله.
    
    مثال الاستخدام:
    
    city = City()
    
    # إضافة العقد
    city.add_node(Node(id="A", name="المنزل", type="house", x=220, y=320))
    city.add_node(Node(id="B", name="المستشفى", type="hospital", x=680, y=320))
    
    # إضافة طريق بين العقد
    city.add_edge(Edge(id="A-B", source="A", target="B", weight=2.5))
    
    # معرفة جيران عقدة معينة
    neighbors = city.get_neighbors("A")  # returns ["B"]
    
    # معرفة المسافة بين عقدتين
    distance = city.get_edge_weight("A", "B")  # returns 2.5
    """
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}  # {node_id: Node object}
        self.edges: Dict[str, Edge] = {}  # {edge_id: Edge object}
    
    def get_neighbors(self, node_id: str) -> List[str]:
        """
        جلب جميع العقد المجاورة لعقدة معينة
        
        مثال:
        city.get_neighbors("I1")  # returns ["A", "C", "B", "I2", "D"]
        """
        neighbors = []
        for edge in self.edges.values():
            if edge.source == node_id:
                neighbors.append(edge.target)
            elif edge.target == node_id:
                neighbors.append(edge.source)
        return neighbors
    
    def get_edge_weight(self, u: str, v: str) -> float:
        """
        جلب وزن الحافة (المسافة) بين عقدتين
        
        مثال:
        distance = city.get_edge_weight("A", "I1")  # returns 2.3
        """
        for edge in self.edges.values():
            if (edge.source == u and edge.target == v) or (edge.source == v and edge.target == u):
                return edge.weight
        return 1.0  # القيمة الافتراضية إذا لم يتم العثور على الحافة
    
    def get_edge_congestion(self, u: str, v: str) -> float:
        """
        جلب مستوى الازدحام بين عقدتين
        
        مثال:
        congestion = city.get_edge_congestion("A", "I1")  # returns 0.7
        """
        for edge in self.edges.values():
            if (edge.source == u and edge.target == v) or (edge.source == v and edge.target == u):
                return edge.congestion
        return 0.0
    
    def degree(self, node_id: str) -> int:
        """
        درجة العقدة = عدد الطرق المتصلة بها
        
        مثال:
        city.degree("I1")  # returns 5 (لأن I1 متصل بـ A, C, B, I2, D)
        """
        return len(self.get_neighbors(node_id))
    
    def add_node(self, node: Node):
        """إضافة عقدة جديدة إلى المدينة"""
        self.nodes[node.id] = node
    
    def add_edge(self, edge: Edge):
        """إضافة حافة جديدة إلى المدينة"""
        self.edges[edge.id] = edge
    
    def remove_node(self, node_id: str):
        """
        حذف عقدة وجميع الحواف المرتبطة بها
        """
        # حذف العقدة نفسها
        if node_id in self.nodes:
            del self.nodes[node_id]
        
        # حذف كل الحواف المتصلة بهذه العقدة
        edges_to_delete = []
        for edge_id, edge in self.edges.items():
            if edge.source == node_id or edge.target == node_id:
                edges_to_delete.append(edge_id)
        
        for edge_id in edges_to_delete:
            del self.edges[edge_id]
    
    def remove_edge(self, edge_id: str):
        """حذف حافة محددة"""
        if edge_id in self.edges:
            del self.edges[edge_id]
    
    def clear(self):
        """مسح جميع البيانات (تفريغ المدينة)"""
        self.nodes.clear()
        self.edges.clear()
    
    def to_dict(self) -> Dict:
        """
        تحويل المدينة إلى قاموس (لحفظها في ملف JSON)
        
        مثال:
        data = city.to_dict()
        # data = {
        #     "nodes": {"A": {...}, "B": {...}},
        #     "edges": {"A-B": {...}}
        # }
        """
        return {
            "nodes": {node_id: node.dict() for node_id, node in self.nodes.items()},
            "edges": {edge_id: edge.dict() for edge_id, edge in self.edges.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "City":
        """
        إنشاء مدينة جديدة من قاموس (تحميل من ملف JSON)
        
        مثال:
        with open("project.dar") as f:
            data = json.load(f)
            city = City.from_dict(data)
        """
        city = cls()
        
        for node_id, node_data in data.get("nodes", {}).items():
            city.nodes[node_id] = Node(**node_data)
        
        for edge_id, edge_data in data.get("edges", {}).items():
            city.edges[edge_id] = Edge(**edge_data)
        
        return city