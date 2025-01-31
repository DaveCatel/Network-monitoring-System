# controller/hops_controller.py
from model.hops_model import HopsModel
from view.hops_view import HopsView

class HopsController:
    def __init__(self):
        self.model = HopsModel()
        self.view = HopsView()

    # Add a new hop and update the view
    def add_hop(self, name, ip):
        if self.model.add_hop(name, ip):
            self.view.display_message(f"Added hop: {name} -> {ip}")
        else:
            self.view.display_message(f"Hop {name} already exists.")

    # Remove a hop and update the view
    def remove_hop(self, name):
        if self.model.remove_hop(name):
            self.view.display_message(f"Removed hop: {name}")
        else:
            self.view.display_message(f"Hop {name} does not exist.")

    # List current hops
    def list_hops(self):
        hops = self.model.list_hops()
        self.view.display_hops(hops)

    # Clear all hops and update the view
    def clear_hops(self):
        self.model.clear_hops()
        self.view.display_message("All hops have been removed.")

    # Get hops data for API response
    def get_hops_data(self):
        return self.model.list_hops()  # Assuming this returns the hops data needed for the API