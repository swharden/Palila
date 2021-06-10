# Code Syntax Highlighting

## C#
```cs
// Load pixel values from a 16-bit TIF using LibTiff
using Tiff image = Tiff.Open("16bit.tif", "r");

// get information from the header
int width = image.GetField(TiffTag.IMAGEWIDTH)[0].ToInt();
int height = image.GetField(TiffTag.IMAGELENGTH)[0].ToInt();
int bytesPerPixel = image.GetField(TiffTag.BITSPERSAMPLE)[0].ToInt() / 8;

// read the image data bytes
int numberOfStrips = image.NumberOfStrips();
byte[] bytes = new byte[numberOfStrips * image.StripSize()];
for (int i = 0; i < numberOfStrips; ++i)
    image.ReadRawStrip(i, bytes, i * image.StripSize(), image.StripSize());

// convert the data bytes to a double array
if (bytesPerPixel != 2)
    throw new NotImplementedException("this is only for 16-bit TIFs");
double[] data = new double[bytes.Length / bytesPerPixel];
for (int i = 0; i < data.Length; i++)
{
    if (image.IsBigEndian())
        data[i] = bytes[i * 2 + 1] + (bytes[i * 2] << 8);
    else
        data[i] = bytes[i * 2] + (bytes[i * 2 + 1] << 8);
}
```

## Python
```python
def _demo_sweep_data(sweeps=3, sweepLengthSec=5, sampleRate=20000):
    """crete a 2D numpy array of data to test ABF creation."""
    sweepData = np.empty((sweeps, sweepLengthSec*sampleRate))
    for i in range(sweeps):
        log.info("Generating sweep %d of %d ..."%(i+1, sweeps))
        sweep = generate.SynthSweep()
        sweep.addOffset(-123)
        sweep.addWobble(2)
        sweep.addNoise(3)
        sweep.addGlutamate(frequencyHz=10, maxMagnitude=20)  # glutamate
        sweep.addGABA(frequencyHz=20, maxMagnitude=5)  # GABA
        sweepData[i] = sweep.sweepY
    return sweepData
```

## PHP

```php
function __construct($path)
{
    if (file_exists($path) == false)
        throw new Exception("file not found: $path");
    $this->path = realpath($path);
    $this->abfID = pathinfo($path)['filename'];

    $this->Open();

    $firstFourBytes = $this->ReadString(4, 0);
    if ($firstFourBytes == "ABF ")
        $this->ReadHeaderABF1();
    else if ($firstFourBytes == "ABF2")
        $this->ReadHeaderABF2();
    else
        throw new Exception("file is not ABF format");

    $this->Close();
}
```