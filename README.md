# OszConverter
<hr>
A python multithreaded osz converter

## Build

### Pyinstaller

```shell
pyinstaller --onefile --icon="icon.ico" --name=osz-converter main.py
```

## Misc

### Performance comparison:<br/>
500 maps without multithread: **188.57 seconds.**<br/>
500 maps with multithread(8threads): **80.88 seconds.**<br/>


3609 maps without multithread: **1787.79 seconds.**<br/>
3609 maps with multithread(8threads): **629.77 seconds.**<br/>
