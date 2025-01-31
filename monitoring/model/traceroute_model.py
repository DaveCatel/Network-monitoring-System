# model/traceroute_model.py
import asyncio
import platform
import subprocess

class TracerouteModel:
    def __init__(self, ip, max_hop=5):
        self.ip = ip
        self.max_hop = max_hop

    async def execute_traceroute(self):
        """Run traceroute command with a limit on the number of hops and return the result."""
        loop = asyncio.get_event_loop()
        
        # Detect the operating system
        os_type = platform.system()

        # Define the traceroute command based on the OS
        if os_type == "Windows":
            command = f"tracert -h {self.max_hop} {self.ip}"
        else:
            command = f"traceroute -m {self.max_hop} {self.ip}"

        try:
            # Use run_in_executor to avoid blocking the event loop
            result = await loop.run_in_executor(None, self.run_traceroute_command, command)
            return result
        except Exception as e:
            return f"Traceroute failed for {self.ip}: {str(e)}."

    def run_traceroute_command(self, command):
        """Run the traceroute command and return the output."""
        try:
            print(f"Running command: {command}")  # Debug statement
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Debug output
            print(f"Traceroute command output: {result.stdout.strip()}")
            print(f"Traceroute command error: {result.stderr.strip()}")

            if result.returncode == 0:
                return result.stdout.strip()  # Capture output on success
            else:
                return f"Traceroute failed with return code {result.returncode}: {result.stderr.strip()}"
        except Exception as e:
            print(f"Exception during traceroute: {str(e)}")  # Debug statement
            return None  # Handle exceptions gracefully