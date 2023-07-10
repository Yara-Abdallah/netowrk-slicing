import cProfile

from Environment import run_env_rl
from memory_profiler import profile

# from Greedy import run_env_greedy
# from FairDistribuition import run_env_fair_distribuition
import gc
gc.set_debug(gc.DEBUG_UNCOLLECTABLE) # Enable debugging of circular references

def main():

    from pympler.tracker import SummaryTracker
    tracker = SummaryTracker()

    # ... some code you want to investigate ...

    env = run_env_rl.Environment('period3')
    env.run()


if __name__ == '__main__':
    main()





