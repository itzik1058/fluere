from fastapi import APIRouter

from fluere.core.builtin import BUILTIN_NODES
from fluere.core.node import NodeSignature

router = APIRouter()


@router.get("/signatures")
def signatures() -> list[NodeSignature]:
    return [node.signature for node in BUILTIN_NODES]
