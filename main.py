# from Environment import run_env_rl
from Greedy import run_env_greedy
# from FairDistribuition import run_env_fair_distribuition
if __name__ == '__main__':
    env = run_env_greedy.Environment()
    env.run()




