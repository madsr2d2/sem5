import sympy
import pandas as pd

# Load the topology and streams from CSV
topology_df = pd.read_csv("topology.csv", header=None)
streams_df = pd.read_csv("streams.csv", header=None)

# Define link speeds (in bits per second)
link_speeds = {
    'ES': 1e9,  # End System: 1 Gbps
    'SW': 10e9  # Switch: 10 Gbps
}

# Define the device class


class Device:
    def __init__(self, env, device_type, name, ports, domain):
        self.env = env
        self.device_type = device_type
        self.name = name
        self.ports = ports
        self.domain = domain
        self.link_speed = link_speeds.get(device_type, None)
        self.queue = sympy.Store(env)  # Create a store for incoming packets

        if self.link_speed is None:
            raise ValueError(
                f"Unknown device type '{device_type}' for device '{name}'.")

        # Start the packet processing process
        self.process = env.process(self.run())

    def run(self):
        while True:
            # Wait for packets to be queued
            packet = yield self.queue.get()
            # Process the packet
            # Simulate the processing delay
            yield self.env.timeout(packet['delay'])
            packet['finish_time'] = self.env.now  # Mark the finish time
            print(
                f"Packet {packet['id']} processed by {self.name} at time {self.env.now}")

            # Save the result for output
            results.append({
                'Packet ID': packet['id'],
                'Source': packet['src'],
                'Destination': packet['dest'],
                'Size': packet['size'],
                'Start Time': packet['start_time'],
                'Finish Time': packet['finish_time'],
                # Convert to microseconds
                'E2E Delay (us)': (packet['finish_time'] - packet['start_time']) * 1e6
            })

    def send_packet(self, packet):
        self.queue.put(packet)


# Dictionary to store devices
devices = {}
links = []

# Create devices based on the topology DataFrame


def create_devices(topology_df):
    for _, row in topology_df.iterrows():
        if row[0] in ['ES', 'SW']:  # Only process devices
            device_type = row[0]  # Device Type
            name = row[1]         # Device Name
            ports = row[2]        # Number of Ports
            domain = row[3]       # Domain
            device = Device(env, device_type, name, ports, domain)
            devices[name] = device

# Create links based on the topology DataFrame


def create_links(topology_df):
    for _, row in topology_df.iterrows():
        if row[0] == 'LINK':  # Only process links
            links.append({
                'link_id': row[1],
                'source_device': row[2],
                'source_port': row[3],
                'destination_device': row[4],
                'destination_port': row[5],
                'domain': row[6]
            })

# Calculate transmission delay based on stream size and link speed


def calculate_transmission_delay(stream_size, link_speed):
    stream_size_bits = stream_size * 8  # Convert size to bits
    return (stream_size_bits / link_speed) * 1e6  # Convert to microseconds

# Function to calculate end-to-end delay for a stream


def calculate_e2e_delay(stream):
    src_device = devices[stream[3]]
    dest_device = devices[stream[4]]

    # Calculate transmission delay
    delay = calculate_transmission_delay(stream[5], src_device.link_speed)
    return delay, src_device, dest_device

# Stream class to represent the streams


class Stream:
    def __init__(self, stream_id, src, dest, size):
        self.stream_id = stream_id
        self.src = src
        self.dest = dest
        self.size = size

    def transmit(self):
        delay, src_device, dest_device = calculate_e2e_delay(
            [self.stream_id, None, None, self.src, self.dest, self.size, None, None])

        # Create a packet representation
        packet = {'id': self.stream_id, 'src': self.src, 'dest': self.dest, 'size': self.size,
                  'delay': delay, 'start_time': env.now}

        # Send packet from source to destination
        src_device.send_packet(packet)

        # Wait for the processing to finish at destination
        yield env.timeout(delay)


# Create a list to store results
results = []

# Create topology and streams
try:
    env = sympy.Environment()  # Initialize the environment
    create_devices(topology_df)
    create_links(topology_df)

    # Create and simulate streams
    for _, row in streams_df.iterrows():
        stream_id = row[1]        # Assuming stream ID is in the second column
        src = row[3]              # Source node
        dest = row[4]             # Destination node
        size = row[5]             # Size
        stream = Stream(stream_id, src, dest, size)
        env.process(stream.transmit())  # Start transmitting the stream

    env.run()  # Run the simulation

    # Save results to a CSV file
    output_df = pd.DataFrame(results)
    output_df.to_csv("simulation_results.csv", index=False)
    print("Simulation complete. Results saved to 'simulation_results.csv'.")

except ValueError as e:
    print(e)
