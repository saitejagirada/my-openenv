import os
import json
from openai import OpenAI
from env import CustomerSupportEnv
from models import Action
from tasks import TASKS

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# 1. Required Environment Variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# 2. Open AI Client Only
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def run_inference():
    env = CustomerSupportEnv()
    
    for idx, task in enumerate(TASKS):
        obs = env.reset(task_idx=idx)
        done = False
        step_idx = 0
        rewards_history = []
        
        # [START] FORMAT
        print(f"[START] task={task.name} env=customer_support model={MODEL_NAME}")
        
        while not done:
            step_idx += 1
            error_msg = "null"
            reward_val = 0.00
            action_str = ""
            
            # 🚀 HEAVILY ENGINEERED PROMPT FOR STRICT COMPLIANCE
            prompt = (
                "System: You are an automated customer support AI. You MUST respond strictly in JSON format matching this schema: "
                "{\"action_type\": \"ROUTE\"|\"ASK_INFO\"|\"REFUND\"|\"CLOSE\", \"argument\": \"string\"}\n\n"
                "CRITICAL RULES:\n"
                "1. If 'missing_info' in the observation is empty ([]), DO NOT use ASK_INFO. You must take action (ROUTE or REFUND).\n"
                "2. If 'missing_info' contains items, you MUST use ASK_INFO. The 'argument' MUST contain the EXACT string from 'missing_info' (e.g., 'serial_number', 'order_id', 'photo_evidence'). Ask for ONLY ONE missing item at a time\n"
                "3. When using ROUTE, the 'argument' MUST be exactly one of these three codes: 'IT_SUPPORT', 'HARDWARE_SUPPORT', or 'BILLING'. Do not output full sentences.\n"
                "4. If the user wants a refund, and you have collected 'order_id', you MUST first use the REFUND action. Then, in the next step, use ROUTE with 'BILLING'.\n\n"
                f"Observation: {obs.model_dump_json()}"
            )

            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                
                # Safely parse JSON in case Qwen outputs markdown ticks
                raw_action = response.choices[0].message.content.strip()
                if raw_action.startswith("```json"):
                    raw_action = raw_action[7:-3].strip()
                elif raw_action.startswith("```"):
                    raw_action = raw_action[3:-3].strip()
                    
                action_data = json.loads(raw_action)
                
                # Pydantic validation
                action = Action(**action_data)
                action_str = f"{action.action_type}('{action.argument}')"
                
                # Env Step
                obs = env.step(action)
                done = obs.done
                reward_val = float(obs.reward) if obs.reward is not None else 0.0
                rewards_history.append(reward_val)
                
            except Exception as e:
                error_msg = str(e).replace('\n', ' ')
                action_str = "ERROR"
                done = True
                rewards_history.append(0.00)
                
            # [STEP] FORMAT
            print(f"[STEP] step={step_idx} action={action_str} reward={reward_val:.2f} done={str(done).lower()} error={error_msg}")

        # [END] FORMAT
        # A score > 0.8 typically means success based on our grader logic
        final_score = sum(rewards_history) if rewards_history else 0.0
        success = final_score > 0.8
        rewards_str = ",".join([f"{r:.2f}" for r in rewards_history])
        print(f"[END] success={str(success).lower()} steps={step_idx} score={final_score:.2f} rewards={rewards_str}")

if __name__ == "__main__":
    run_inference()