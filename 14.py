text = """
12 VJWQR, 1 QTBC => 6 BGXJV
12 BGTMN, 2 DRKQR => 2 TVSF
2 FTFK => 2 THNDN
13 LKRTN, 7 MDPN, 12 NZKQZ => 5 LPWPD
1 HDKX, 3 DWZS, 1 RCBQS => 1 DCRK
14 ZCMF => 6 ZKHLC
3 ZFVH, 2 ZCMF, 1 SCJG, 1 LQWJ, 4 BGBJ, 1 NHPR, 3 VKZFJ, 7 FWFXZ => 4 QVJMP
11 TNMLB => 7 NVDCR
1 LPWPD, 1 BGBJ => 2 SCJG
3 DFCVF, 1 QGSN => 6 PQXG
1 BGXJV, 1 THNDN => 4 BCQN
3 LKRTN => 9 MDPN
2 THNDN, 13 RCKZ, 10 FQSLN => 8 VKZFJ
4 LBCZ, 9 LWHS => 1 FQSLN
6 WSRVZ => 9 TNMLB
8 FQSLN, 14 JQRF, 4 BGTMN => 5 QGSN
4 ZCMF, 4 PLSM, 2 ZHTX => 8 TDHPM
2 RSKC, 10 SHBC, 8 MDPN => 6 FMSZ
2 VJWQR => 2 FPTV
12 DRKQR => 6 NHPR
35 QJLF, 22 BGTMN, 11 VJWTR, 1 QVJMP, 8 LQWJ, 1 TWLC, 16 NXZCH, 18 THKF, 42 JBLM => 1 FUEL
2 BGTMN, 4 XJKN => 8 ZCMF
4 TVSF => 3 RSKC
7 HRWS, 1 TVSF => 3 ZHTX
134 ORE => 4 WSRVZ
1 VKZFJ, 1 TWLC, 4 ZHTX, 5 THNDN, 12 PLVN, 1 ZFXNP, 1 PQXG, 6 CWHV => 7 VJWTR
20 XJKN, 1 LCKW, 3 NZKQZ => 7 HDKX
1 LPWPD => 8 RCKZ
4 RCBQS, 1 NVDCR => 5 BGBJ
8 BGXJV => 4 BGTMN
13 QBDX, 16 BGXJV => 6 NZKQZ
2 LPWPD => 3 DRKQR
4 QBDX => 7 XJKN
12 LCKW, 9 NVDCR => 3 RCBQS
142 ORE => 3 QBDX
1 WXHJF => 1 XKDJ
2 RSKC => 2 CWHV
2 ZHTX, 1 ZFXNP => 6 JQRF
1 FTFK, 1 TVSF, 1 QBDX => 2 JBLM
1 TDHPM, 14 NHPR, 3 QPSF => 5 ZFVH
3 GDTPC, 1 ZKHLC => 8 ZFXNP
5 DWZS => 3 LQWJ
1 FTFK, 4 LBCZ, 13 NHPR => 1 FWFXZ
1 RCBQS, 12 SHBC => 9 FTFK
1 WSRVZ, 1 XKDJ => 5 LKRTN
2 BGTMN, 1 MDPN => 5 PLSM
2 BGXJV, 17 XKDJ, 4 FPTV => 9 LCKW
148 ORE => 2 QTBC
110 ORE => 2 VJWQR
42 ZFXNP, 15 RCKZ, 8 GDTPC => 3 QJLF
13 HRWS => 4 GDTPC
34 HRWS => 4 DFCVF
2 VKZFJ, 2 NHPR, 16 PLVN, 1 QPSF, 13 LBCZ, 4 DCRK, 10 LWHS => 7 NXZCH
3 CWHV, 1 THNDN => 7 LWHS
1 BGXJV, 2 QBDX => 5 DWZS
9 LQWJ => 8 QPSF
21 BCQN, 3 FMSZ, 1 RSKC => 5 THKF
118 ORE => 6 WXHJF
11 FMSZ => 9 TWLC
28 PLSM => 5 SHBC
1 ZKHLC, 23 SCJG => 7 LBCZ
17 DWZS, 16 THNDN => 9 PLVN
7 HDKX => 9 HRWS
""".strip()


import re
import math
from collections import defaultdict


def parse_reactions(text):
    reactions = dict()
    for line in text.splitlines():
        inputs, output = line.split('=>')
        inputs = re.findall('\d+ \w+', inputs)
        output = re.findall('\d+ \w+', output)[0]
        out_quantity, out_chemical = int(output.split()[0]), output.split()[1]
        reactions[out_chemical] = {'q': out_quantity, 'l': []}

        for inp in inputs:
            in_quantity, in_chemical = int(inp.split()[0]), inp.split()[1]
            reactions[out_chemical]['l'].append({'c': in_chemical, 'q': in_quantity})
        
    return reactions


def cost(tree, node, required, stocks, reactions, needed_ore=None):
    if needed_ore is None:
        needed_ore = []
        
    if node == 'ORE':
        needed_ore.append(required)
        return

    available = stocks[node]
    use_available = min(required, available)
    needed = required - use_available
    productible = reactions[node]['q']
    num_reactions_needed = math.ceil(needed / productible)
    extra_produced = num_reactions_needed * productible - needed
    stocks[node] += extra_produced - use_available
    
    current_tree = tree[node]
    for child_tree in reactions[node]['l']:
        child, needed = child_tree['c'], child_tree['q']
        current_tree[child] = {}
        child_required = needed * num_reactions_needed
        cost(current_tree, child, child_required, stocks, reactions, needed_ore)
    
    return sum(needed_ore)


# 1
reactions = parse_reactions(text)
ore_per_fuel = cost({'FUEL': {}}, node='FUEL', required=1, stocks=defaultdict(int), reactions=reactions)
print(ore_per_fuel)


# 2
tree = {'FUEL': {}}
stocks = defaultdict(int)
max_ore = 10**12
needed_ore = 0
produced_fuel = 0

while True:
    remaining_ore = max_ore - needed_ore
    required_fuel = remaining_ore // ore_per_fuel
    if required_fuel == 0:
        break
    needed_ore += cost(tree, node='FUEL', required=required_fuel, stocks=stocks, reactions=reactions)
    produced_fuel += required_fuel
print(produced_fuel)
