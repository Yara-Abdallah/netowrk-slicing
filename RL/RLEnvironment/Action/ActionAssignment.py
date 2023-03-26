class ActionAssignment:
    def excute(self, state, action_decision):
        print("action ", action_decision)
        print("action shape :",action_decision.shape )
        state.supported_services = action_decision
        return state.calculate_state(state.supported_services)
