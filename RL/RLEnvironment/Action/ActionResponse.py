class ActionResponse:
    def execute(self, state, action_decision):
        _, next_state = state.update_queue(action_decision)
        return next_state
