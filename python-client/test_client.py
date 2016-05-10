from ds_rpc import Server
from random import random, randrange

server = Server()


def string_method_test():
    print server.python('string.upper', 'abc')


def correlation_test():
    # generate data
    x = [random() for _ in range(100)]
    y = [random() for _ in range(100)]

    # test the correlation
    result = server.python('scipy.stats.pearsonr', x, y)

    print result


def _make_identity_matrix(n, value=1):
    """Create an nxn identity matrix for testing"""
    one_at_pos = lambda pos: [value if i == pos else 0 for i in range(n)]
    return [one_at_pos(j) for j in range(n)]


def matrix_test():

    m = _make_identity_matrix(5)

    result = server.python('scipy.linalg.inv', m)
    print result


def sampling_test():

    ones = [1 for _ in range(3)]
    n_samples = 5
    result = server.python('numpy.random.dirichlet', ones, n_samples)
    print result


def r_sampling_test():

    ones = [1 for _ in range(3)]
    n_samples = 5
    result = server.r('gtools.rdirichlet', n_samples, ones)

    print result


def r_correlation_test():
    # generate data
    x = [random() for _ in range(100)]
    y = [random() for _ in range(100)]

    # test the correlation
    result = server.r('solve', _make_identity_matrix(3, 4))

    print result

r_sampling_test()
