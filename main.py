from Environment import run_env
import threading
if __name__ == '__main__':
    env = run_env.Environment()
    env.run()
    # sim_thread = threading.Thread(target=env.run())
    # # plot_thread = threading.Thread(target=env.run_plot_animation())
    #
    # sim_thread.start()
    # # plot_thread.start()
    #
    # sim_thread.join()
    # # plot_thread.join()



