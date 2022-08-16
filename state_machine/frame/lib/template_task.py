from lib.debugcolor import co
from state_machine import state_machine


class Task:

    """
    Template task object.
    Stores the task name and color.
    """

    name = 'temp'
    color = 'gray'

    def __init__(self):
        """
        Initialize the Task
        """
        pass

    def debug(self, msg, level=1):
        """
        Print a debug message formatted with the task name and color

        :param msg: Debug message to print
        :type msg: str
        :param level: > 1 will print as a sub-level
        :type level: int
        """
        if level == 1:
            header = f"[{co(msg=self.name,color=self.color)}/{state_machine.state}]"
            print(f"{header:>35} {msg}")
        else:
            print("\t" + f"{'   └── '}{msg}")

    async def main_task(self, *args, **kwargs):
        """
        Contains the code for the user defined task.

        :param `*args`: Variable number of arguments used for task execution.
        :param `**kwargs`: Variable number of keyword arguments used for task execution.
        """
        pass
