class Reward:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def __init__(self, value=0):
        self.value = value

    def calculate_reward(self,params):
        raise NotImplementedError
