# defunct
Exploring the functional paradigm in Python. Implementing dope decorators and funky functions.
`defunct` includes three(-ish) submodules: `de`, `funct`, and `utils`. 

Find decorators in `de` and functions in `funct`. Yes, most decorators are functions.
Functions here mean "functions not specifically purposed as decorators".


# usage
A quick example of a decorator from the `defunct.decorators` module that caches 
outputs of computationally intensive procedures

```python
from defunct.de import autocache
import random 
import pickle


@autocache(loader=pickle.load, dumper=pickle.dump)
def bajillion_randoms(num_rands=10000):
    """
    seeds for downstream stochastic computation
    """
    return [random.random() for _ in range(num_rands)]    

mybajillion = bajillion_randoms(cache_to='random_outputs.bin')
```

Obligatory `deprecated` decorator

```python
from defunct.decorators import deprecated
@deprecated('use the new version')
def old_add(a, b):
    return sum([1 for _ in range(a)] + [1 for _ in range(b)])

>>> old_add(100, 200)
>>> DeprecationWarning: Call to deprecated function :: [old_add] (use the new version)

```

Or who hasn't wanted to save a marginal amount of characters to perform a composition?
```python
from defunct.funcs import compose

composed_function = compose(lambda x: x * 10, int, chr)

composed_function(97.5)
    'Ϗ' # chr(int(97.5 * 10)))!!
```


