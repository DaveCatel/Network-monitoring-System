import asyncio
import platform
import subprocess
import time

class PingModel:
    def __init__(self, ip, count=4):
        self.ip = ip
        self.count = count  # Number of packets to send

    async def execute_ping(self):
        """Ping the specified IP and return the average latency along with responses."""
        loop = asyncio.get_event_loop()
        
        # Detect the operating system
        os_type = platform.system()
        command = f"ping -c {self.count} {self.ip}" if os_type != "Windows" else f"ping -n {self.count} {self.ip}"

        try:
            responses = []
            latencies = []
            
            for _ in range(self.count):
                start_time = time.time()  # Start timing
                response = await loop.run_in_executor(None, self.run_ping_command, command)
                end_time = time.time()  # End timing
                
                latency = (end_time - start_time) * 1000  # Convert to milliseconds
                
                if response:
                    responses.append(response)
                    latencies.append(latency)
                else:
                    responses.append(f"Request timed out for {self.ip}.")
                    latencies.append(None)  # Add None for timeouts

                await asyncio.sleep(1)  # Optional: Wait between pings

            # Calculate average latency, ignoring None values
            valid_latencies = [lat for lat in latencies if lat is not None]
            avg_latency = sum(valid_latencies) / len(valid_latencies) if valid_latencies else None
            
            return avg_latency, responses  # Return average latency and raw responses
        except Exception as e:
            return None, f"Ping failed for {self.ip}: {str(e)}."

    def run_ping_command(self, command):
        """Run the ping command and return the output."""
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                return result.stdout.strip()  # Capture output on success
            else:
                return None  # Return None if ping fails
        except Exception as e:
            return None  # Handle exceptions gracefully

async def main():
    ip = input("Enter the IP address to ping: ")
    count = int(input("Enter the number of packets to send (default is 4): ") or 4)

    ping_model = PingModel(ip, count)
    latency, response = await ping_model.execute_ping()

    print(f"Average Latency: {latency:.2f} ms" if latency is not None else "No valid responses.")
    print("Responses:")
    for res in response:
        print(res)

if __name__ == "__main__":
    asyncio.run(main())