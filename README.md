#PL4fitter
Provides a least-square curve fitting implementation coded in python for a sigmoidal curve that fits the 4PL logistic equation:

 `((A-D)/(1.0+((x/C)**B))) + D`

*A is the minimum asymptote, B is the steepness, C is the inflection point and D is the maximum asymptote.*

In this implementation A is pushed towards zero and B is pushed to be postive (i.e. residual is set to 1e8).

# Dependencies
The script relies on python and several libraries. Likely libraries and the depencies you'll need to install are matplotlib, numpy and scipy. The best suggestion is to download a total package. I suggest Canopy (Express free)
 `https://store.enthought.com/`.

# Usage
 `python pl4fitter.py arg1`
Where arg1 is an optional CSV filename (See *exampledata.csv* for the format of the input document)

# Authors
Internals are inspired by 
 `http://people.duke.edu/~ccc14/pcfb/analysis.html`

Coded by **Jan de Mooij** and fine-tuned by **Chris van Run**
