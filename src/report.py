from src.queue import WRR
import matplotlib.pyplot as plt
import numpy as np


class QueueEvent:
    # arrive = true and departure = false
    def __init__(self, time, arrive_or_departure):
        self.time = time
        self.arrive_or_departure = arrive_or_departure


class QueueLengthReporter:
    def __init__(self, packet_list, T):
        self.packet_list = packet_list
        self.T = T

    def __create_queue_event_list(self):
        event_list = list()
        for packet in self.packet_list:
            if packet.arrival_time is not None:
                event_list.append(QueueEvent(packet.arrival_time, True))
            if packet.process_start_time is not None:
                event_list.append(QueueEvent(packet.process_start_time, False))
        event_list.sort(key=lambda x: x.time)
        return event_list

    def calculate_queue_length_avg(self):
        event_list = self.__create_queue_event_list()
        t = 0  # start of simulation
        event_index = 0
        queue_length = 0
        time_by_length = dict()
        while event_index < len(event_list):
            event = event_list[event_index]
            if event.arrive_or_departure:
                queue_length = queue_length + 1
            else:
                queue_length = queue_length - 1

            if event_index != len(event_list) - 1 and event_list[event_index + 1].time == event.time:
                event_index = event_index + 1
                continue

            time_diff = event.time - t

            if queue_length not in time_by_length.keys():
                time_by_length[queue_length] = time_diff
            else:
                time_by_length[queue_length] = time_by_length[queue_length] + time_diff

            t = event.time
            event_index = event_index + 1

        sum = 0
        for length, time_distance in time_by_length.items():
            sum = length * time_distance + sum

        return float(sum / self.T)


def get_dropped_packets_count(packets_list):
    dropped_count = 0
    for packet in packets_list:
        if packet.drop:
            dropped_count = dropped_count + 1
    return dropped_count


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
        high_avg = 0
        medium_avg = 0
        low_avg = 0
        if len(high_list) != 0:
            high_avg = float(sum(high_list) / len(high_list))
        if len(medium_list) != 0:
            medium_avg = float(sum(medium_list) / len(medium_list))
        if len(low_list) != 0:
            low_avg = float(sum(low_list) / len(low_list))
        return high_avg, medium_avg, low_avg

    else:
        return get_all_queue_Avg(packets_list)


def get_queue_length_avg(packets_list, total_time):
    queue_length_calculator = QueueLengthReporter(packets_list, total_time)
    return queue_length_calculator.calculate_queue_length_avg()


def get_processors_utilization(router, total_time):
    processors_work_time_dict = router.get_all_processors_work_time()
    for index, work_time in processors_work_time_dict.items():
        print(str("processor number " + str(index) + " server utilization  " + str(float(work_time / total_time))))


def show_high_packets_CDF(packet_list):
    high_packets_time = []
    for packet in packet_list:
        if packet.priority() == 1:
            high_packets_time.append(packet.queue_time())

    high_packets_time = np.sort(high_packets_time)
    cdf = np.arange(1, len(high_packets_time) + 1) / len(high_packets_time)

    plt.plot(high_packets_time, cdf, marker='.', linestyle='none')
    plt.xlabel('Data')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution Function (CDF)')
    plt.grid(True)
    plt.show()
