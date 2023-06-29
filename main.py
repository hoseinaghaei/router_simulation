from src.packet import PacketGenerator
from src.queue import FIFO, WRR
from src.router import Router
from src.simulator import Simulator

X = 10  # 10 packets per second
Y = 0.2  # router processor rate
T = 2  # 2 seconds for simulation time

LENGTH_LIMIT = 2
PROCESSORS_NUM = 2

packet_generator = PacketGenerator(period=T, poison_rate=X)
packets = packet_generator.generate()

queue = FIFO(length_limit=LENGTH_LIMIT)
router = Router(processor_count=PROCESSORS_NUM, rate=Y, queue=queue)

simulator = Simulator(router=router, packets=packets)
simulator.simulate()

max1 = 0

max2 = 0
print(
    "arrival                  drop          p         start                        end                       max1                    max2")
for i in packets:
    if i.processor_index == 1:
        max1 = max(max1, i.process_end_time)
    elif i.processor_index == 2:
        max2 = max(max2, i.process_end_time)

    print(i.arrival_time, "     ", i.drop, "         ", i.processor_index, "    ", i.process_start_time, "      ",
          i.process_end_time, "     ", max1, "      ", max2)


def get_dropped_packets_count(packets_list):
    dropped_count = 0
    for packet in packets_list:
        if packet.drop:
            dropped_count = dropped_count + 1


def get_all_queue_Avg(packets_list):
    queue_times = [packet.queue_time() for packet in packets_list]
    return float(sum(queue_times) / len(queue_times))


def get_each_queue_Avg(packets_list, queue_simulation):
    if isinstance(queue_simulation, WRR):
        high_list = []
        medium_list = []
        low_list = []
        for packet in packets_list:
            if packet.priority() == 1:
                high_list.append(packet.queue_time())
            elif packet.priority() == 2:
                medium_list.append(packet.queue_time())
            else:
                low_list.append(packet.queue_time())
        high_avg = sum(high_list) / len(high_list)
        medium_avg = sum(medium_list) / len(medium_list)
        low_avg = sum(low_list) / len(low_list)
        return high_avg, medium_avg, low_avg

    else:
        return get_all_queue_Avg(packets_list)


def get_queue_length_avg(total_time, packets_list):
    packets_list.sort(key=lambda x: x.arrival_time)
    pass