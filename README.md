# WitTrane
Configures WIT & generates series of utterances to train on.

### Goals
1. ~~Use templates & create sentences by iterating through provided intents, entities & traits~~
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

### NOTE:
The [pywit](https://github.com/wit-ai/pywit) library has a bug in it. Either it should be forked & fixed or better yet a PR should be raised. In the meantime, it's been cloned, updated & installed locally to get things up & running. To so within the `create_intent` method in `wit.py` swap out the existing line for:
```python
resp = req(self.logger, self.access_token, 'POST', endpoint, params, data=json.dumps(data) , headers=headers)
```