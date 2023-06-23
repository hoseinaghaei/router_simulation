from packet import Packet


class RouterQueue:
    def __init__(self, length_limit: int):
        self.limit = length_limit
        self.queue = []

    def add_packet(self, packet: Packet):
        pass

    def pop_packet(self) -> Packet | None:
        pass


class FIFO(RouterQueue):
    def add_packet(self, packet: Packet):
        if len(self.queue) < self.limit:
            self.queue.append(packet)
        else:
            packet.drop = True

    def pop_packet(self) -> Packet | None:
        if len(self.queue) > 0:
            return self.queue.pop(0)


class WRR(RouterQueue):
    def __init__(self, length_limit: int, queue_count: int, queue_weights: list):
        super().__init__(length_limit)
        self._queue_count = queue_count
        self.queue = [[] for _ in range(queue_count)]
        self._default_queue_weights = queue_weights
        self._queue_weights = [i for i in queue_weights]

    def add_packet(self, packet: Packet):
        if len(self.queue[packet.priority() - 1]) < self.limit:
            self.queue[packet.priority() - 1].append(packet)
        else:
            packet.drop = True

    def pop_packet(self) -> Packet | None:
        for i in range(self._queue_count):
            if len(self.queue[i]) > 0 and self._queue_weights[i] > 0:
                self._queue_weights[i] -= 1
                return self.queue[i].pop(0)

        for i in range(self._queue_count):
            if len(self.queue[i]) > 0 and self._queue_weights[i] == 0:
                self._queue_weights[i] = self._default_queue_weights[i] - 1
                return self.queue[i].pop(0)


class NPPS(RouterQueue):
    def add_packet(self, packet: Packet):
        if len(self.queue) == 0:
            if self.limit > 0:
                self.queue.append(packet)
            else:
                packet.drop = True
        else:
            priority = packet.priority()
            for i, elem in enumerate(self.queue):
                if elem.priority() >= priority:
                    self.queue.insert(i, packet)
                    if len(self.queue) > self.limit:
                        self.queue.pop(0).drop = True
                    return

    def pop_packet(self) -> Packet | None:
        if len(self.queue) > 0:
            return self.queue.pop()
