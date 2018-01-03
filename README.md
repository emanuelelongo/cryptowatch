# CryptoWatch

## How to use
``` sh
git clone https://github.com/emanuelelongo/cryptowatch.git
cd cryptowatch
vim settings.py
# edit settings...
python main.py
```

## Never push settings.py

``` sh
git update-index --assume-unchanged settings.py
```

## If you really want to push changes to settings.py

``` sh
git update-index --no-assume-unchanged
```
