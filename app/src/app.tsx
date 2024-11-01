import { ReactFlowProvider } from "@xyflow/react"
import "@xyflow/react/dist/style.css"
import Flow from "./components/flow"

function App() {
  return (
    <ReactFlowProvider>
      <Flow />
    </ReactFlowProvider>
  )
}

export default App
