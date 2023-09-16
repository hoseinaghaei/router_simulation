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

## Getting Started

To start using the router simulation script, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/hoseinaghaei/router_simulation.git


1) برای افزایش بهره وری سیستم میتوان پردازنده جدید اضافه کرد و یا از زمانبندی های متنوع دیگر مانند class based queueing و ... استفاده کرد.

میتوان قدرت پردازنده ها را افزایش داد.

2) اگر در ترافیک شبکه اولویت بسته ها مهم باشد که استفاده از راند روبین وزن دار بهتر است

اگر در ترافیک شبکه دچار نوسانات بالا در طی زمان است استفاده از NPPS بهتر است 

ولی ساده ترین حالت استفاده از FIFO است که در آن اولویت اهمیتی ندارد و ترافیک حدودا ثابت است
