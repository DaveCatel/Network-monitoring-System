from flask import Flask, request, jsonify
from controller.ping_controller import PingController
from controller.hops_controller import HopsController
from controller.traceroute_controller import TracerouteController
from threading import Thread
import re

app = Flask(__name__)

# Initialize controllers
hops_controller = HopsController()
ping_controller = PingController()
traceroute_controller = TracerouteController()

# In-memory storage for ping results
ping_results = {}

def is_valid_ip(ip):
    """Validate the given IP address."""
    pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
    return pattern.match(ip) is not None

@app.route('/traceroute', methods=['POST'])
def traceroute():
    data = request.get_json()
    ip_address = data.get('ip')

    if not ip_address:
        return jsonify({'error': 'No IP address provided.'}), 400
    
    if not is_valid_ip(ip_address):
        return jsonify({'error': 'Invalid IP address format.'}), 400

    traceroute_controller.set_ip(ip_address)  # Set IP in the controller
    result = traceroute_controller.perform_traceroute()  # Perform the traceroute

    return jsonify({'result': result}), 200  # Assuming result is returned as a string

@app.route('/ping', methods=['POST'])
def ping():
    """Endpoint to start pinging multiple hops."""
    try:
        thread = Thread(target=ping_controller.ping_multiple_hops)
        thread.start()  # Start pinging in a separate thread
        return jsonify({'message': 'Ping operation started.'}), 202  # Accepted status
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Internal server error

@app.route('/hops', methods=['GET'])
def get_hops():
    try:
        hops_data = hops_controller.get_hops_data()
        return jsonify(hops_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ping/results', methods=['GET'])
def get_ping_results():
    """Endpoint to retrieve ping results."""
    return jsonify(ping_results)

if __name__ == '__main__':
    app.run(debug=True)