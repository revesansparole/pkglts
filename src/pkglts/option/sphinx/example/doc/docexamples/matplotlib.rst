
Example of 'matplotlib.sphinxext.plot_directive' usage
======================================================

.. ifconfig:: 'matplotlib.sphinxext.plot_directive' not in extensions

    You need to install `matplotlib`_ to use this extension.

see `matplotlib extensions page`_ for more documentation.

.. plot::

   import matplotlib.pyplot as plt
   import numpy as np
   x = np.random.randn(1000)
   plt.hist( x, 20)
   plt.grid()
   plt.title(r'Normal: $\mu=%.2f, \sigma=%.2f$'%(x.mean(), x.std()))
   plt.show()


.. _`matplotlib`: http://matplotlib.org
.. _`matplotlib extensions page`: http://matplotlib.org/sampledoc/extensions.html
