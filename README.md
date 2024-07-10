# GVaspWeb Manual

![GitHub](https://img.shields.io/github/license/Rasic2/GVaspWeb)

## Table of contents

- [About GVaspWeb](#about-gvasp)
- [Install](#install)
    - [Install GVasp](#install-gvasp)
    - [Install Vue](#install-vue)
- [Code Structure](#code-structure)
- [Requirements](#requirements)

## About GVaspWeb

The Web version of [GVasp](https://github.com/Rasic2/gvasp) created by Vue and Flask, which can involve in many kinds of
tasks as below:

- plot optimization process
- plot electrostatic potential
- plot band structure
- plot density of states
- plot energy barrier

More detailed information about GVasp can see [here](https://qvasp.readthedocs.io/en/latest/).

## Install

### Create Environment

Before install the `GVaspWeb`, we strongly recommend you to
install [conda](https://www.anaconda.com/products/distribution)
before.

After install conda, create a new environment, e.g. `gvasp-web`, and install a `python (version=3.9)`, using following
command:

```
conda create -n gvasp-web python=3.9
```

### Install GVasp

1. Use conda (recommend)

   We now made a conda package (production process can
   see [here](https://codenote.readthedocs.io/en/latest/package.html#conda-package)) and uploaded to
   the [Anaconda](https://anaconda.org/hui_zhou/gvasp), so you can also install `GVasp` from it:

   ```
   conda install -c hui_zhou -c conda-forge gvasp
   ```

2. Use PyPi

   We have made the wheel (production process can
   see [here](https://codenote.readthedocs.io/en/latest/package.html#pypi-wheel)) and upload to
   the [pypi](https://pypi.org/project/gvasp/),
   you can also install from it:

   ```
   python -m pip install gvasp
   ```

   If the download speed is too slow, we suggest you change the pip mirror by modifying the `~/.pip/pip.conf` file.

If you run the `gvasp -v` and print version information, then you install the `GVasp` successful ~~

```
GVasp version x.x.x (Linux-5.10.16.3-microsoft-standard-WSL2-x86_64-with-glibc2.35)
```

### Install Vue

1. Install nvm (node)

NVM is the most popular NodeJs Management tool, we recommend you to install nodejs with nvm.

Firstly, download the nvm and install it.

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
```

Secondly, install node16 with nvm.

```bash
nvm install 16.20.1
```

Finally, use node16 with nvm.

```bash
nvm use 16.20.1
```

2. Install Vue

```bash
npm install -g @vue/cli

```

3. Install modules

```bash
cd frontend
npm install .
```

## Code Structure

- [backend](backend): backend code in Flask

- [frontend](frontend): frontend code in Vue

## Requirements

- Python >= 3.9
- Cython
- pybind11
- numpy
- matplotlib
- bash-completion
- Vue.js
- Flask

Copyright © 2024 `Hui Zhou` All rights reserved.
