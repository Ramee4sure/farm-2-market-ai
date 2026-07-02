import importlib.util
import sys
import os

agent_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "agent.py"))

try:
    spec = importlib.util.spec_from_file_location("agent", agent_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["agent"] = module
    spec.loader.exec_module(module)
    
    root_agent = module.root_agent
    print("Agent imported successfully!")
    print(f"Workflow name: {root_agent.name}")
    print(f"Workflow nodes: {[node.name for node in root_agent.graph.nodes]}")
    print("Graph validation completed successfully!")
    sys.exit(0)
except Exception as e:
    import traceback
    print("Error compiling/validating agent workflow:")
    traceback.print_exc()
    sys.exit(1)
