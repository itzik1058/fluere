from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import networkx as nx
from fastapi import APIRouter, HTTPException

from fluere.api.schema import CallEdge, CallGraph, CallNode
from fluere.core import BUILTIN_NODES
from fluere.core.node import Node, NodeParameterKind, NodeSignature

NODES: dict[str, Node] = {}


@asynccontextmanager
async def api_lifespan(router: APIRouter) -> AsyncIterator[None]:
    NODES.update(BUILTIN_NODES)
    yield


router = APIRouter(lifespan=api_lifespan)


@router.get("/signatures")
def signatures() -> list[NodeSignature]:
    return [node.signature for node in BUILTIN_NODES.values()]


@router.post("/execute")
def execute(call_graph: CallGraph) -> dict[str, Any]:
    graph: nx.DiGraph[str] = nx.DiGraph()
    for call_node in call_graph.nodes:
        graph.add_node(
            call_node.id,
            **call_node.model_dump(),
        )
    for edge in call_graph.edges:
        if edge.source not in graph.nodes:
            raise HTTPException(
                status_code=400,
                detail=f"Edge {edge!r} refers to a missing node {edge.source!r}",
            )
        if edge.target not in graph.nodes:
            raise HTTPException(
                status_code=400,
                detail=f"Edge {edge!r} refers to a missing node {edge.target!r}",
            )
        graph.add_edge(
            edge.source,
            edge.target,
            **edge.model_dump(),
        )
    if not nx.is_directed_acyclic_graph(graph):
        raise HTTPException(status_code=400, detail="Call graph contains a cycle")
    call_return: dict[str, Any] = {}
    for graph_node in nx.topological_sort(graph):
        call_node = CallNode.model_validate(graph.nodes[graph_node])
        node = NODES.get(call_node.name)
        if node is None:
            raise HTTPException(
                status_code=400,
                detail=f"Could not find {call_node!r}",
            )
        parameters: dict[str, Any] = {
            parameter.name: parameter.value for parameter in call_node.parameters
        }
        for source, _, edge_data in graph.in_edges(graph_node, data=True):
            call_edge = CallEdge.model_validate(edge_data)
            parameters[call_edge.parameter] = call_return[source]
        args: list[Any] = []
        kwargs: dict[str, Any] = {}
        for parameter in node.signature.parameters.values():
            defined = parameter.name in parameters or parameter.default is not None
            arg = parameter.default
            if parameter.name in parameters:
                arg = parameters[parameter.name]
            match parameter.kind:
                case (
                    NodeParameterKind.POSITIONAL_ONLY
                    | NodeParameterKind.POSITIONAL_OR_KEYWORD
                ):
                    if not defined:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Missing required argument "
                            f"{parameter.name!r} of {call_node!r}",
                        )
                    args.append(arg)
                case NodeParameterKind.VAR_POSITIONAL:
                    if defined:
                        args.append(arg)
                case NodeParameterKind.KEYWORD_ONLY:
                    if not defined:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Missing required argument "
                            f"{parameter.name!r} of {call_node!r}",
                        )
                    kwargs[parameter.name] = arg
                case NodeParameterKind.VAR_KEYWORD:
                    if defined:
                        kwargs[parameter.name] = arg
        call_return[graph_node] = node(*args, **kwargs)
    return call_return
