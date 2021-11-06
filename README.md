# Biblical Learning Data Science Toolkit (biblearn)
Biblical Learning tools and data

## Introduction

## Overview

## Data Sources
* https://github.com/rcdilorenzo/ecce - Original Inspiration for Project
* https://github.com/robertrouse/STEPBible-Data - STEP Biblical data


## Usage

## Build & Upload
For full instructions see: [Build PyPI projects](https://packaging.python.org/tutorials/packaging-projects/)
make sure you have cloned the repo and `cd` to the root directory (same location as `setup.cfg`).
Then Run:
```bash
python -m build
```
this will create a `dist/` folder containing the build artifacts.  These are the artifacts that will be
uploaded to the PyPI registry.  Make sure you have access token then do:
```bash
python -m twine upload --repository testpypi dist/*
```

### Streamlit Apps
#### Data Exploration App
https://share.streamlit.io/hensh2ss/biblearn/src/data_view_app.py

## Additional Information

biblearn: Biblical Learning Data Science Toolkit

Copyright (C) 2021 Seth S. Henshaw

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

<br>
<br>
