# controller/traceroute_controller.py
import asyncio
from model.traceroute_model import TracerouteModel
from view.traceroute_view import TracerouteView

class TracerouteController:
    def __init__(self):
        self.view = TracerouteView()
        self.ip_address = None  # Initialize IP address here

    def set_ip(self, ip):
        """Set the IP address for traceroute."""
        self.ip_address = ip

    async def perform_traceroute(self):
        """Perform the traceroute operation."""
        if not self.ip_address:
            raise ValueError("IP address not set.")
        
        self.view.set_ip(self.ip_address)  # Set the IP for the view, if needed
        await self.view.display_traceroute_result()  # Execute and display the result