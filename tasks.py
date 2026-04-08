class TaskDef:
    def __init__(self, name: str, initial_msg: str, expected_route: str, required_info: list = None, needs_refund: bool = False):
        self.name = name
        self.initial_msg = initial_msg
        self.expected_route = expected_route
        self.required_info = required_info or[]
        self.needs_refund = needs_refund

# Define 3 strict tasks (Easy, Medium, Hard)
TASKS =[
    TaskDef(
        name="easy_password_reset",
        initial_msg="I forgot my password and cannot log in.",
        expected_route="IT_SUPPORT"
    ),
    TaskDef(
        name="medium_hardware_issue",
        initial_msg="My laptop won't turn on.",
        expected_route="HARDWARE_SUPPORT",
        required_info=["serial_number"]
    ),
    TaskDef(
        name="hard_refund_processing",
        initial_msg="I want a refund for my recent purchase, it arrived broken.",
        expected_route="BILLING",
        required_info=["order_id", "photo_evidence"],
        needs_refund=True
    )
]

def grader(task: TaskDef, final_state: dict) -> float:
    """Deterministic programmatic grader returning 0.0 to 1.0"""
    score = 0.0
    total_checks = 1 + len(task.required_info) + (1 if task.needs_refund else 0)
    
    if final_state.get("route") == task.expected_route:
        score += 1.0
        
    for info in task.required_info:
        if info in final_state.get("collected_info",[]):
            score += 1.0
            
    if task.needs_refund and final_state.get("refund_processed", False):
        score += 1.0
        
    return score / total_checks