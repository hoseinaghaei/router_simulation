from src.packet import PacketGenerator
from src.queue import FIFO
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
