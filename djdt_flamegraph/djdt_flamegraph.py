import collections
import signal

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
</template>

<iframe id="djdt-flamegraph-iframe" style="width:100%;height:100%;">
</iframe>
"""

from django.templatetags.static import static

class FlamegraphPanel(Panel):
    title = 'Flamegraph'
    template = 'djdt_flamegraph.html'

    @property
    def enabled(self):
        key = 'djdt' + self.panel_id
        return self.toolbar.request.COOKIES.get(key, 'off') == 'on'

    @property
    def content(self):
        return Template(template).render(Context({
            'flamegraph': flamegraph.stats_to_svg(self.sampler.get_stats())
        }))

    @property
    def scripts(self):
        scripts = super().scripts
        scripts.append(static("djdt_flamegraph/djdt_flamegraph.js"))
        return scripts

    def enable_instrumentation(self):
        self.sampler = Sampler()

    def process_request(self, request):
        self.sampler.start()
        response =  super().process_request(request)
        self.sampler.stop()
        return response


class Sampler(object):
    def __init__(self, interval=0.001):
        self.stack_counts = collections.defaultdict(int)
        self.interval = interval

    def _sample(self, signum, frame):
        stack = []
        while frame is not None:
            formatted_frame = '{}({})'.format(frame.f_code.co_name,
                                              frame.f_globals.get('__name__'))
            stack.append(formatted_frame)
            frame = frame.f_back

        formatted_stack = ';'.join(reversed(stack))
        self.stack_counts[formatted_stack] += 1

    def get_stats(self):
        return '\n'.join('%s %d' % (key, value) for key, value in sorted(self.stack_counts.items()))

    def start(self):
        signal.signal(signal.SIGALRM, self._sample)
        signal.setitimer(signal.ITIMER_REAL, self.interval, self.interval)

    def stop(self):
        signal.setitimer(signal.ITIMER_REAL, 0, 0)
