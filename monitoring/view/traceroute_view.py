# view/traceroute_view.py

from model.traceroute_model import TracerouteModel

class TracerouteView:
    def __init__(self):
        self.traceroute_model = None

    def set_ip(self, ip):
        """Set the IP address for the traceroute."""
        self.traceroute_model = TracerouteModel(ip)

    async def display_traceroute_result(self):
        """Execute the traceroute and display the result."""
        if self.traceroute_model is None:
            print("No IP address set for traceroute.")
            return
        
        result = await self.traceroute_model.execute_traceroute()
        self.display_result(result)

    def display_result(self, result):
        """Display the result of the traceroute."""
        if result:
            print("Traceroute Result:")
            print(result)
        else:
            print("No result to display.")