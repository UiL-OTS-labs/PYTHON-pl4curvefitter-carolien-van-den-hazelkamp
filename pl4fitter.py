# using http://people.duke.edu/~ccc14/pcfb/analysis.html
# where x is the concentration, A is the minimum asymptote, B is the steepness, C is the inflection point and D is the maximum asymptote.

import csv, os, re, math, sys, warnings
try:
	import matplotlib.pyplot as plt
	from matplotlib.widgets import Button
except:
	print "matplotlib library is not installed. Please install this first"
try:
	import numpy as np
	import numpy.random as npr
except:
	print "Numpy library is not installed. Please install this first"
try:
	from scipy.optimize import leastsq
except:
	print "scipy library is not installed. Please install this first"

class valuesWriter():

	writer = ""

	def __init__(self):
		self.filename = raw_input("Enter the name of the output directory you wish to use. Existing files in the directory will be overwritten:\n")
		try:
			os.stat(self.filename)
		except:
			os.mkdir(self.filename)
		self.f = open(self.filename + "/" + self.filename + "_output.csv", 'w')
		self.writeHeader()

	def writeHeader(self):
		headerrow = "PPId;"
		for i in range(7):
			headerrow += ("X%d;" %(i+1))
			headerrow += ("Y%d-original;" %(i+1))
			headerrow += ("Y%d-fit;" %(i+1))
		headerrow += "A;B;C;D;GoF;Keep/Discard\n"
		self.f.write(headerrow)

	def shutdown(self):
		self.f.close()

	def writeRow(self, pp, list1, list2, list3, vals, gof, useful):
		row = "%s;" %pp
		for i in range(len(list1)):
			row += "%f;" %list1[i]
			row += "%f;" %list2[i]
			row += "%f;" %list3[i]
		
		# Handle empty Y-values
		missingItems = 7 - len(list1)
		if missingItems > 0:
			for i in range(missingItems):
				row += ";;;"

		row += "%f;%f;%f;%f;%f;%s\n" %(vals['A'], vals['B'], vals['C'], vals['D'],gof,useful)
		self.f.write(row)

	def getFilename(self):
		return self.filename

def readfile(name):
	'''
	Read the input file.
	Creates a dictionary with the participants as key
	and a list of 7 items as value
	@arg name 	The filename and relative path for the input file
	@return 	Dictionary of participants and their items
	'''
	if not name.lower().endswith('.csv'): 
		print("The file '%s' does not seem to be a .csv file. Please select a file that ends with '.csv'" %name)
		exit(1)
	elif not os.path.isfile(name):
		print("The file '%s' could not be found. Try again with another file." %name)
		exit(1)
	else:
		print "Now reading file '%s'" %name
		result = dict()
		with open(name, 'rb') as data:
			reader = csv.reader(data, delimiter=';')
			for line,row in enumerate(reader):
				if row[0] == "ppid":
					continue
				if not row[0] in result:
					result[row[0]] = list()
				try:
					x = int(row[1])
				except ValueError:
					continue
				try:
					y = row[2].replace(',', '.')
					y = float(y)
				except ValueError:
					print "Warning: missing or faulty value (\'%s\') on line: %d"%(row[2], line)
					continue
				result[row[0]].append( (x, y) )
		return result

def logistic4(x, A, B, C, D):
	"""4PL lgoistic equation."""
	result = ((A-D)/(1.0+((x/C)**B))) + D
	return result

def residuals(p, y, x):
	"""Deviations of data from fitted 4PL curve"""
	A,B,C,D = p
	with warnings.catch_warnings():
		warnings.filterwarnings('error')
		try:
			err = y-logistic4(x, 0, B, C, D)
		except RuntimeWarning:
			err = list(p)
			for i in range(len(p)):
				err[i] = 1e8
	if B<0:
		err = 1e8
	return err

def peval(x, p):
    """Evaluated value at x with current parameters."""
    A,B,C,D = p
    return logistic4(x, A, B, C, D)

def plot(data, sortKeys, index, figure):
	'''
	Plots the coordinates for a participant.
	@arg 	pp 		Participant ID
	@arg 	coords 	list of coordinates (x = time, y = accurary)
	'''
	pp = sortKeys[index]
	coords = data[pp]
	list1, list2 = [list(t) for t in zip(*coords)]

	# Convert x and y data to numpy array
	x = np.asarray(list1)
	y_meas = np.asarray(list2)

	# Initial guess for parameters
	p0 = [0, 1, 1, max(y_meas)]

	# Fit equation using least squares optimization
	plsq = leastsq(residuals, p0, args=(y_meas, x),maxfev=10000)


	x_fitted_plot = np.linspace(1e-8,max(x),200)

	# Plot results
	figure.clear()

	theplot = plt.plot(x_fitted_plot, peval(x_fitted_plot, plsq[0]),x,y_meas, 'o')

	
	plt.xlabel('Time (ms)')
	plt.ylabel('accurary')
	plt.title('Least-squares 4PL fit to %s data' %pp)
	textX = max(x)*0.7
	textY = max(y_meas)*0.4
	for i, (param, est) in enumerate(zip('ABCD',plsq[0])):
	     plt.text(textX, textY-i*0.2, '%s = %.2f' % (param, est))
	plt.savefig(writer.getFilename() + "/" + pp + '.png')
	plt.draw()

	vals = dict()
	for i, (param, est) in enumerate(zip('ABCD',plsq[0])):
	     vals[param] = est
	
	# Calculate new Y-values and Goodness of Fit (GoF)
	list3 = [logistic4(x, vals['A'],vals['B'],vals['C'],vals['D']) for x in list1]
	gof = sum([(y1 - y2)**2 for (y1, y2) in zip(list2,list3)])
	
	# Ask user how to mark these values
	saveValues(pp, list1, list2, list3, vals, gof)
	


def selectFile():
	return raw_input("Enter the name of the source csv file\n")

def saveValues(pp, list1, list2, list3, vals, gof):
	quest = "For participant %s I found these values: \nA: %.2f\tB: %.2f\tC: %.2f\tD: %.2f\n" %(pp, vals['A'], vals['B'], vals['C'], vals['D'])
	quest += "The goodness of fit is %.2f\n" %gof
	quest += 'Do you want to mark these values as useful? Press \'U\'. Otherwise, press \'n\'\nTo exit type "exit"\n'
	useful = raw_input(quest)
	u = ""
	if useful in ["u", "U", "USE", "use", "Use","y","Y","yes","YES"]:
		print "Items will be used! On to the next graph.\n\n"
		u = "keep"
	elif useful in ["n", "N", "No", "no", "NO"]:
		u = "discard"
		print "These items will not be used! On to the next graph.\n\n"
	elif useful == "exit":
		#user terminated program
		writer.shutdown()
		exit(0)
	else:
		print "Your input was not recognised."
		return saveValues(pp, list1, list2, list3, vals, gof)

	writer.writeRow(pp, list1, list2, list3, vals, gof, u)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		selectedFile = sys.argv[1]
	else:
		selectedFile = selectFile()

	data = readfile(selectedFile)
	sortKeys = sorted(data.keys())

	writer = valuesWriter()
	
	fig1 = plt.figure()
	fig1.show()
	plt.ion()

	for i in range(len(sortKeys)):
		plot(data, sortKeys, i, fig1)

	print "Done! All the entries in the file have been fitted."

	writer.shutdown()

	
