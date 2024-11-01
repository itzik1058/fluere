import {
  BuiltInNode,
  Edge,
  OnConnect,
  OnEdgesChange,
  OnNodesChange,
} from "@xyflow/react"
import { DefaultNode } from "./nodes/default"

export type FluereNode = BuiltInNode | DefaultNode

export type FlowState = {
  nodes: FluereNode[]
  edges: Edge[]
  nextNodeId: number

  onNodesChange: OnNodesChange<FluereNode>
  onEdgesChange: OnEdgesChange
  onConnect: OnConnect

  setNodes: (nodes: FluereNode[]) => void
  setEdges: (edges: Edge[]) => void
  setNextNodeId: (nodeId: number) => void
}
