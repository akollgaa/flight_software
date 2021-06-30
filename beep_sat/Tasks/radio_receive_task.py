# Task to listen for "killswitch" command on Radio

# import Tasks.stop_tasks as stop_tasks

class Task:
    priority = 1
    frequency = 1
    task_id = 1

    def __init__(self, satellite):
        self.cubesat = satellite
        self.include = True
        self.cubesat.radio1.listen()


    # this should be moved to radio library for generic await receive
    def __await__(self):

        while not self.cubesat.radio1.rx_done():
            yield
        message = self.cubesat.radio1.receive()
        print(message==b'killswitch')
        msg_text = str(message, "ascii")
        if msg_text == "killswitch":
            print("Sending message.....")
            self.cubesat.radio1.send(
                "Killswitch received, Bye World......", keep_listening=True
            )

            #Stop desired tasks
            for t in self.cubesat.scheduled_objects:
                t.stop()
            # stop_tasks.StopTask(self.cubesat, 3, [1,2,3]).stop()

    async def main_task(self):
        print("Awaiting message")
        await self
        print("Done awaiting message")


