# controller/ping_controller.py
import asyncio
from model.ping_model import PingModel
from view.ping_view import PingView
from controller.hops_controller import HopsController
from controller.traceroute_controller import TracerouteController
from model.traceroute_queue import TracerouteQueue

ping_results = {}
class PingController:
    def __init__(self, interval=5):
        self.hops_controller = HopsController()
        self.view = PingView()
        self.traceroute_queue = TracerouteQueue()
        self.traceroute_controller = TracerouteController()  # Initialize TracerouteController
        self.interval = interval


    async def ping_multiple_hops(self):
        while True:
            hops = self.hops_controller.model.list_hops()

            if not hops:
                self.view.display_message("No hops to ping.")
                await asyncio.sleep(self.interval)
                continue

            tasks = [self.ping_host(name, ip) for name, ip in hops.items()]
            try:
                results = await asyncio.gather(*tasks, return_exceptions=True)

                self.view.display_results(results)
                
            except asyncio.CancelledError:
                self.view.display_message("Ping operation was cancelled.")
                break  # Break the loop if cancelled
            await asyncio.sleep(self.interval)

    async def ping_host(self, name, ip):
        model = PingModel(ip)
        latency, result = await model.execute_ping()

        if latency is not None:
            ping_results[ip] = {
                'name': name,
                'latency': latency,
                'result': result
            }
            # Check for high latency or packet loss
            if latency > 100 or "loss" in result.lower():
                self.view.display_message(f"High latency or packet loss detected for {name} ({ip}). Initiating traceroute...")
                self.traceroute_controller.set_ip(ip)  # Set the IP for traceroute
                await self.traceroute_controller.perform_traceroute()  # Call the traceroute controller
                return f"{name} ({ip}): {result}. Traceroute initiated."

            return f"{name} ({ip}): {result}. Average Latency: {latency:.2f} ms"  # Format latency safely
        else:
            return f"{name} ({ip}): {result}. Latency not available."  # Handle None case