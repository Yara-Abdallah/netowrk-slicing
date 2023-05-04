from Environment import run_env_rl
from memory_profiler import profile

# from Greedy import run_env_greedy
# from FairDistribuition import run_env_fair_distribuition
import gc
gc.set_debug(gc.DEBUG_UNCOLLECTABLE) # Enable debugging of circular references

def main():
    env = run_env_rl.Environment()
    env.run()


if __name__ == '__main__':
    main()





