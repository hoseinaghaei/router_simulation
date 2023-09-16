from src.router import *


class TriggerObject:
    def __init__(self, arrival_not_leave: bool, packet: Packet):
        self._arrival = arrival_not_leave
        self._leave = not arrival_not_leave
        self._packet = packet

    def arrival(self) -> bool:
        return self._arrival

    def leave(self) -> bool:
        return self._leave

    def packet(self) -> Packet:
        return self._packet


class Simulator:
    def __init__(self, router: Router, packets: list):
        self._router = router
        self._packets = packets
        self._arrival_packet_triggers = [TriggerObject(arrival_not_leave=True, packet=i) for i in packets]
        self._leaving_packet_triggers = []
        self._arrival_index = 0
        self._time = 0.0

    def simulate(self):
        while True:
            next_trigger = self._next_trigger()
            if next_trigger is None:
                self._router.empty_queue(time=self._time)
                return

            if next_trigger.arrival():
                self._time = max(next_trigger.packet().arrival_time, self._time)
                processed_packet = self._router.accept_packet(packet=next_trigger.packet(), time=self._time)
                if processed_packet is not None:
                    self._leaving_packet_triggers.append(
                        TriggerObject(arrival_not_leave=False, packet=processed_packet))
            else:
                self._time = next_trigger.packet().process_end_time
                processed_packet = self._router.pick_from_queue(time=self._time)
                if processed_packet is not None:
                    self._leaving_packet_triggers.append(
                        TriggerObject(arrival_not_leave=False, packet=processed_packet))

    def _next_trigger(self) -> TriggerObject | None:
        arrival_packet = None
        leave_packet = None
        if 0 <= self._arrival_index < len(self._arrival_packet_triggers):
            arrival_packet = self._arrival_packet_triggers[self._arrival_index]

        index = 0
        min_value = 1e10
        for i in range(len(self._leaving_packet_triggers)):
            p_end = self._leaving_packet_triggers[i].packet().process_end_time
            if p_end < min_value:
                min_value = p_end
                index = i
                leave_packet = self._leaving_packet_triggers[i]

        if arrival_packet == leave_packet is None:
            return None

        if arrival_packet is None:
            return self._leaving_packet_triggers.pop(index)

        if leave_packet is None:
            self._arrival_index += 1
            return arrival_packet

        if arrival_packet.packet().arrival_time > leave_packet.packet().process_end_time:
            return self._leaving_packet_triggers.pop(index)

        self._arrival_index += 1
        return arrival_packet
