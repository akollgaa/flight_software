import tasko
from lib.pycubed import cubesat

from lib.state_machine_utils import validate_config


class StateMachine:
    """Singleton State Machine Class"""

    def __init__(self):
        pass

    def start(self, start_state: str):
        """Starts the state machine

        Args:
        :param start_state: The state to start the state machine in
        :type start_state: str
        """
        from StateMachineConfig import config, TaskMap, TransitionFunctionMap

        self.config = config
        validate_config(config, TaskMap, TransitionFunctionMap)

        self.states = list(config.keys())
        self.states.sort()

        # init task objects
        self.tasks = {key: task() for key, task in TaskMap.items()}

        # set scheduled tasks to none
        self.scheduled_tasks = {}

        self.state = start_state
        self.switch_to(start_state, force=True)
        tasko.run()

    def stop_all(self):
        """Stops all running tasko processes"""
        for _, task in self.scheduled_tasks.items():
            task.stop()

    def switch_to(self, state_name, force=False):
        """Switches the state of the cubesat to the new state"""

        # prevent (or allow forced) illegal transitions
        if not(state_name in self.config[self.state]['StepsTo'] or force):
            raise ValueError(
                f'You cannot transition from {self.state} to {state_name}')

        # execute transition functions
        if self.state != state_name:
            for fn in config[self.state]['ExitFunctions']:
                fn = TransitionFunctionMap[fn]
                fn(self.state, state_name, cubesat)
            for fn in config[state_name]['EnterFunctions']:
                fn = TransitionFunctionMap[fn]
                fn(self.state, state_name, cubesat)

        # reschedule tasks
        self.stop_all()
        self.scheduled_tasks = {}
        self.state = state_name
        state_config = self.config[state_name]

        for task_name, props in state_config['Tasks'].items():
            if props['ScheduleLater']:
                schedule = tasko.schedule_later
            else:
                schedule = tasko.schedule

            frequency = 1 / props['Interval']
            priority = props['Priority']
            task_fn = self.tasks[task_name].main_task

            self.scheduled_tasks[task_name] = schedule(
                frequency, task_fn, priority)


state_machine = StateMachine()
