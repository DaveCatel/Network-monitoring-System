# model/traceroute_queue.py
import asyncio
from model.traceroute_model import TracerouteModel
from view.traceroute_view import TracerouteView

class TracerouteQueue:
    def __init__(self):
        self.queue = asyncio.Queue()  # Initialize the queue
        self.traceroute_view = TracerouteView()  # Initialize the view
        self.worker_task = None  # Placeholder for the worker task

    async def start(self):
        """Start the traceroute worker."""
        self.worker_task = asyncio.create_task(self.process_queue())  # Start the worker task

    async def process_queue(self):
        while True:
            ip = await self.queue.get()  # Wait for an IP to process
            traceroute_model = TracerouteModel(ip)
            traceroute_result = await traceroute_model.execute_traceroute()

            if traceroute_result:
                self.traceroute_view.display_result(traceroute_result)
            else:
                self.traceroute_view.display_error("No output from traceroute.")

            self.queue.task_done()  # Mark the task as done

    async def add_to_queue(self, ip):
        await self.queue.put(ip)  # Add an IP to the queue