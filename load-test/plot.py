import csv, os
import matplotlib.pyplot as plt
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
rows = list(csv.DictReader(open(os.path.join(R, "results.csv"))))
x = [int(r["concurrency"]) for r in rows]
def col(k):
    return [float(r[k]) for r in rows]
def graph(title, ylabel, series, fname):
    plt.figure()
    for label, k in series:
        plt.plot(x, col(k), marker="o", label=label)
    plt.xlabel("Concurrent Requests")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(x)
    plt.grid(True)
    if len(series) > 1:
        plt.legend()
    plt.savefig(os.path.join(R, fname), dpi=150)
    plt.close()
svc = ["appointment", "patient", "doctor"]
graph("Concurrent Requests vs Avg Response Time", "ms", [("Response time", "avg_response_ms")], "response_time.png")
graph("Concurrent Requests vs Throughput", "requests/sec", [("Throughput", "throughput_rps")], "throughput.png")
graph("Concurrent Requests vs CPU Utilization", "CPU %", [(s, f"{s}_cpu_pct") for s in svc], "cpu.png")
graph("Concurrent Requests vs Memory Utilization", "MB", [(s, f"{s}_mem_mb") for s in svc], "memory.png")
print("Graphs saved")
