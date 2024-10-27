from pydantic import BaseModel


class CallNodeParameter(BaseModel):
    name: str
    value: str


class CallNode(BaseModel):
    id: str
    name: str
    cache: bool = True
    parameters: list[CallNodeParameter]


class CallEdge(BaseModel):
    id: str
    source: str
    target: str
    parameter: str


class CallGraph(BaseModel):
    nodes: list[CallNode]
    edges: list[CallEdge]
