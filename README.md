# ds-rpc
Remote procedure calling system built for data science applications. CS262 Final Project.

### Overview

This application consists of a server that can run code from any Python or R library remotely for its clients. Communicating with the server requires using one of the client libraries (right now, client libraries exist for Python and JavaScript). The server has all of the needed libraries installed so the clients don't need any extra code besides the lightweight client libraries. 

The functionality of the application is probably best shown by example:

##### Running R code remotely using the Python client library
```python
# sample from a Dirichlet distribution with uniform alpha
ones = [1 for _ in range(3)]
n_samples = 3
result = server.r('gtools.rdirichlet', n_samples, ones)
print result  #[[[0.0606,0.1637,0.095,0.6807],[0.0625,0.6069,0.2534,0.0773],[0.2252,0.2347,0.0306,0.5095]]]
```

##### Running Python code remotely using JavaScript client library
```javascript
// calculate the correlation coefficient between two lists of random numbers
var callback = function(result){console.log(result);}
var x = get_n_random_numbers(100); //gets a list of 100 random numbers between 0 and 1
var y = get_n_random_numbers(100);
server.python(callback, 'scipy.stats.pearsonr', x, y);

// outputs [0.09398385492166901,0.3523279903811445]
// (the scipy pearsonr function returns the correlation constant and the p value)
```

### Setup

##### Server

The server requires Flask and any scientific computing libraries you want to use. If you don't already have a Python environment with the depedencies, the easiest way to get started is setting up a virtual environment:

```
virtualenv venv
source venv/bin/activate (to activate)
pip install -r requirements.txt (to install dependencies)
```


