from dotenv import load_dotenv
load_dotenv()

import uvicorn
from openenv.core.env_server.http_server import create_app
from env import CustomerSupportEnv
from models import Action, Observation

# Use the environment class and Pydantic types to create the app
app = create_app(
    CustomerSupportEnv, 
    Action, 
    Observation, 
    env_name="customer_support_env"
)

def main():
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
