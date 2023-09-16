# Router Simulation

This repository contains a router simulation script that models packet processing with an exponential input-output rate and dynamic processor count, featuring different queue policies.

## Overview

The router simulation script is designed to provide insights into packet processing dynamics in a network router. It simulates the arrival, processing, and departure of packets through the router, with the flexibility to adjust various parameters for experimentation.

## Key Simulation Parameters

Before diving into the details of the script, let's understand the global variables that shape the simulation:

- **LENGTH_LIMIT**: The maximum size of the queue in the router.
- **PROCESSORS_NUM**: The number of processors the router has. Note that when a processor processes a packet, it automatically moves to the first one based on the queue policy.
- **X**: The poison rate of incoming packets per second.
- **Y**: The exponential mean time for processors.
- **T**: The duration of the simulation in seconds. You can modify these parameters in the `main.py` file to tailor the simulation to your needs.

## File Descriptions

### 1. `src/packet.py`

This file defines the core packet processing logic and packet characteristics within the simulation. Key components include:

- **Packet Priorities**: There are three kinds of packets with HIGH(1), MEDIUM(2), and LOW(3) priorities, with assumed probabilities of 0.2, 0.3, and 0.5, respectively. You can adjust these probabilities by modifying the `random_priority` function.

- **Packet Class**: This class represents packets with the following attributes:
    - `_priority`: The priority level (1, 2, or 3).
    - `arrival_time`: The time at which the packet arrives at the router.
    - `drop`: A flag indicating whether the router dropped the packet due to a full queue.
    - `processor_index`: The index of the processor that manages the packet.
    - `process_start_time`: The time at which the processor starts handling the packet.
    - `process_end_time`: The time at which the processor finishes processing the packet.

- **Queue Time and System Time**: Two essential definitions in the simulation:
    - Queue Time: The time a packet spends in the queue, calculated as the difference between arrival time and process start time.
    - System Time: The total time a packet spends in the entire system, calculated as the difference between process end time and arrival time if it was not dropped.

- **PacketGenerator Class**: This class generates packets for simulation based on the simulation time and incoming packet rate. It creates a list of packets to be processed during the simulation.

### 2. `src/queue.py`

In this file, we implement three types of queues that extend from the base `RouterQueue` class. The base class contains two essential functions: `add_packet` and `pop_packet`, each of which must be implemented for its specific queue type.

#### a. FIFO Queue (First-In-First-Out)

- `add_packet`: In the FIFO queue, if the queue is full, the packet is dropped; otherwise, it is appended to the end of the list.
- `pop_packet`: This function pops the front packet from the queue if there is any.

#### b. WRR Queue (Weighted Round Robin)

For the WRR queue, you must add a new parameter named `queue_weights`, which represents the weight of each queue. Typically, there are three queues for each priority level. This [link](https://www.educative.io/answers/what-is-the-weighted-round-robin-load-balancing-technique) provides more details on the Weighted Round Robin technique.

- `add_packet`: Similar to the FIFO queue, packets are added to the queue with a priority equal to the packet's priority.

- `pop_packet`: In the WRR queue, we pop packets from the higher priority queue if it has remaining weight. If the higher priority queue is empty or has no remaining weight, we pop packets from the next queue.

#### c. NPPS Queue (Non-Preemptive Priority Scheduling)

Non-Preemptive Priority Scheduling is another queue type implemented in this simulation. If you are unfamiliar with this type of queue, you can refer to this [link](https://www.javatpoint.com/os-non-preemptive-priority-scheduling) for more information.

- `add_packet`: In the NPPS queue, packets are inserted at the first place that has a lower priority. If the chosen queue is full, the packet with the lowest priority in that queue is dropped.

- `pop_packet`: Non-Preemptive Priority Scheduling simply pops the last element from the queue.

### 3. `src/simulator.py`

In this file, we address the challenge of handling packet arrival and departure triggers efficiently within the simulation. Rather than using traditional methods like multi-threading or real-time clock handling, we've implemented a unique solution.

#### Arrival and Departure Triggers

In the `Simulator` class, we treat every Arrival or Departure event as a `TriggerObject`. This approach allows us to manage the simulation in a structured manner. Key properties within the `Simulator` class include:

- `_router`: An instance of the `Router` object that we define later in the simulation.
- `_packets`: A list of packets generated in the `PacketGenerator` class.
- `_arrival_packet_triggers`: A list of `TriggerObject`s, each representing an arrival event. These triggers are created for each packet generated and are used to control packet routing.
- `_leaving_packet_triggers`: When a packet finishes processing, a leaving trigger is generated. We use this list to assign a new packet to idle processors.
- `_arrival_index`: Tracks which arrival packet is next in line for processing.
- `_time`: Represents the simulated system's current time.

#### Simulation Algorithm

The heart of the simulation lies in the `simulate` function, where we process packets until they have all reached their destinations. The algorithm is as follows:

1. Find the next trigger object to process.
2. If no triggers are left, it indicates that we have processed all incoming packets, and we need to handle packets that are still in the queue using the `empty_queue` function from the `src/router.py` module.
3. If the trigger is an arrival, we first move the simulated time to match the arrival time (if it's greater than our current time). Then, we call the `accept_packet` function of the `Router` class. If the router returns a packet that is currently being processed, we add it to the `_leaving_packet_triggers` list.
4. If the trigger is a departure, we advance the `_time` to the `process_end_time` and instruct the router to select another packet from the queue using the `pick_from_queue` function.

The `_next_trigger` function plays a crucial role by selecting the trigger that is scheduled to occur next between arrival packets and departing ones, ensuring the simulation proceeds in chronological order.

## Implementation Details

[Provide additional implementation details, insights, or code snippets that are essential for understanding and using your simulation script...]

## Usage

[Explain how to use the simulator to run your router simulation with arrival and departure triggers...]

## Contributing

[If you have ideas for improving the simulator or wish to contribute to its development, describe how others can contribute. Follow the standard GitHub Fork and Pull Request workflow to get started...]

## License

[Include information about the project's licensing, such as the MIT License...]

## Contact

[If users have questions, suggestions, or need assistance with the simulator script or its components, provide contact information for the repository owner...]

Thank you for your interest in the router simulation project and its innovative approach to handling packet arrival and departure triggers. We hope this simulation serves as a valuable tool for networking experimentation.



1) برای افزایش بهره وری سیستم میتوان پردازنده جدید اضافه کرد و یا از زمانبندی های متنوع دیگر مانند class based queueing و ... استفاده کرد.

میتوان قدرت پردازنده ها را افزایش داد.

2) اگر در ترافیک شبکه اولویت بسته ها مهم باشد که استفاده از راند روبین وزن دار بهتر است

اگر در ترافیک شبکه دچار نوسانات بالا در طی زمان است استفاده از NPPS بهتر است 

ولی ساده ترین حالت استفاده از FIFO است که در آن اولویت اهمیتی ندارد و ترافیک حدودا ثابت است
