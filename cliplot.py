"""
Draws 2D functions and draws extrapolations of those
with max third degree polynomials.
Usage example:

draw:
python cliplot.py -x 1,2,3 -y 3,6,9 -v "time"

extrapolate to 5 and draw:
python cliplot.py -x 0,1,2,3 -y 0,1,4,9 -v "time" -e 5
"""

from plumbum import cli
import matplotlib.pyplot as plt
import numpy as np


MAX_DEGREE = 3


class Cliplot(cli.Application):

    @cli.switch(['-x', '--val_x'], str)
    def x_val_switch(self, val_x):
        """Specify xes to plot"""
        self._x = [float(i) for i in val_x.split(",")]

    @cli.switch(['-y', '--val_y'], str)
    def y_switch(self, val_y):
        """Specify ys to plot"""
        self._y = [float(i) for i in val_y.split(",")]

    @cli.switch(['-v', '--label_y'], str)
    def ly_switch(self, label_y):
        """Specify y label"""
        self._ly = label_y

    @cli.switch(['-h', '--label_x'], str)
    def lx_switch(self, label_x):
        """Specify x label"""
        self._lx = label_x

    @cli.switch(['-d', '--degree'], str)
    def degree_switch(self, degree):
        """Specify degrees to extrapolate"""
        self._d = [int(i) for i in degree.split(",") if int(i) <= MAX_DEGREE]

    @cli.switch(['-e', '--extrapolate'], str)
    def extrapolate_switch(self, extrapolate):
        self._extrapolate = float(extrapolate)

    @property
    def label_x(self):
        if hasattr(self, '_lx'):
            return self._lx
        return 'x'

    @property
    def label_y(self):
        if hasattr(self, '_ly'):
            return self._ly
        return 'y'

    @property
    def val_y(self):
        if hasattr(self, '_y'):
            return self._y
        return None

    @property
    def val_x(self):
        if hasattr(self, '_x'):
            return self._x
        return None

    @property
    def extrapolate(self):
        if hasattr(self, '_extrapolate'):
            return self._extrapolate
        return None

    @property
    def degree(self):
        if hasattr(self, '_d'):
            return self._d
        return [2]

    def _plot_2d(self):
        min_x = min(self.val_x)
        max_x = max(self.val_x)
        min_y = min(self.val_y)
        max_y = max(self.val_y)

        if self.extrapolate:
            max_x = max(max_x, self.extrapolate)
            times = 20 * max(1, int(self.extrapolate - self.val_x[-1]))
            colours = dict(zip(range(1, MAX_DEGREE + 1), ['g+', 'b+', 'r+']))

            plt.plot(self.val_x, self.val_y, 'ro')

            for deg in self.degree:
                z = np.polyfit(self.val_x, self.val_y, deg)
                f = np.poly1d(z)

                for x in np.linspace(self.val_x[0], self.extrapolate, times):
                    min_y = min(min_y, f(x))
                    max_y = max(max_y, f(x))
                    plt.plot(x, f(x), colours[deg])

        else:
            plt.plot(self.val_x, self.val_y)
        plt.ylabel(self.label_y)
        plt.xlabel(self.label_x)
        plt.axis([min_x, max_x, min_y, max_y])
        plt.show()

    def main(self):
        self._plot_2d()


def main():
    Cliplot.run()


if __name__ == '__main__':
    main()
