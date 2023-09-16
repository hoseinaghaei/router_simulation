from src.packet import *
from src.queue import RouterQueue


class Processor:
    def __init__(self, rate: float, index: int):
        self.packet = None
        self.start = None
        self.end = None
        self._rate = rate
        self.index = index
        self.total_work_time = 0

    def process(self, packet: Packet, time: float):
        self.packet = packet
        self.start = time
        self.end = time + np.random.exponential(scale=self._rate)
        packet.process_start_time = self.start
        packet.process_end_time = self.end
        packet.processor_index = self.index
        self.total_work_time = self.total_work_time + (self.end - self.start)


class Router:
    def __init__(self, processor_count: int, rate: float, queue: RouterQueue):
        self._processor_count = processor_count
        self.processors = [Processor(rate=rate, index=i + 1) for i in range(processor_count)]
        self.queue = queue

    def get_all_processors_work_time(self):
        processor_work_time_dict = dict()
        for i in range(len(self.processors)):
            processor_work_time_dict[i] = self.processors[i].total_work_time
        return processor_work_time_dict

    def _idle_processor_index(self, time: float):
        for i, processor in enumerate(self.processors):
            if processor.packet is None:
                return i

            if time >= processor.end:
                return i

        return -1

    def accept_packet(self, packet: Packet, time: float) -> Packet | None:
        self.queue.add_packet(packet)
        idle_processor_index = self._idle_processor_index(time)
        if idle_processor_index != -1:
            packet_to_process = self.queue.pop_packet()
            self.processors[idle_processor_index].process(packet_to_process, time)
            return packet_to_process

    def empty_queue(self, time: float):
        processors_end_time = [processor.end for processor in self.processors]
        processors_time = [time for _ in range(self._processor_count)]
        packet = self.queue.pop_packet()
        while packet is not None:
            for i in range(self._processor_count):
                if processors_time[i] >= processors_end_time[i]:
                    self.processors[i].process(packet=packet, time=time)
                    processors_end_time[i] = packet.process_end_time
                    packet = self.queue.pop_packet()
                    if packet is None:
                        return
                else:
                    processors_time[i] = processors_end_time[i]

    def pick_from_queue(self, time: float) -> Packet | None:
        idle_processor_index = self._idle_processor_index(time=time)
        if idle_processor_index != -1:
            packet_to_process = self.queue.pop_packet()
            if packet_to_process is not None:
                self.processors[idle_processor_index].process(packet=packet_to_process, time=time)
                return packet_to_process
