import numpy as np
import pickle
from openGLviz.net_visualizer import Visualizer
from vispy import gloo, app
import vispy
from threading import Thread
import time
import qtpy.QtWidgets
from matplotlib.colors import hex2color

def hexes2colors(h):
    colors = [list(hex2color(c)) for c in h]
    colors = np.float32(colors)
    colors = np.concatenate([colors, np.ones([len(h), 1], dtype=np.float32)], axis=1)
    return colors


edge_colors = hexes2colors(['#000000', '#3f34a0', '#334f9a', '#337294', '#338e8c'])
# node_colors = hexes2colors(['#3d3cb5', '#2e7c89', '#349d55', '#a9ad3a', '#b8663d', '#b33c4c', '#933165'])
#node_colors = hexes2colors(['#005cff', '#389d34', '#be4f3f', '#ffdc28', '#00af67', '#ba3ea0', '#00a4ff'])
node_colors = hexes2colors(['#005cff', '#ffdc28', '#005cff', '#ffdc28', '#005cff', '#ffdc28', '#005cff', '#ffdc28'])

node_positions = np.load('/Users/vincentherrmann/Documents/Projekte/Immersions/models/e32-2019-08-13_2/e32_positions_interp_240.npy').astype(np.float32)

# node_weights = np.load(
#     '/Users/vincentherrmann/Documents/Projekte/Immersions/visualization/layouts/e25_version_3/e25_positions_interp_100_weights.npy')
# node_weights = node_weights.astype(np.float32)
# node_weights = np.sqrt(node_weights)

focus = np.zeros(node_positions.shape[1])
focus[10000:10100] += 1.
focus = focus > 0.

edges_textures = np.load(
        '/Users/vincentherrmann/Documents/Projekte/Immersions/models/e32-2019-08-13_2/e32_positions_interp_240_edges_weighted.npy') * 1.
edges_textures = edges_textures.astype(np.float32)
edges_textures[edges_textures != edges_textures] = 0.
edges_textures /= edges_textures.max()
edges_textures = np.power(edges_textures, 0.3) * 1.

c = Visualizer(node_positions=node_positions,
               #edge_textures=np.zeros((240, 600, 600), dtype=np.float32),
               edge_textures=edges_textures,
               node_weights=None,
               focus=focus)

c.edges_colors = edge_colors
c.node_colors = node_colors
c.scale_factor = 6.

def change_focus():
    while True:
        time.sleep(4.)
        c.transition_frames = 240
        focus = np.random.rand(node_positions.shape[1])
        focus = focus > 1.
        focus[np.random.randint(0, node_positions.shape[1])] = True
        #focus[np.random.randint(0, node_positions.shape[1])] = True
        c.focus = focus

focus_change_thread = Thread(target=change_focus)
focus_change_thread.daemon = True
focus_change_thread.start()

window = qtpy.QtWidgets.QMainWindow()
window.setCentralWidget(c.native)
window.show()
app.Timer(1 / 60., connect=c.update, start=True)
app.run()
