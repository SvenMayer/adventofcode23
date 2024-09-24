#! /usr/bin/python3
PLOT_DATA = False

if PLOT_DATA:
    import matplotlib.pyplot as plt
    plt.close("all")

import numpy as np



TEST_DATA1 = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
TEST_DATA2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""

class Node:
    def __init__(self, name, no_inp):
        self.name = name
        self.no_inputs = no_inp
        self.state = 0

    def set_input(self, inp, pulse):
        pass


class Broadcast(Node):
    def __init__(self, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)

    def set_input(self, inp, pulse):
        return pulse


class FlipFlop(Node):
    def __init__(self, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)

    def set_input(self, inp, pulse):
        if pulse == 0:
            self.state = (self.state + 1) % 2
            return self.state

class Conjecture(Node):
    def __init__(self, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)
        self.allset_comp = 2**self.no_inputs - 1

    def set_input(self, inp, pulse):
        if pulse:
            self.state |= 1 << inp
        else:
            self.state &= ~(1 << inp)
        if self.state == self.allset_comp:
            return 0
        return 1

class Blank(Node):
    def __init__(self, *args, **kwargs):
        Node.__init__(self, *args, **kwargs)

    def set_input(self, inp, pulse):
        return None


class Network:
    def __init__(self, data):
        self.network, self.broadcast = self.parse_input(data)
        self.rx_pressed = False
        self.button_count = 0
        self.mg_states = []

    @staticmethod
    def parse_input(data):
        no_inputs = dict()
        idx_dict = dict()
        known_outputs = set()
        node_list = []
        for idx, ln in enumerate(data.split("\n")):
            ln = ln.strip()
            if len(ln) == 0:
                continue
            node, outputs = ln.split("->")
            node = node.strip(" %&")
            idx_dict[node] = idx
            node_list.append((ln[0], node, outputs))
            for out in outputs.split(","):
                out = out.strip()
                known_outputs.add(out)
                if out not in no_inputs:
                    no_inputs[out] = 1
                else:
                    no_inputs[out] += 1
        network = []
        act_input = dict([(itm, 0) for itm in no_inputs.keys()])
        broadcast = None
        blank_outputs = []
        for out in known_outputs:
            if out in idx_dict.keys():
                continue
            no = len(node_list) + len(blank_outputs)
            idx_dict[out] = no
            blank_outputs.append((Blank(out, no_inputs[out]), (no, 0)))
        for n in node_list:
            if n[0] == "b":
                node = Broadcast(n[1], 1)
                broadcast = len(network)
            elif n[0] == "%":
                node = FlipFlop(n[1], no_inputs[n[1]])
            elif n[0] == "&":
                node = Conjecture(n[1], no_inputs[n[1]])
            connections = []
            for out in n[2].split(","):
                out = out.strip()
                connections.append((idx_dict[out], act_input[out]))
                act_input[out] += 1
            network.append((node, connections))
        network.extend(blank_outputs)
        return network, broadcast

    def push_button(self):
        self.button_count += 1
        lowhigh = [0, 0]
        events = [(self.broadcast, 0, 0)]
        while len(events):
            idx, inp, pulse = events.pop(0)
            lowhigh[pulse] += 1
            n, outs = self.network[idx]
            if n.name == "rx" and pulse == 0:
                self.rx_pressed = True
            res = n.set_input(inp, pulse)
            if n.name == "mg":
                self.mg_states.append((self.button_count, n.state))
            if res is None:
                continue
            events.extend([(o[0], o[1], res) for o in outs])
        return lowhigh

    @property
    def networkisreset(self):
        for n, _ in self.network:
            if n.state != 0:
                return False
        return True

    def cycle_network(self, nmax):
        low_pulse = []
        high_pulse = []
        lh = self.push_button()
        low_pulse.append(lh[0])
        high_pulse.append(lh[1])
        n = 1
        while (n < nmax) and not self.networkisreset:
            lh = self.push_button()
            low_pulse.append(low_pulse[-1] + lh[0])
            high_pulse.append(high_pulse[-1] + lh[1])
            n += 1
        return low_pulse, high_pulse

    def get_pulses(self, nbutton):
        low_list, high_list = self.cycle_network(nbutton)
        n_cylce = len(low_list)
        rem = nbutton % n_cylce
        n_mult = nbutton // n_cylce
        if rem > 0:
            return low_list[-1] * n_mult + low_list[rem-1], high_list[-1] * n_mult + high_list[rem-1]
        return low_list[-1] * n_mult, high_list[-1] * n_mult


def solution1(data):
    network = Network(data)
    lw = network.get_pulses(1000)
    return lw[0] * lw[1]


def solution2(data):
    network = Network(data)
    for i in range(10000):
        network.push_button()
    I = [], [], [], [], []
    B = set(), set(), set(), set()
    for ln in network.mg_states:
        i0 = ln[1] & 0b1
        i1 = (ln[1] & 0b10) // 0b10
        i2 = (ln[1] & 0b100) // 0b100
        i3 = (ln[1] & 0b1000) // 0b1000
        I[0].append(ln[0])
        I[1].append(i0)
        I[2].append(i1)
        I[3].append(i2)
        I[4].append(i3)
        if i0:
            B[0].add(ln[0])
        if i1:
            B[1].add(ln[0])
        if i2:
            B[2].add(ln[0])
        if i3:
            B[3].add(ln[0])
    if PLOT_DATA:
        fig, ax = plt.subplots(5, 1, sharex=True)
        for i, ax_ in enumerate(ax):
            ax_.plot(I[i])
        fig.show()

    B_CTR = [sorted([itm for itm in B[i]]) for i in range(len(B))]
    lcm_1 = np.lcm(B_CTR[0][0], B_CTR[1][0])
    lcm_2 = np.lcm(B_CTR[2][0], B_CTR[3][0])
    return np.lcm(lcm_1, lcm_2)


with open("../../inputs/day20/input", "r") as fid:
    print("Test Data")
    print(solution1(TEST_DATA2))

    data = fid.read()
    print("Solution 1")
    print(solution1(data))

    print("Solution 2")
    print(solution2(data))