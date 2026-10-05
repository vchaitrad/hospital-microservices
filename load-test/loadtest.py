import requests, time, csv, subprocess, threading, statistics, os
from concurrent.futures import ThreadPoolExecutor
URL = "http://localhost:5000/book/1/1"
LEVELS = [1, 2, 4, 8, 16]
TOTAL = 200
CONTAINERS = {"appointment-service": "appointment", "patient-service": "patient", "doctor-service": "doctor"}
RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "results.csv")
def parse_mem(s):
    v = s.split("/")[0].strip()
    for unit, mult in (("GiB", 1024), ("MiB", 1), ("KiB", 1/1024), ("kB", 1/1024), ("B", 1/1048576)):
        if v.endswith(unit):
            return float(v[:-len(unit)]) * mult
    return 0.0
def sampler(stop, store):
    while not stop.is_set():
        out = subprocess.run(["docker", "stats", "--no-stream", "--format", "{{.Name}},{{.CPUPerc}},{{.MemUsage}}"], capture_output=True, text=True).stdout
        for line in out.strip().splitlines():
            name, cpu, mem = line.split(",", 2)
            if name in CONTAINERS:
                store[name].append((float(cpu.strip("%")), parse_mem(mem)))
def one_request(_):
    start = time.time()
    try:
        ok = requests.get(URL, timeout=10).status_code == 200
    except Exception:
        ok = False
    return time.time() - start, ok
rows = []
for _ in range(10):
    one_request(0)
for i, conc in enumerate(LEVELS, 1):
    store = {name: [] for name in CONTAINERS}
    stop = threading.Event()
    t = threading.Thread(target=sampler, args=(stop, store))
    t.start()
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=conc) as ex:
        results = list(ex.map(one_request, range(TOTAL)))
    elapsed = time.time() - t0
    stop.set()
    t.join()
    good = [r[0] for r in results if r[1]]
    row = {"workload": f"W{i}", "concurrency": conc,
           "avg_response_ms": round(statistics.mean(good) * 1000, 2) if good else 0,
           "throughput_rps": round(TOTAL / elapsed, 2), "failed": TOTAL - len(good)}
    for name, short in CONTAINERS.items():
        s = store[name] or [(0, 0)]
        row[f"{short}_cpu_pct"] = round(statistics.mean(x[0] for x in s), 2)
        row[f"{short}_mem_mb"] = round(statistics.mean(x[1] for x in s), 2)
    rows.append(row)
    print(row)
    time.sleep(3)
with open(RES, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print("Saved", RES)
