import { addEdge, applyEdgeChanges, applyNodeChanges } from "@xyflow/react";
import { create } from "zustand";
import { FlowState } from "../types/flow";

const useFlowStore = create<FlowState>((set, get) => ({
  nodes: [],
  edges: [],
  nextNodeId: 0,

  onNodesChange: (changes) => {
    set({
      nodes: applyNodeChanges(changes, get().nodes),
    });
  },
  onEdgesChange: (changes) => {
    set({
      edges: applyEdgeChanges(changes, get().edges),
    });
  },
  onConnect: (connection) => {
    set({
      edges: addEdge(connection, get().edges),
    });
  },

  setNodes: (nodes) => {
    set({ nodes });
  },
  setEdges: (edges) => {
    set({ edges });
  },
  setNextNodeId: (nodeId) => {
    set({ nextNodeId: nodeId });
  },
}));

export default useFlowStore;
