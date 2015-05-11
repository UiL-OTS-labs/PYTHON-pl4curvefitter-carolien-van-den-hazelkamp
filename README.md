#PL4fitter
Provides a curve fitting implementation coded in python for a sigmoidal curve that fits the 4PL logistic equation:

 `((A-D)/(1.0+((x/C)**B))) + D`

# Dependencies
The script relies on python and several libraries. Likely libraries and the depencies you'll need to install are matplotlib, numpy and scipy. The best suggestion is to download a total package. I suggest Canopy (Express free)
 `https://store.enthought.com/`.

# Usage
 `python pl4fitter.py arg1`
Where arg1 is an optional CSV filename (e.g. *exampledata.csv*)

# Authors
Internals are inspired by 
 `http://people.duke.edu/~ccc14/pcfb/analysis.html`

Coded by **Jan de Mooij** and fine-tuned by **Chris van Run**
