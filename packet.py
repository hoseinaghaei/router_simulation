from enum import Enum
import numpy as np


class Priority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


def random_priority():
    ri = np.random.random()
    if ri < 0.2:
        return Priority(1)
    elif ri < 0.5:
        return Priority(2)
    else:
        return Priority(3)


class Packet:
    def __init__(self, priority: Priority, arrival_time: float):
        self._priority = priority
        self.arrival_time = arrival_time
        self.drop = False
        self.processor_index = -1
        self.process_start_time = None
        self.process_end_time = None

    def priority(self) -> int:
        return self._priority.value

    def queue_time(self):
        if self.drop:
            return 0
        return self.process_end_time - self.arrival_time


class PacketGenerator:
    def __init__(self, period: int, poison_rate: int):
        self._T = period
        self._X = poison_rate
        self._packets = []

    def generate(self) -> list:
        self._packets = []
        chunk_size = 1000
        t = 0
        while t < self._T:
            exp_numbers = np.random.exponential(scale=1 / self._X, size=chunk_size)
            for i in range(chunk_size):
                ri = exp_numbers[i]
                t += ri
                if t > self._T:
                    break

                pi = Packet(random_priority(), t)
                self._packets.append(pi)

        return self._packets
