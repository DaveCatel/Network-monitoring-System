import asyncio
from controller.ping_controller import PingController

async def main():
    controller = PingController(interval=5)
    await controller.traceroute_queue.start()

    # Add initial hops (could be dynamic or user input)
    initial_hops = [
        ("Adapter", "192.168.1.4"),
        ("Switch", "192.168.1.2"),
        ("Google DNS", "8.8.8.8")
    ]

    for name, ip in initial_hops:
        try:
            controller.hops_controller.add_hop(name, ip)
        except Exception as e:
            print(f"Failed to add hop {name} ({ip}): {e}")

    try:
        print("Starting the pinging process. Press Ctrl+C to stop.")
        await controller.ping_multiple_hops()  # Use await here
    except asyncio.CancelledError:
        print("Ping operation was cancelled.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted. Cleaning up...")
        # Note: You cannot await here directly.
        # You should handle the shutdown process in the main function or elsewhere.