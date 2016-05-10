# ds-rpc
Remote procedure calling system built for data science applications. CS262 Final Project.

### Overview

This application consists of a server that can run code from any Python or R library remotely for its clients. Communicating with the server requires using one of the client libraries (right now, client libraries exist for Python and JavaScript). The server has all of the needed libraries installed so the clients don't need any extra code besides the lightweight client libraries. 

The functionality of the application is probably best shown by example:

##### Calling R code using the Python client library
```python
# sample from a Dirichlet distribution with uniform alpha
ones = [1 for _ in range(3)]
n_samples = 3
result = server.r('gtools.rdirichlet', n_samples, ones)
print result  #[[[0.0606,0.1637,0.095,0.6807],[0.0625,0.6069,0.2534,0.0773],[0.2252,0.2347,0.0306,0.5095]]]
```

##### Calling Python code using JavaScript client library
```javascript
var callback = function(result){console.log(result);}
var x = get_n_random_numbers(100);
var y = get_n_random_numbers(100);
server.python(callback, 'scipy.stats.pearsonr', x, y);

// outputs [0.09398385492166901,0.3523279903811445]
// (the scipy pearsonr function returns the correlation constant and the p value)

```

### Setup


##### Server



