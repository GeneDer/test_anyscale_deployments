import ray
import ray.rllib.algorithms.ppo as ppo
from ray import serve


def train_ppo_model():
    # Configure our PPO algorithm.
    config = (
        ppo.PPOConfig()
        .environment("CartPole-v1")
        .framework("torch")
        .rollouts(num_rollout_workers=0)
    )
    # Create a `PPO` instance from the config.
    algo = config.build()
    # Train for one iteration.
    algo.train()
    # Save state of the trained Algorithm in a checkpoint.
    checkpoint_dir = algo.save("/tmp/rllib_checkpoint")
    return checkpoint_dir


checkpoint_path = train_ppo_model()

from starlette.requests import Request


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


ppo_model = ServePPOModel.bind(checkpoint_path)
serve.run(ppo_model)
