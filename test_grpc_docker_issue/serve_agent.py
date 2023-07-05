from starlette.requests import Request
import ray.rllib.algorithms.ppo as ppo
from ray import serve
import gymnasium.spaces as spaces
import numpy as np
from pathlib import Path
import requests
# from ray.tune.registry import register_env
# from mixing_environment.mixing_env.env_creator import mixing_env_creator
# register_env("mixing_environment", mixing_env_creator)
# Update this to match location of checkpoint
folder_path = "checkpoint_000020"
PATH_TO_CHECKPOINT = Path(__file__).absolute().parent / "inference_checkpoints" / folder_path

# Update this to reflect observation and action space in environment
observation_space = spaces.Box(
            low=np.array([0, 0, 0]),
            high=np.array([30000, 20, 300]),
            shape=(3,),
            dtype=np.float32,
        )
action_space = spaces.Box(
            low=np.array([0, 0]),
            high=np.array([10, 200]),
            shape=(2,),
            dtype=np.float32,
        )
@serve.deployment
class ServePPOModel:
    """
    Class which defines how the model is served

    args:
        - checkpoint_path (str): path to the checkpoint

    """
    def __init__(self, checkpoint_path) -> None:
        # Re-create the originally used config. - NOTE this assumes PPO, update for a different algorithm as needed
        config = ppo.PPOConfig()\
            .framework("torch")\
            .rollouts(num_rollout_workers=0)

        # Build the Algorithm instance using the config. env=None since it is not needed for inference
        self.algorithm = config.environment(env=None,observation_space=observation_space,action_space=action_space).build()
        # self.algorithm = config.build(env="mixing_environment")
        # Restore the algorithm state from the checkpoint
        self.algorithm.restore(checkpoint_path)
        print('restored!')


    async def __call__(self, request: Request):
        json_input = await request.json()
        obs = json_input["observation"] #observation is the key, the list of states are the value in the dictionary we send as data
        action = self.algorithm.compute_single_action(obs)
        return {"action": action}
    
agent = ServePPOModel.bind(PATH_TO_CHECKPOINT)
serve.run(agent)

