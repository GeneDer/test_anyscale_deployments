import ray.rllib.algorithms.ppo as ppo
from pathlib import Path
from ray import serve
from starlette.requests import Request

folder_path = "checkpoint_000001"
PATH_TO_CHECKPOINT = Path(__file__).absolute().parent / "rllib_checkpoint" / folder_path

@serve.deployment
class ServePPOModel:
    def __init__(self, checkpoint_path) -> None:
        # Re-create the originally used config.
        config = ppo.PPOConfig() \
            .framework("torch") \
            .rollouts(num_rollout_workers=0)
        # Build the Algorithm instance using the config.
        self.algorithm = config.build(env="CartPole-v0")
        # Restore the algo's state from the checkpoint.
        self.algorithm.restore(checkpoint_path)

    async def __call__(self, request: Request):
        json_input = await request.json()
        obs = json_input["observation"]

        action = self.algorithm.compute_single_action(obs)
        return {"action": int(action)}


agent = ServePPOModel.bind(PATH_TO_CHECKPOINT)
# serve.run(agent)
