import subprocess
import os


PATH_TO_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
FLAMEGRAPH_PL = os.path.join(PATH_TO_THIS_DIR, 'flamegraph.pl')


def stats_to_svg(stats):
    proc = subprocess.Popen(
        args=[FLAMEGRAPH_PL],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    out, _ = proc.communicate(stats)
    return out
