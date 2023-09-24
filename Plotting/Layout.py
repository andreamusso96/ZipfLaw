import plotly.express as px
from plotly.validators.scatter.marker import SymbolValidator


class PlotLayout:
    def __init__(self):
        self.color_map = px.colors.qualitative.Light24
        self.grey = px.colors.qualitative.Dark2[-2]
        self.n_colors = len(self.color_map)
        self.symbols = PlotLayout._get_selected_symbols()
        self.n_symbols = len(self.symbols)

    def system_to_symbol(self, system: int):
        if system >= len(self.symbols):
            print('Warning: More communities than symbols available')
            symbol = self.symbols[-1]
        else:
            symbol = self.symbols[system % self.n_symbols]
        return symbol

    def system_to_color(self, system: int, shift: int = 0):
        color = self.color_map[(shift + system) % self.n_colors]
        return color

    @staticmethod
    def _get_selected_symbols():
        raw_symbols = SymbolValidator().values
        symbols = [raw_symbols[i + 2] for i in range(0, len(raw_symbols), 3)]
        symbols = [s for s in symbols if not ('open' in s or 'dot' in s)]
        return symbols


class MapPlotLayout(PlotLayout):
    def __init__(self):
        super().__init__()
        self.marker_size_min = 4
        self.marker_size_max = 10
        self.marker_size_exponent = 0.7
        self.width_map_plot = 1500
        self.height_map_plot = 600


class ZipfPlotLayout(PlotLayout):
    def __init__(self):
        super().__init__()
        self.node_size_highlighted_system_zipf_plot = 10
        self.opacity_nodes_zipf_plot_with_highlighted_system = 0.2
        self.opacity_nodes_zipf_plot_without_highlighted_system = 1
        self.width_zipf_plot = 1200
        self.height_zipf_plot = 600