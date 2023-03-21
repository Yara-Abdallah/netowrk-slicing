class State:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def __init__(self):
        raise NotImplementedError

    def calculate_state(self):
        pass
