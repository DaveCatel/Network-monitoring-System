# model/hops_model.py
import json
import os

class HopsModel:
    def __init__(self, filename='hops.json'):
        self.hops = {}  # Dictionary to store hops
        self.filename = filename
        self.load_hops()  # Load existing hops from the file

    # Add a new hop to the network
    def add_hop(self, name, ip):
        if name not in self.hops:
            self.hops[name] = ip
            self.save_hops() 
            return True
        return False

    # Remove a hop from the network
    def remove_hop(self, name):
        if name in self.hops:
            del self.hops[name]
            self.save_hops()
            return True
        return False

    # Return dictionary of current hops
    def list_hops(self):
        return self.hops

    # Clear all hops from the network
    def clear_hops(self):
        self.hops.clear()
        self.save_hops()

    # Save the list of hops to a JSON file
    def save_hops(self):
        with open(self.filename, 'w') as f:
            json.dump(self.hops, f)

    # Load the list of hops from a JSON file
    def load_hops(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.hops = json.load(f)