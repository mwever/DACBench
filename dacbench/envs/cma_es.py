"""
CMA-ES environment adapted from CMAWorld in
"Learning Step-size Adaptation in CMA-ES"
by G.Shala and A. Biedenkapp and N.Awad and S. Adriaensen and M.Lindauer and F. Hutter.
Original author: Gresa Shala
"""

import numpy as np
from collections import deque
from cma.evolution_strategy import CMAEvolutionStrategy
import threading

from dacbench import AbstractEnv


def _norm(x):
    return np.sqrt(np.sum(np.square(x)))


# IDEA: if we ask cma instead of ask_eval, we could make this parallel
class CMAESEnv(AbstractEnv):
    def __init__(self, config):
        super(CMAESEnv, self).__init__(config)
        self.b = None
        self.bounds = [None, None]
        self.fbest = None
        self.history_len = config.hist_length
        self.history = deque(maxlen=self.history_len)
        self.past_obj_vals = deque(maxlen=self.history_len)
        self.past_sigma = deque(maxlen=self.history_len)
        self.solutions = None
        self.func_values = []
        self.cur_obj_val = -1
        # self.chi_N = dim ** 0.5 * (1 - 1.0 / (4.0 * dim) + 1.0 / (21.0 * dim ** 2))
        self.lock = threading.Lock()
        self.popsize = config["popsize"]
        self.cur_ps = self.popsize
        if "state_method" in config.keys():
            self.get_state = config["state_method"]
        else:
            self.get_state = self.get_default_state

    def step(self, action):
        """
        Execute environment step

        Parameters
        ----------
        action : list
            action to execute

        Returns
        -------
        np.array, float, bool, dict
            state, reward, done, metainfo

        """
        done = super(CMAESEnv, self).step_()
        self.history.append([self.f_difference, self.velocity])
        done = done or self.es.stop()
        if not done:
            """Moves forward in time one step"""
            sigma = action
            self.es.tell(self.solutions, self.func_values)
            self.es.sigma = np.maximum(sigma, 0.05)
            self.solutions, self.func_values = self.es.ask_and_eval(self.fcn)

        self.f_difference = np.nan_to_num(
            np.abs(np.amax(self.func_values) - self.cur_obj_val)
            / float(self.cur_obj_val)
        )
        self.velocity = np.nan_to_num(
            np.abs(np.amin(self.func_values) - self.cur_obj_val)
            / float(self.cur_obj_val)
        )
        self.fbest = min(self.es.best.f, np.amin(self.func_values))

        self.past_obj_vals.append(self.cur_obj_val)
        self.past_sigma.append(self.cur_sigma)
        self.cur_ps = _norm(self.es.adapt_sigma.ps)
        self.cur_loc = self.es.best.x
        self.cur_sigma = self.es.sigma
        self.cur_obj_val = self.es.best.f
        return self.get_state(), -self.fbest, done, {}

    def reset(self):
        """
        Reset environment

        Returns
        -------
        np.array
            state
        """
        super(CMAESEnv, self).reset_()
        self.history.clear()
        self.past_obj_vals.clear()
        self.past_sigma.clear()
        self.cur_loc = self.instance[3]
        self.init_sigma = self.instance[2]
        self.cur_sigma = self.init_sigma
        self.dim = self.instance[1]
        self.fcn = self.instance[0]

        self.func_values = []
        self.f_vals = deque(maxlen=self.popsize)
        self.es = CMAEvolutionStrategy(
            self.cur_loc,
            self.init_sigma,
            {"popsize": self.popsize, "bounds": self.bounds},
        )
        self.solutions, self.func_values = self.es.ask_and_eval(self.fcn)
        self.fbest = self.func_values[np.argmin(self.func_values)]
        self.f_difference = np.abs(
            np.amax(self.func_values) - self.cur_obj_val
        ) / float(self.cur_obj_val)
        self.velocity = np.abs(np.amin(self.func_values) - self.cur_obj_val) / float(
            self.cur_obj_val
        )
        self.es.mean_old = self.es.mean
        self.history.append([self.f_difference, self.velocity])
        return self.get_state()

    def get_default_state(self):
        """
        Gather state description

        Returns
        -------
        dict
            state

        """
        past_obj_val_deltas = []
        for i in range(1, len(self.past_obj_vals)):
            past_obj_val_deltas.append(
                (self.past_obj_vals[i] - self.past_obj_vals[i - 1] + 1e-3)
                / float(self.past_obj_vals[i - 1])
            )
        if len(self.past_obj_vals) > 0:
            past_obj_val_deltas.append(
                (self.cur_obj_val - self.past_obj_vals[-1] + 1e-3)
                / float(self.past_obj_vals[-1])
            )
        past_obj_val_deltas = np.array(past_obj_val_deltas).reshape(-1)

        history_deltas = []
        for i in range(len(self.history)):
            history_deltas.append(self.history[i])
        history_deltas = np.array(history_deltas).reshape(-1)
        past_sigma_deltas = []
        for i in range(len(self.past_sigma)):
            past_sigma_deltas.append(self.past_sigma[i])
        past_sigma_deltas = np.array(past_sigma_deltas).reshape(-1)
        past_obj_val_deltas = np.hstack(
            (
                np.zeros((self.history_len - past_obj_val_deltas.shape[0],)),
                past_obj_val_deltas,
            )
        )
        history_deltas = np.hstack(
            (
                np.zeros((self.history_len * 2 - history_deltas.shape[0],)),
                history_deltas,
            )
        )
        past_sigma_deltas = np.hstack(
            (
                np.zeros((self.history_len - past_sigma_deltas.shape[0],)),
                past_sigma_deltas,
            )
        )

        cur_loc = np.array(self.cur_loc)
        cur_ps = np.array([self.cur_ps])
        cur_sigma = np.array([self.cur_sigma])

        state = {
            "current_loc": cur_loc,
            "past_deltas": past_obj_val_deltas,
            "current_ps": cur_ps,
            "current_sigma": cur_sigma,
            "history_deltas": history_deltas,
            "past_sigma_deltas": past_sigma_deltas,
        }
        return state