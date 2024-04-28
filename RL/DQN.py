from ray.rllib.algorithms.ppo import PPOConfig
import numpy as np
import OperatorEnv
import Operator
config = (  # 1. Configure the algorithm,
    PPOConfig()
    .environment(OperatorEnv.OperatorEnv)
    .rollouts(num_rollout_workers=2)
    .framework("torch")
    .training(model={"fcnet_hiddens": [64, 64]})
    .evaluation(evaluation_num_workers=1)
)

algo = config.build()  # 2. build the algorithm,

for _ in range(5):
    print(algo.train())  # 3. train it,

algo.evaluate()  # 4. and evaluate it.