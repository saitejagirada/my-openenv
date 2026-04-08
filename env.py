from models import Observation, Action, State
from tasks import TASKS, grader
import copy
from typing import Any, Optional
import openenv.core.env_server as es

class CustomerSupportEnv(es.Environment):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_task_idx = 0
        self.state_data = {}
        self.step_count = 0
        self.max_steps = 10
        self.done = False
        self.reset()

    def reset(self, seed: Optional[int] = None, episode_id: Optional[str] = None, task_idx: int = 0, **kwargs: Any) -> Observation:
        self.current_task_idx = task_idx
        task = TASKS[self.current_task_idx]
        self.step_count = 0
        self.done = False
        
        self.state_data = {
            "ticket_id": f"TKT-{1000 + task_idx}",
            "customer_message": task.initial_msg,
            "history":[f"Customer: {task.initial_msg}"],
            "missing_info": task.required_info.copy(),
            "collected_info":[],
            "route": None,
            "refund_processed": False,
            "status": "OPEN",
            "episode_id": episode_id
        }
        return self._get_obs(reward=0.01, feedback="")

    @property
    def state(self) -> State:
        return State(
            ticket_id=self.state_data.get("ticket_id", ""),
            customer_message=self.state_data.get("customer_message", ""),
            history=copy.deepcopy(self.state_data.get("history", [])),
            missing_info=copy.deepcopy(self.state_data.get("missing_info", [])),
            status=self.state_data.get("status", "OPEN"),
            refund_processed=self.state_data.get("refund_processed", False),
            episode_id=self.state_data.get("episode_id", None),
            step_count=self.step_count
        )

    def _get_obs(self, reward: float = 0.01, feedback: str = "") -> Observation:
        # Clamp ALL rewards strictly between 0 and 1 (exclusive)
        clamped_reward = max(0.01, min(0.99, reward))
        return Observation(
            ticket_id=self.state_data["ticket_id"],
            customer_message=self.state_data["customer_message"],
            history=self.state_data["history"],
            missing_info=self.state_data["missing_info"],
            status=self.state_data["status"],
            refund_processed=self.state_data["refund_processed"],
            done=self.done,
            reward=clamped_reward,
            metadata={"feedback": feedback, "state": self.state_data}
        )

    def step(self, action: Action, timeout_s: Optional[float] = None, **kwargs: Any) -> Observation:
        if self.done:
            return self._get_obs(reward=0.01, feedback="Episode already done")

        self.step_count += 1
        reward_val = 0.01
        feedback = ""
        task = TASKS[self.current_task_idx]

        # Penalize infinite loops / max steps
        if self.step_count >= self.max_steps:
            self.done = True
            final_score = grader(task, self.state_data)
            return self._get_obs(reward=float(final_score), feedback="Max steps reached")

        if action.action_type == "ASK_INFO":
            asked = action.argument.lower()
            found = False
            for req in self.state_data["missing_info"]:
                if req.lower() in asked.lower():
                    self.state_data["missing_info"].remove(req)
                    self.state_data["collected_info"].append(req)
                    reply = f"Here is my {req}: [MOCK_DATA]"
                    self.state_data["history"].extend([f"Agent: {action.argument}", f"Customer: {reply}"])
                    self.state_data["customer_message"] = reply
                    reward_val = 0.3
                    feedback = f"Successfully collected {req}"
                    found = True
                    break
            if not found:
                reward_val = 0.05
                feedback = "Asked for unnecessary information."

        elif action.action_type == "REFUND":
            if task.needs_refund and "order_id" in self.state_data["collected_info"]:
                self.state_data["refund_processed"] = True
                reward_val = 0.4
                feedback = "Refund processed successfully."
            else:
                reward_val = 0.05
                feedback = "Cannot process refund without order ID or refund not required."

        elif action.action_type == "ROUTE":
            self.state_data["route"] = action.argument
            if self.state_data["missing_info"]:
                reward_val = 0.05
                feedback = "Routed prematurely without gathering required info."
            else:
                self.done = True
                final_score = grader(task, self.state_data)
                reward_val = float(final_score)
                feedback = f"Ticket routed. Final Score: {final_score}"

        elif action.action_type == "CLOSE":
            self.done = True
            self.state_data["status"] = "CLOSED"
            final_score = grader(task, self.state_data)
            reward_val = float(final_score)
            feedback = f"Ticket closed. Final Score: {final_score}"

        return self._get_obs(reward=reward_val, feedback=feedback)
