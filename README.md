# Work Tool

### Useful Commands
Run in bash directly. Creates a text file with 1000 random numbers.
```
for i in $(seq 1 1000); do echo "$RANDOM" >> random.txt; done
```

Pip command to add package to system. requrires setup.py.
```
pip3 install -v -e .
```