"""
test__offline

"""
from __future__ import absolute_import

from nose.tools import raises
from unittest import TestCase

import plotly

# TODO: matplotlib-build-wip
from plotly.tools import _matplotlylib_imported
if _matplotlylib_imported:
    import matplotlib

    # Force matplotlib to not use any Xwindows backend.
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

# Generate matplotlib plot for tests
fig = plt.figure()

x = [10, 20, 30]
y = [100, 200, 300]
plt.plot(x, y, "o")

PLOTLYJS = plotly.offline.offline.get_plotlyjs()


class PlotlyOfflineTestCase(TestCase):
    def setUp(self):
        plotly.offline.offline.__PLOTLY_OFFLINE_INITIALIZED = False

    @raises(plotly.exceptions.PlotlyError)
    def test_iplot_doesnt_work_before_you_call_init_notebook_mode(self):
        plotly.offline.iplot([{}])

    def test_iplot_works_after_you_call_init_notebook_mode(self):
        plotly.tools._ipython_imported = True
        plotly.offline.init_notebook_mode()
        plotly.offline.iplot([{}])

    def test_iplot_mpl_works_after_you_call_init_notebook_mode(self):
        plotly.tools._ipython_imported = True
        plotly.offline.init_notebook_mode()
        plotly.offline.iplot_mpl(fig)


class PlotlyOfflineMPLTestCase(TestCase):
    def setUp(self):
        pass

    def _read_html(self, file_url):
        """ Read and return the HTML contents from a file_url in the
        form e.g. file:///Users/chriddyp/Repos/plotly.py/plotly-temp.html
        """
        with open(file_url.replace('file://', '').replace(' ', '')) as f:
            return f.read()

    def test_default_mpl_plot_generates_expected_html(self):
        data_json = ('[{"name": "_line0", "yaxis": "y1", "marker": {"color":' +
                     ' "#0000FF", "opacity": 1, "line": {"color": "#000000",' +
                     ' "width": 0.5}, "symbol": "dot", "size": 6.0}, "mode":' +
                     ' "markers", "xaxis": "x1", "y": [100.0, 200.0, 300.0],' +
                     ' "x": [10.0, 20.0, 30.0], "type": "scatter"}]')
        layout_json = ('{"autosize": false, "width": 640, "showlegend": ' +
                       'false, "xaxis1": {"tickfont": {"size": 12.0}, ' +
                       '"domain": [0.0, 1.0], "ticks": "inside", "showgrid":' +
                       ' false, "range": [10.0, 30.0], "mirror": "ticks", ' +
                       '"zeroline": false, "showline": true, "nticks": 5, ' +
                       '"type": "linear", "anchor": "y1", "side": "bottom"},' +
                       ' "height": 480, "yaxis1": {"tickfont": ' +
                       '{"size": 12.0}, "domain": [0.0, 1.0], "ticks": ' +
                       '"inside", "showgrid": false, "range": [100.0, 300.0]' +
                       ', "mirror": "ticks", "zeroline": false, "showline": ' +
                       'true, "nticks": 5, "type": "linear", "anchor": "x1",' +
                       ' "side": "left"}, "hovermode": "closest", "margin":' +
                       ' {"b": 47, "r": 63, "pad": 0, "t": 47, "l": 80}}')
        html = self._read_html(plotly.offline.plot_mpl(fig))

        # just make sure a few of the parts are in here
        # like PlotlyOfflineTestCase(TestCase) in test_core
        self.assertTrue('Plotly.newPlot' in html) # plot command is in there
        self.assertTrue(data_json in html)        # data is in there
        self.assertTrue(layout_json in html)        # layout is in there too
        self.assertTrue(PLOTLYJS in html)         # and the source code
        # and it's an <html> doc
        self.assertTrue(html.startswith('<html>') and html.endswith('</html>'))

    def test_including_plotlyjs(self):
        html = self._read_html(plotly.offline.plot_mpl(fig, include_plotlyjs=False))
        self.assertTrue(PLOTLYJS not in html)

    def test_div_output(self):
        html = plotly.offline.plot_mpl(fig, output_type='div')

        self.assertTrue('<html>' not in html and '</html>' not in html)
        self.assertTrue(html.startswith('<div>') and html.endswith('</div>'))

