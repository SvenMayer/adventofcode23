import pyvis

def graph_network(data):
    network = pyvis.network.Network(directed=True)
    known_nodes = set()
    for ln in data.split("\n"):
        ln = ln.strip()
        if len(ln) == 0:
            continue
        inp, outp = ln.split("->")
        inp = inp.strip()
        outp = outp.strip()
        if inp[0] in "%&":
            inp = inp[1:]
        known_nodes.add(inp)
        for n in outp.split(","):
            n = n.strip()
            known_nodes.add(n)
    network.add_nodes(known_nodes)
    for ln in data.split("\n"):
        ln = ln.strip()
        if len(ln) == 0:
            continue
        inp, outp = ln.split("->")
        inp = inp.strip()
        outp = outp.strip()
        if inp[0] in "%&":
            inp = inp[1:]
        for n in outp.split(","):
            n = n.strip()
            network.add_edge(inp, n)
    network.show("network.html")


with open("../../inputs/day20/input", "r") as fid:
    graph_network(fid.read())
