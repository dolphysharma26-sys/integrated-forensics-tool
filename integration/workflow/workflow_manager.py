"""
Workflow Manager Module
Coordinates all system modules and operations
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Dict, Any, Optional, List
from enum import Enum
from core.common.logger import setup_logger

logger = setup_logger(__name__)

class WorkflowType(Enum):
    DRIVE_ERASE = "drive_erase"
    FILE_ERASE = "file_erase"
    FILE_RECOVERY = "file_recovery"
    FILE_CARVING = "file_carving"
    VERIFICATION = "verification"
    COMBINED = "combined"

class WorkflowManager:
    """Manages complex workflows involving multiple modules"""
    
    def __init__(self):
        self.active_workflows = {}
        logger.info("Workflow Manager initialized")
    
    def start_workflow(self, workflow_type: WorkflowType, params: Dict) -> str:
        """Start a new workflow"""
        workflow_id = f"WF-{len(self.active_workflows) + 1}"
        
        workflow = {
            "id": workflow_id,
            "type": workflow_type,
            "params": params,
            "status": "PENDING",
            "steps": [],
            "current_step": 0
        }
        
        self.active_workflows[workflow_id] = workflow
        logger.info(f"Workflow started: {workflow_id} ({workflow_type.value})")
        
        return workflow_id
    
    def add_step(self, workflow_id: str, step_name: str, function, args=None):
        """Add a step to workflow"""
        workflow = self.active_workflows.get(workflow_id)
        if workflow:
            workflow["steps"].append({
                "name": step_name,
                "function": function,
                "args": args or {}
            })
            logger.info(f"Added step '{step_name}' to {workflow_id}")
    
    def execute_workflow(self, workflow_id: str) -> bool:
        """Execute all steps in workflow"""
        workflow = self.active_workflows.get(workflow_id)
        if not workflow:
            logger.error(f"Workflow not found: {workflow_id}")
            return False
        
        workflow["status"] = "RUNNING"
        
        for i, step in enumerate(workflow["steps"]):
            workflow["current_step"] = i + 1
            logger.info(f"Executing step {i+1}/{len(workflow['steps'])}: {step['name']}")
            
            try:
                result = step["function"](**step["args"])
                step["result"] = result
                step["status"] = "COMPLETED"
                logger.info(f"Step completed: {step['name']}")
            except Exception as e:
                step["status"] = "FAILED"
                step["error"] = str(e)
                logger.error(f"Step failed: {step['name']} - {e}")
                workflow["status"] = "FAILED"
                return False
        
        workflow["status"] = "COMPLETED"
        logger.info(f"Workflow completed: {workflow_id}")
        return True
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict]:
        """Get workflow status"""
        return self.active_workflows.get(workflow_id)
    
    def list_workflows(self) -> List[Dict]:
        """List all workflows"""
        return list(self.active_workflows.values())

if __name__ == "__main__":
    wm = WorkflowManager()
    
    # Example workflow
    wf_id = wm.start_workflow(WorkflowType.DRIVE_ERASE, {"device": "test"})
    wm.add_step(wf_id, "Detect Device", lambda **kw: print("Detecting..."))
    wm.add_step(wf_id, "Erase Device", lambda **kw: print("Erasing..."))
    wm.add_step(wf_id, "Verify", lambda **kw: print("Verifying..."))
    
    wm.execute_workflow(wf_id)
    print(f"Status: {wm.get_workflow_status(wf_id)['status']}")