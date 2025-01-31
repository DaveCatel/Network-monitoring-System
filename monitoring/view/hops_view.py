# view/hops_view.py
class HopsView:
    def display_hops(self, hops):
        """Display the list of hops."""
        if hops:
            print("Current Hops:")
            for name, ip in hops.items():
                print(f"  {name}: {ip}")
        else:
            print("No hops available.")

    # Display a message
    def display_message(self, message):
        print(message)