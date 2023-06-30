from src.packet import PacketGenerator
from src.queue import FIFO, WRR, NPPS
from src.report import QueueLengthReporter, get_queue_length_avg, get_all_queue_Avg, get_each_queue_Avg, \
    get_dropped_packets_count, get_processors_utilization, show_high_packets_CDF
from src.router import Router
from src.simulator import Simulator

X = 10  # 10 packets per second
Y = 0.2  # router processor rate
T = 2  # 2 seconds for simulation time

LENGTH_LIMIT = 2
PROCESSORS_NUM = 2


def simulate_and_report(queue_simulation):
    packet_generator = PacketGenerator(period=T, poison_rate=X)
    packets = packet_generator.generate()
    router = Router(processor_count=PROCESSORS_NUM, rate=Y, queue=queue_simulation)
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

    print("average length of queue " + str(get_queue_length_avg(packets, T)))
    print(str("average of all queues  ") + str(get_all_queue_Avg(packets)))
    print(str("average of each queues  ") + str(get_each_queue_Avg(packets, queue_simulation)))
    get_processors_utilization(router, T)
    print(str("the count of dropped packets " + str(get_dropped_packets_count(packets))))
    show_high_packets_CDF(packets)
    print(
        "------------------------------------------------------------------------------------------------------------")
    print()
    print()


fifo_queue = FIFO(length_limit=LENGTH_LIMIT)
simulate_and_report(fifo_queue)

wrr_queue = WRR(length_limit=LENGTH_LIMIT, queue_count=3, queue_weights=[2, 3, 5])
simulate_and_report(wrr_queue)

nssp_queue = NPPS(length_limit=LENGTH_LIMIT)
simulate_and_report(nssp_queue)
