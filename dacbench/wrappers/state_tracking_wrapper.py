from gym import spaces
from gym import Wrapper
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sb

sb.set_style("darkgrid")
current_palette = list(sb.color_palette())


class StateTrackingWrapper(Wrapper):
    """ Wrapper to track state changed over time """

    def __init__(self, env, state_interval=None):
        super(StateTrackingWrapper, self).__init__(env)
        self.state_interval = state_interval
        self.overall_states = []
        if self.state_interval:
            self.state_intervals = []
            self.current_states = []
        self.episode_states = None
        self.state_type = type(env.observation_space)

    def __setattr__(self, name, value):
        if name in [
            "state_interval",
            "overall_states",
            "state_intervals",
            "current_states",
            "state_type",
            "env",
            "episode_states",
            "get_states",
            "step",
            "reset",
            "render_state_tracking",
        ]:
            object.__setattr__(self, name, value)
        else:
            setattr(self.env, name, value)

    def __getattribute__(self, name):
        if name in [
            "state_interval",
            "overall_states",
            "state_intervals",
            "current_states",
            "state_type",
            "env",
            "episode_states",
            "get_states",
            "step",
            "reset",
            "render_state_tracking",
        ]:
            return object.__getattribute__(self, name)

        else:
            return getattr(self.env, name)

    def reset(self):
        """
        Reset environment and record starting state

        Returns
        -------
        np.array
            state
        """
        state = self.env.reset()
        self.overall_states.append(state)
        if self.state_interval:
            if len(self.current_states) < self.state_interval:
                self.current_states.append(state)
            else:
                self.state_intervals.append(self.current_states)
                self.current_states = [state]
        return state

    def step(self, action):
        """
        Execute environment step and record state

        Parameters
        ----------
        action : int
            action to execute

        Returns
        -------
        np.array, float, bool, dict
            state, reward, done, metainfo
        """
        state, reward, done, info = self.env.step(action)
        self.overall_states.append(state)
        if self.state_interval:
            if len(self.current_states) < self.state_interval:
                self.current_states.append(state)
            else:
                self.state_intervals.append(self.current_states)
                self.current_states = [state]
        return state, reward, done, info

    def get_states(self):
        """
        Get state progression

        Returns
        -------
        np.array or np.array, np.array
            all states or all states and interval sorted states

        """
        if self.state_interval:
            complete_intervals = self.state_intervals + [self.current_states]
            return self.overall_states, complete_intervals

        else:
            return self.overall_states

    def render_state_tracking(self):
        """
        Render state progression

        Returns
        -------
        np.array
            RBG data of state tracking

        """

        def plot_single(ax=None, index=None, title=None, x=False, y=False):
            if ax is None:
                plt.xlabel("Episode")
                plt.ylabel("State")
            elif x and y:
                ax.set_ylabel("State")
                ax.set_xlabel("Episode")
            elif x:
                ax.set_xlabel("Episode")
            elif y:
                ax.set_ylabel("State")

            if index is not None:
                ys = [state[index] for state in self.overall_states]
            else:
                ys = self.overall_states

            if ax is None:
                p = plt.plot(
                    np.arange(len(self.overall_states)),
                    ys,
                    label="Episode state",
                    color="g",
                )
            else:
                p = ax.plot(
                    np.arange(len(self.overall_states)),
                    ys,
                    label="Episode state",
                    color="g",
                )
            p2 = None
            if self.state_interval:
                if index is not None:
                    y_ints = []
                    for interval in self.state_intervals:
                        y_ints.append([state[index] for state in interval])
                else:
                    y_ints = self.state_intervals
                if ax is None:
                    p2 = plt.plot(
                        np.arange(len(self.state_intervals)),
                        [np.mean(interval) for interval in y_ints],
                        label="Mean interval state",
                        color="orange",
                    )
                    plt.legend(loc="upper left")
                else:
                    p2 = ax.plot(
                        np.arange(len(self.state_intervals)) * self.state_interval,
                        [np.mean(interval) for interval in y_ints],
                        label="Mean interval state",
                        color="orange",
                    )
                    ax.legend(loc="upper left")
            return p, p2

        if self.state_type == spaces.Discrete:
            figure = plt.figure(figsize=(20, 20))
            canvas = FigureCanvas(figure)
            p, p2 = plot_single()
            canvas.draw()
        elif self.state_type == spaces.Dict:
            raise NotImplementedError

        elif self.state_type == spaces.Tuple:
            raise NotImplementedError

        elif (
            self.state_type == spaces.MultiDiscrete
            or self.state_type == spaces.MultiBinary
            or self.state_type == spaces.Box
        ):
            if self.state_type == spaces.MultiDiscrete:
                state_length = len(self.env.observation_space.nvec)
            elif self.state_type == spaces.MultiBinary:
                state_length = self.env.observation_space.n
            else:
                state_length = len(self.env.observation_space.high)
            if state_length == 1:
                figure = plt.figure(figsize=(20, 20))
                canvas = FigureCanvas(figure)
                p, p2 = plot_single()
            elif state_length < 5:
                dim = 1
                figure, axarr = plt.subplots(state_length)
            else:
                dim = state_length % 4
                figure, axarr = plt.subplots(state_length % 4, state_length // dim)
            figure.suptitle("State over time")
            canvas = FigureCanvas(figure)
            for i in range(state_length):
                if state_length == 1:
                    continue

                x = False
                if i % dim == dim - 1:
                    x = True
                if state_length < 5:
                    p, p2 = plot_single(axarr[i], i, y=True, x=x)
                else:
                    y = i % state_length // dim == 0
                    p, p2 = plot_single(axarr[i % dim, i // dim], i, x=x, y=y)
            canvas.draw()
        width, height = figure.get_size_inches() * figure.get_dpi()
        img = np.fromstring(canvas.tostring_rgb(), dtype="uint8").reshape(
            int(height), int(width), 3
        )
        return img
