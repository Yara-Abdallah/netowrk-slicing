from RL.ActionBuilder import ActionBuilder_
from RL.Agent.Agent import Agent


class AgentBuilder_:
    def __init__(self, agent=None):
        if agent is None:
            self.agent = Agent()
        else:
            self.agent = agent

    def __str__(self):
        return f"action : {self.agent.action}"

    def action(self):
        return ActionBuilder(self.agent)

    def build(self):
        return self.agent


class ActionBuilder(AgentBuilder_):
    def __init__(self, agent):
        super().__init__(agent)

    def build_action(self):
        self.agent.action = ActionBuilder_().command().build_command().build()
        return self



# act = AgentBuilder()
# act = act \
#     .action() \
#     .build_action()
#
# print(act)
# print(act.build())

