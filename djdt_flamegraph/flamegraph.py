import subprocess
import os


PATH_TO_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
FLAMEGRAPH_PL = os.path.join(PATH_TO_THIS_DIR, 'flamegraph.pl')


def stats_to_svg(stats):
    proc = subprocess.Popen(
        args=[FLAMEGRAPH_PL, '--title', ' '],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True)
    out, _ = proc.communicate(stats)
    return out
