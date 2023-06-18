### Labelprinterkit

Labelprinterkit is a Python3 library for creating and printing labels with
Brother P-Touch devices. It was developed for the Networking department of
KIT (Karlsruhe Institute of Technology).

Labelprinterkit's simple layout engine can be used to create simple labels:

```python
from labelprinterkit.backends.usb import PyUSBBackend
from labelprinterkit.printers import P750W
from labelprinterkit.label import Label, Text
from labelprinterkit.job import Job
from labelprinterkit.constants import MediaType, MediaSize

# Define the layout of our label
# We define a single row with two text items.
# In real usage, you will probably want to change the font of the text.
class MyLabel(Label):
    items = [
        [Text(pad_right=50), Text()]
    ]

# Instantiate the label with specific data
label = MyLabel("text1", "text2")
page = labe.page()
job = Job(MediaSize.W12, MediaType.LAMINATED_TAPE)
job.add_page(page)
# scan for a USB printer using the PyUSBBackend
backend = PyUSBBackend()
printer = P700(backend)
# Print!
printer.print(job)
```

Example of using a better font:

```python
from PIL import Image, ImageFont
SIZE = 60
font = ImageFont.truetype("FreeSans.ttf", SIZE)
# Use it in the label template, e.g.
Text(font, pad_right=50)
```

To use a Bluetooth connection:
1. pair your device
2. specify the serial device node when instantiating the printer:

```python
printer = GenericPrinter(BTSerialBackend(dev_path='/dev/ttyS8'))
```

The following printers are currently supported:

 * Brother P-Touch PT-700 (aka P700)
 * Brother P-Touch PT-750W (aka P750W)
 * Brother H500
 * Brother E500

The following printers have been tested to mostly work, although not
officially supported (their protocol is similar, although not identical):

* Brother P-touch CUBE Plus PTP710BT

The following backends are currently supported:

 * USB Printer Device Class via PyUSB
 * Bluetooth Serial connection via PySerial
 * Network connection via TCP

The official source of this repository is at https://git.scc.kit.edu/scc-net/labelprinterkit.
Pull requests and issues are also accepted on github at https://github.com/notafile/labelprinterkit.
