# ds-rpc
Remote procedure calling system built for data science applications. CS262 Final Project by Andrew Mauboussin (amaub217@gmail.com).

### Overview

This application consists of a server that can run code from any Python or R library remotely for its clients. Communicating with the server requires using one of the client libraries (right now, client libraries exist for Python and JavaScript). Clients can send requests with a function name from any Python or R library and a series of arguments. The server will run the computation and return the results. The client libraries abstract out serialization and network communication and provide a simple interface. 

The functionality of the application is probably best shown by example:

##### Running R code remotely using the Python client library
```python
from ds_rpc import Server
server = Server() # url set settings.json
# sample from a Dirichlet distribution with uniform alpha
ones = [1 for _ in range(3)]
n_samples = 3
result = server.r('gtools.rdirichlet', n_samples, ones)
print result  #[[[0.0606,0.1637,0.095,0.6807],[0.0625,0.6069,0.2534,0.0773],[0.2252,0.2347,0.0306,0.5095]]]
```

##### Running Python code remotely using JavaScript client library
```javascript
// calculate the correlation coefficient between two lists of random numbers
var server = new Server(server_url);
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

Remotely executing R code will require R [https://www.r-project.org/](https://www.r-project.org/)

After the server is running, you can test if it working by going to [http://127.0.0.1:5000/demo](http://127.0.0.1:5000/demo) in a browser. This will  send requests to the server via the JavaScript client library and display the results. 

After the dependencies are installed the server can be run with `python app.py`.

##### Client

The Python client library depends on the Requests package (`pip install requests`) and the JavaScript client library depends on jQuery.
The client libraries each expose a Server class (imported from ds_rpc.py or ds_rpc.js) that can be used to run code remotely. Both server exposes two functions, Server.python and Server.r. In Python, the server functions run synchronously and take a string denoting the name of the function to be run followed by the arguments to the function. In JavaScript, the server functions run asynchronously and take a callback function, a string denoting the name of the function to be run, and finally any arguments required by the given function (see examples above). 




