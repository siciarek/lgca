# Lattice Gas Cellular Automata

This project contains `Python` implementation of the popular *Lattice Gas Cellular Automata*, listed below.

* [X] HPP
* [X] FHP I
* [X] FHP II
* [ ] FHP III

> [!WARNING]
> Work in progress...

## Installation

Clone or download current project

```bash
git clone https://github.com/siciarek/lgca.git
```

go to the main project directory

```bash
cd lgca
```

and install it locally (using a Python virtual environment is strongly recommended).

```bash
python -m venv .venv
. .venv/bin/activate
pip install '.[dev]'
```

> [!NOTE]
> The project will be available via `PyPI` after full implementation of `FHP III`,
> at the moment is available only as described above.

## Usage

To get some information about the application just run:

```bash
lgca --help
```

and You should see something like below.

```text
pygame 2.5.2 (SDL 2.28.3, Python 3.12.7)
Hello from the pygame community. https://www.pygame.org/contribute.html
Usage: lgca [OPTIONS]

  Lattice Gas Cellular Automata [X] HPP [X] FHP I [X] FHP II [ ] FHP III

Options:
  -v, --value INTEGER RANGE       Content value.  [default: 0; 0<=x<=255]
  -n, --model-name [HPP|FHPI|FHPII|FHPIII|hpp|fhpi|fhpii|fhpiii]
                                  Model name.  [default: HPP]
  -w, --width INTEGER             Lattice window width.  [default: 300]
  -h, --height INTEGER            Lattice window height.  [default: 200]
  -s, --steps INTEGER             Number of steps.  [default: -1]
  -r, --run                       Run immediately.
  -d, --deterministic             Generate the same randomized result for the
                                  same params.  [default: True]
  -p, --pattern [wiki|random|alt|single|obstacle|test]
                                  Select initial state pattern.  [default:
                                  wiki]
  --help                          Show this message and exit.
```

So the sample usage can look like this

```bash
lgca --run
```

The above command should display the *HPP model* visualization, identical to the one on Wikipedia.

<https://en.wikipedia.org/wiki/HPP_model>

* To start/stop the application just press the *space button*.
* To reset app to the initial state press the *S button*.
* To quit the app pres *ESC button* or quit the window.
