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
lgca --model-name=FHP_II --pattern=obstacle --steps=250 --run
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

  Lattice Gas Cellular Automata [X] HPP [X] FHP I [X] FHP II [X] FHP III

Options:
  -v, --value TEXT                Content value.  [default: 0]
  -n, --model-name [HPP|FHP_I|FHP_II|FHP_III]
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

## References

* [Hardy, J., Pomeau, Y., & Pazzis, O.D. (1973). Time evolution of a two‐dimensional model system. I. Invariant states and time correlation functions. Journal of Mathematical Physics, 14, 1746-1759.](https://sci-hub.se/10.1063/1.1666248)
* [Hardy, J., Pazzis, O.D., & Pomeau, Y. (1976). Molecular dynamics of a classical lattice gas: Transport properties and time correlation functions. Physical Review A, 13, 1949-1961.](https://sci-hub.se/10.1103/physreva.13.1949)
* [Frisch, U., Hasslacher, B., & Pomeau, Y. (1986). Lattice-gas automata for the Navier-Stokes equation. Physical review letters, 56 14, 1505-1508 .](https://sci-hub.se/10.1103/physrevlett.56.1505)
* [Frisch, U., d'Humières, D., Hasslacher, B., Lallemand, P., Pomeau, Y., & Rivet, J. (1987). Lattice Gas Hydrodynamics in Two and Three Dimensions. Complex Syst., 1.](https://content.wolfram.com/sites/13/2018/02/01-4-7.pdf)
* [Wylie, B.J. (1990). Application of two-dimensional cellular automaton lattice-gas models to the simulation of hydrodynamics.](https://pages.cs.wisc.edu/~wylie/doc/PhD_thesis.pdf)
* [Buick, J.M. (1997). Lattice Boltzmann methods in interfacial wave modelling.](https://era.ed.ac.uk/bitstream/handle/1842/10845/Buick1997.pdf)

## Status

![build status](https://github.com/siciarek/lgca/actions/workflows/python-app.yml/badge.svg?style=flat&cache-control=no-cache)
![Code Coverage](https://img.shields.io/badge/Code%20Coverage-100%25-success?style=flat)
