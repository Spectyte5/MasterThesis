from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

@dataclass
class graph:
    def my_figure(self):
        """ Returns a matplot figure with required size 
        @return fig (Figure)
        """
        fig, ax = plt.subplots()
        ax.plot([1, 3, 4], [3, 2, 5])
        return fig

    def draw_figure(self):
        """ Draws the wave plot on figure with desired characteristics
        @return data (string)
        """
        fig = plt.figure()
        k_values = np.linspace(0.1, 2.0, 100)  
        omega_values = 2 * np.pi * k_values  
        plt.plot(k_values,omega_values)
        plt.xlabel("Freq (Rad/s)")
        plt.ylabel("Velocity (a.u)")
        plt.title("Velocity vs Frequency of the system")
        imgdata = StringIO()
        fig.savefig(imgdata, format='svg', transparent=True)
        imgdata.seek(0)
        data = imgdata.getvalue()
        return data