from llmmpc2.env.game24 import Game24
from functools import partial


def get_input():
    inputNew = partial(input, 'Input something pls:\n')
    sentinel = 'end'  # 遇到这个就结束
    lines = []
    for line in iter(inputNew, sentinel):
        lines.append(line)
    return "\n".join(lines)


env = Game24("24.csv")

print(env.puzzle)
obs = env.reset(0)
done = False
while not done:
    action = get_input()
    obs, reward, done, info = env.step(action)
    print(obs)
    print(reward, done, info)
