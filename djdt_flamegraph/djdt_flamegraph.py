import collections
import signal
import time
import math

from django.template import Template, Context

from . import flamegraph

try:
    from debug_toolbar.panels import Panel
except ImportError as e:
    import os
    if os.environ.get('TESTING'):
        import mock
        Panel = mock.Mock()
    else:
        raise e

template = r"""
<style>
    #FlamegraphPanel .djDebugPanelContent { padding:0; }
</style>
<template id="djdt-flamegraph-tpl">
    <style>
        body {margin: 0;}
    </style>
    {{ flamegraph|safe }}
    <script>
        init();
    </script>
    <div style="padding: 1ex">
      Total time: {{ stats.total_time|floatformat:"0" }} ms <br>
      Sampling overhead: {{ stats.sampling_cost|floatformat:"0" }} ms
        ({{ stats.sampling_cost_per_sample|floatformat }} &micro;s per sample) <br>
      Samples: {{ stats.samples }} (expected: {{ stats.expected_samples|floatformat:"0" }}) <br>
      Interval: {{ stats.min_interval|floatformat:"-3" }}..{{ stats.max_interval|floatformat:"-3" }} ms
                (average {{ stats.avg_interval|floatformat:"-3" }} ms, stddev {{ stats.stddev|floatformat:"-3" }} ms) <br>
      Outliers:
      {% for outlier in stats.outliers %}
        {{ outlier|floatformat:"-3"}}&#x200a;ms
      {% endfor %}
      {% for outlier in stats.serious_outliers %}
        <b title="sample {{ outlier.pos }} of {{ stats.samples }}">{{ outlier.value|floatformat:"-3"}}&#x200a;ms</b>
      {% endfor %}
    </div>
</template>
<iframe id="djdt-flamegraph-iframe" style="width:100%;height:100%;" src="about:blank">
</iframe>
<script>
    (function(){
        var i = document.querySelector('#djdt-flamegraph-iframe');
        var tpl = document.querySelector('#djdt-flamegraph-tpl');
        i.contentWindow.document.write(tpl.innerHTML);
    }())
</script>
"""


class FlamegraphPanel(Panel):
    title = 'Flamegraph'
    template = 'djdt_flamegraph.html'

    @property
    def enabled(self):
        key = 'djdt' + self.panel_id
        return self.toolbar.request.COOKIES.get(key, 'off') == 'on'

    @property
    def content(self):
        ctx = {
            'flamegraph': flamegraph.stats_to_svg(self.sampler.get_stats()),
            'stats': self.sampler.get_sampling_stats(),
        }
        return Template(template).render(Context(ctx))

    def enable_instrumentation(self):
        self.sampler = Sampler()

    def process_request(self, request):
        self.sampler.start()

    def process_response(self, request, response):
        self.sampler.stop()


class Sampler(object):
    def __init__(self, interval=0.001):
        self.stack_counts = collections.defaultdict(int)
        self.interval = interval
        self.sampling_cost = 0
        self.total_time = 0
        self.intervals = []
        self._start = self._last = 0

    def _sample(self, signum, frame):
        now = time.time()
        stack = []
        while frame is not None:
            formatted_frame = '{}({})'.format(frame.f_code.co_name,
                                              frame.f_globals.get('__name__'))
            stack.append(formatted_frame)
            frame = frame.f_back

        formatted_stack = ';'.join(reversed(stack))
        self.stack_counts[formatted_stack] += 1
        self.intervals.append(now - self._last)
        self._last = now
        self.sampling_cost += time.time() - now

    def get_stats(self):
        return '\n'.join('%s %d' % (key, value) for key, value in sorted(self.stack_counts.items()))

    def get_sampling_stats(self):
        intervals, outliers = split_outliers(self.intervals)
        serious_threshold = self.interval * 10
        serious_outliers = [
            {'value': o * 1000,
             'pos': self.intervals.index(o)}
            for o in outliers if o >= serious_threshold
        ]
        outliers = [o for o in outliers if o < serious_threshold]
        return {
            'sampling_cost': self.sampling_cost * 1000,
            'sampling_cost_per_sample': 'n/a' if not self.intervals else 1e6 * self.sampling_cost / len(self.intervals),
            'interval': self.interval * 1000,
            'min_interval': min(intervals) * 1000,
            'max_interval': max(intervals) * 1000,
            'avg_interval': avg(intervals) * 1000,
            'stddev': stddev(intervals) * 1000,
            'outliers': [o * 1000 for o in outliers],
            'serious_outliers': serious_outliers,
            'total_time': self.total_time * 1000,
            'samples': len(self.intervals),
            'expected_samples': self.total_time / self.interval,
        }

    def start(self):
        self._start = self._last = time.time()
        signal.signal(signal.SIGALRM, self._sample)
        signal.setitimer(signal.ITIMER_REAL, self.interval, self.interval)

    def stop(self):
        signal.setitimer(signal.ITIMER_REAL, 0, 0)
        self.total_time = time.time() - self._start


def avg(numbers):
    return sum(numbers) / len(numbers) if numbers else 'n/a'


def stddev(numbers):
    if len(numbers) < 2:
        return 'n/a'
    c = avg(numbers)
    ss = sum((x - c) ** 2 for x in numbers)
    # XXX: divide by len(numbers) - 1 maybe?  lol I don't know stats
    return math.sqrt(ss / len(numbers))


def split_outliers(numbers):
    numbers = sorted(numbers)
    outliers = []
    if len(numbers) < 10:
        return numbers, outliers
    q1 = numbers[len(numbers) // 4]
    q3 = numbers[len(numbers) * 3 // 4]
    iqr = q3 - q1
    f = 15  # usually 1.5 but I want fewer outliers -- only those that are seriously out there
    min_x = q1 - f * iqr
    max_x = q3 + f * iqr
    outliers = [x for x in numbers if x < min_x or x > max_x]
    numbers = [x for x in numbers if min_x <= x <= max_x]
    return numbers, outliers
