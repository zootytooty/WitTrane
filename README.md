# WitTrane
Configures WIT & generates series of utterances to train on.

### Goals
1. Use templates & create sentences by iterating through provided intents, entities & traits
2. Make templates smarter by automatically creating permutations that look like typos. These should apply to:
    - The fixed template strings
    - The template variables populated by entities & traits
3. Turn in to a general package anyone could use


## Usage

1. Install required libraries:
```sh
pip install -r requirements.txt
```

2. Set WIT Environment Variable
```sh
export WIT_TOKEN=abc123
```

3. Train WIT
```sh
python train_wit.py
```