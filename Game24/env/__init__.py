DATA_PATH = 'data'


class Environment:
    def __init__(self):
        pass

    def reset(self, idx: int):
        raise NotImplementedError

    def step(self, action):
        raise NotImplementedError
