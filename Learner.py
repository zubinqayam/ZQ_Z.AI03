"""WorkflowLearner - Learns patterns from workflow executions"""
import logging
from typing import Dict, List, Any
from datetime import datetime


logger = logging.getLogger(__name__)


class WorkflowLearner:
    """Learns patterns and optimizes workflows based on historical data"""
    
    def __init__(self):
        self.learned_patterns: Dict[str, Any] = {}
        self.execution_history: List[Dict[str, Any]] = []
        logger.info("WorkflowLearner initialized")
    
    def record_execution(self, workflow_id: str, execution_data: Dict[str, Any]) -> None:
        """Record a workflow execution for learning"""
        execution = {
            "workflow_id": workflow_id,
            "timestamp": datetime.now().isoformat(),
            "data": execution_data
        }
        self.execution_history.append(execution)
        logger.debug(f"Recorded execution for workflow: {workflow_id}")
    
    def learn_patterns(self, workflow_id: str) -> Dict[str, Any]:
        """Analyze execution history and learn patterns"""
        relevant_executions = [
            ex for ex in self.execution_history 
            if ex["workflow_id"] == workflow_id
        ]
        
        if not relevant_executions:
            return {}
        
        # Simple pattern learning: track success rates and common parameters
        total = len(relevant_executions)
        successful = sum(1 for ex in relevant_executions 
                        if ex["data"].get("success", False))
        
        pattern = {
            "workflow_id": workflow_id,
            "total_executions": total,
            "success_rate": successful / total if total > 0 else 0,
            "last_execution": relevant_executions[-1]["timestamp"]
        }
        
        self.learned_patterns[workflow_id] = pattern
        logger.info(f"Learned patterns for workflow: {workflow_id}")
        return pattern
    
    def get_recommendations(self, workflow_id: str) -> List[str]:
        """Get recommendations based on learned patterns"""
        pattern = self.learned_patterns.get(workflow_id)
        if not pattern:
            return ["No execution history available"]
        
        recommendations = []
        if pattern["success_rate"] < 0.5:
            recommendations.append("Consider reviewing workflow configuration")
        elif pattern["success_rate"] > 0.9:
            recommendations.append("Workflow performing optimally")
        
        return recommendations or ["Workflow performing normally"]
