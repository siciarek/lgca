# Lattice Gas Cellular Automata

This project focuses on the declarative implementation of the popular *Lattice Gas Cellular Automata* listed below.
Models with checked names are implemented and ready to use.

* [X] HPP
* [X] FHP I
* [X] FHP II
* [X] FHP III

Currently, all the models are fully implemented, so feel free to test them.

## Application GUI

*Application window when the following commands were called:*

```bash
lgca --model-name=HPP --pattern=wiki --steps=640 --run
```

![HPP, obstacle, step 250 <](https://github.com/siciarek/lgca/raw/main/docs/images/hpp-obstacle-step-640.png?raw=True)

```bash
lgca --model-name=FHPII --pattern=obstacle --steps=250 --run
```

![FHP II, obstacle, step 250 <](https://github.com/siciarek/lgca/raw/main/docs/images/fhp-ii-obstacle-step-250.png?raw=True)

## Installation

Install using `pip` (creating a Python virtual environment first is strongly recommended).

```bash
pip install lgca
```

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

## Status

![build status](https://github.com/siciarek/lgca/actions/workflows/python-app.yml/badge.svg)
