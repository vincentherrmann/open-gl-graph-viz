import numpy as np
import qtpy
from openGLviz.net_visualizer import Visualizer
from vispy import gloo, app
from threading import Thread
import time
import random

positions = np.random.rand(1, 100, 2).astype(np.float32)
viz = Visualizer(node_positions=positions, animate=False)
viz.animate = False
viz.node_alpha_factor = 1.
viz.min_node_radius = 0.005

window = qtpy.QtWidgets.QMainWindow()
window.setCentralWidget(viz.native)


def update_plot():
    while True:

        num_nodes = random.randint(10, 100)
        print("num nodes:", num_nodes)
        viz.set_new_node_positions(np.random.rand(1, num_nodes, 2).astype(np.float32))
        viz.update()
        time.sleep(0.2)


update_thread = Thread(target=update_plot, daemon=True)
update_thread.start()

window.show()
app.run()