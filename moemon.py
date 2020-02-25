from seed import method1_mons, seed_at

start_cycle = 1552  # RNG cycle to start at
start_value = seed_at(start_cycle)
otId = 0xDD2E8EA2

def shiny(pid, otId):
    tid = otId >> 16
    sid = otId & 0xffff
    p1 = pid >> 16
    p2 = pid & 0xffff
    s = tid ^ sid ^ p1 ^ p2
    return s < 8

for i, pid, _ in method1_mons(start_value, limit=7200):
    if shiny(pid, otId):
        print(f'{i+start_cycle-2} {pid:08X} {shiny(pid, otId)}')
