# storyscript
An OMG server exposing the Storyscript compiler

Usage
-----

```coffee
# Storyscript
storyscript compile files: {'my.story': 'x = 2'}
storyscript lex files: {'my.story': '2 + 2'}
storyscript parse files: {'my.story': '4 - 2'}
```
