# decorum
Stylish, useful python decorators for coding with your pinky extended

# usage
A quick example of a decorator from the `decorum.decorators` that caches computationally
intensive routine outputs

```python
from decorum.decorators import autocache
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
