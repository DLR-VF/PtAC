
PtAC User Guide
----------------

Here you can find information about how to install and use PtAC.

Getting Started
------------
In order to run the library on a windows computer you have to have a recent Python version installed
(we recommend using Python `Anaconda <https://www.anaconda.com/products/individual>`_ or `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_, which is a lightweight version of the conda environment).

**1. open the Anaconda prompt (can be found on windows start menu) and navigate to your home folder**

.. code-block:: bash

   cd C:\Users\ptac_user

**2. generate a project folder and navigate to this folder**

.. code-block:: bash

   mkdir ptac
   cd ptac

**3. now, we can create a python virtual environment via conda and activate the created environment**

.. code-block:: bash

   conda create -n ptac python=3.8
   conda activate ptac

(ptac) should now be displayed in brackets at the starting of the line.

**4. in the next step, install necessary dependency libraries**

.. code-block:: bash

   conda install osmnx, rasterio

**5. you are able to install ptac now by typing**

.. code-block:: bash

   pip install -i https://test.pypi.org/simple/ ptac



In order to try out the `examples <https://github.com/DLR-VF/PtAC-examples>`_,
jupyter notebook needs to be installed with the following command:

.. code-block:: bash
   pip install notebook

For further details see `python packaging instructions
<https://packaging.python.org/tutorials/installing-packages/>`_.

Usage
-----
To get started with PtAC, read the user reference and see sample code and input data in
`examples repository <https://github.com/DLR-VF/PtAC-examples>`_.

Features
--------
PtAC is built on top of osmnx, geopandas, networkx and
uses `UrMoAC <https://github.com/DLR-VF/UrMoAC>`_ for accessibility computation.

* Download and prepare road networks from OpenStreetMap for accessibility calculation
* Calculate accessibilities from origins to the next destination
* Generate a population point dataset from population raster dataset
* Calculate Sustainable Development Goal 11.2.1 based on starting points with population information

Support
--------

If you have a usage question please contact us via email (simon.nieland@dlr.de,
serra.yosmaoglu@dlr.de).



