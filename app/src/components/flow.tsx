import { Controls, MiniMap, ReactFlow, useReactFlow } from "@xyflow/react"
import "@xyflow/react/dist/style.css"
import { MouseEvent as ReactMouseEvent } from "react"
import { useShallow } from "zustand/react/shallow"
import useFlowStore from "../stores/flow"
import { DefaultNode } from "../types/nodes/default"
import DefaultFlowNode from "./nodes/default"

const nodeTypes = {
  defaultNode: DefaultFlowNode,
}

function Flow() {
  const {
    nodes,
    edges,
    nextNodeId,
    onNodesChange,
    onEdgesChange,
    onConnect,
    setNodes,
    setNextNodeId,
  } = useFlowStore(useShallow((state) => ({
    nodes: state.nodes,
    edges: state.edges,
    nextNodeId: state.nextNodeId,
    onNodesChange: state.onNodesChange,
    onEdgesChange: state.onEdgesChange,
    onConnect: state.onConnect,
    setNodes: state.setNodes,
    setNextNodeId: state.setNextNodeId,
  })))
  const { screenToFlowPosition } = useReactFlow()

  const onPaneContextMenu = (event: ReactMouseEvent | MouseEvent) => {
    event.preventDefault()
    const { clientX, clientY } = event
    const node = {
      id: `${nextNodeId}`,
      type: "defaultNode",
      data: {},
      position: screenToFlowPosition({ x: clientX, y: clientY }),
    } as DefaultNode
    setNodes([...nodes, node])
    setNextNodeId(nextNodeId + 1)
  }

  return (
    <div className="w-screen h-screen">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onPaneContextMenu={onPaneContextMenu}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        colorMode="system"
        fitView
      >
        <MiniMap /> <Controls />
      </ReactFlow>
    </div>
  )
}

export default Flow
