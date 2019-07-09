# defunct
Exploring the functional paradigm in Python. Implementing dope decorators and funky functions.

# usage
A quick example of a decorator from the `corator.decorators` module that caches 
outputs of computationally intensive procedures

```python
from defunct.decorators import autocache
import random 
import pickle

@autocache(loader=pickle.load, dumper=pickle.dump, read_as='b', write_as='b')
def bajillion_randoms(num_rands=10000):
    """
    seeds for downstream stochastic computation
    """
    return [random.random() for _ in range(num_rands)]    

mybajillion = bajillion_randoms(cache_to='random_outputs.bin')
```
