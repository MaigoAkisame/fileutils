import numpy
import struct
from fileutils import smart_open

def readAudioSet(filename):
    """
    Reads audio and labels from a Google Audio Set file.
    Returns two variables:
      * wav -- a 2-D numpy float32 array, where each row is a waveform
        (10 seconds @ 16 kHz, mono);
      * labels -- a 2-D numpy int32 array of zeros and ones, where each row
        indicates the sound events active in the corresponding waveform.
    """
    with smart_open(filename, "rb") as f:
        nClips, nSamples, nLabels = struct.unpack("<3i", f.read(12))
        nBytes = (nLabels - 1) / 8 + 1
        data = struct.unpack("<%dh" % (nClips * nSamples), f.read(nClips * nSamples * 2))
        wav = numpy.array(data, dtype = "float32").reshape(nClips, nSamples) / 32768
        data = struct.unpack("<%dB" % (nClips * nBytes), f.read(nClips * nBytes))
        bytes = numpy.array(data).reshape(nClips, nBytes)
        labels = numpy.zeros((nClips, nLabels), dtype = "int32")
        for i in xrange(nLabels):
            labels[:,i] = (bytes[:, i / 8] >> (i % 8)) & 1
        return wav, labels

def writeAudioSet(filename, wav, labels):
    """
    Writes audio and labels to a Google Audio Set file.
    Takes two variables as input:
      * wav -- a 2-D numpy array, where each row is a waveform
        (10 seconds @ 16 kHz, mono, dtype is arbitrary);
      * labels -- a 2-D numpy array of zeros and ones, where each row
        indicates the sound events active in the corresponding waveform.
    The number of rows in the two variables must match.
    The data will be written in a compact form. The waveforms will be written
      in 16-bit integers. The labels will be written in bit arrays.
    """
    if len(wav) != len(labels):
        raise ValueError("The number of rows in 'wav' and 'labels' must match.")
    nClips, nSamples = wav.shape
    if numpy.abs(wav).max() <= 1: wav *= 32768
    wav = numpy.maximum(numpy.minimum(wav, 32767), -32768).astype("int16")
    nLabels = labels.shape[1]
    labels = labels.astype("uint8")
    nBytes = (nLabels - 1) / 8 + 1
    bytes = numpy.zeros((nClips, nBytes), dtype = "uint8")
    for i in xrange(nLabels):
        bytes[:, i / 8] += labels[:,i] << (i % 8)
    with smart_open(filename, "wb") as f:
        f.write(struct.pack("<3i", nClips, nSamples, nLabels))
        f.write(struct.pack("<%dh" % wav.size, *wav.ravel()))
        f.write(struct.pack("<%dB" % bytes.size, *bytes.ravel()))
