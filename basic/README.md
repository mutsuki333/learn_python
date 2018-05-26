# Notes

## **File reading** \: [ref](https://stackoverflow.com/questions/15599639/what-is-the-perfect-counterpart-in-python-for-while-not-eof)
Loop over the file to read lines:
```python
with open('somefile') as openfileobject:
    for line in openfileobject:
        do_something()
```

## Packages
`pip list` to list installed packages
