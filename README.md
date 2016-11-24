# fileutils

This repository contains Python helper functions to read/write feature and label files for machine learning.

Supported file types include HTK feature files, Janus feature files, Kaldi archive and script files, pfiles, and TextGrid annotation files.

Below is a brief documentation of the functions:

## In `__init__.py`:

* `file = smart_open(filename, mode, ...)`

  Works just like the built-in `open` function, but can deal with `.gz` and `.bz2` compressed files transparently.

## In `htk.py`:

* `x = readHtk(filename)`

  Reads the feature matrix stored in a HTK feature file, and returns it as a 2-D numpy array.

* `writeHtk(filename, feature, sampPeriod, parmKind)`:

  Writes a 2-D numpy array to a HTK feature file. `sampPeriod` and `parmKind` are required fields of HTK feature files.

## In `janus.py`:

* `x = readFmatrix(filename)`

  Reads the feature matrix stored in a Janus feature file, and returns it as a 2-D numpy array.

* `writeFmatrix(filename, feature)`

  Writes a 2-D numpy array to a Janus feature file.

## In `kaldi.py`:

* `features, uttids = readArk(filename, limit = numpy.inf)`

  Reads at most `limit` feature matrices in a Kaldi `ark` file.  
  Returns the feature matrices in a list of 2-D numpy arrays, and their utterance ids in a list of strings.
  
* `features, uttids = readScp(filename, limit = numpy.inf)`

  Reads at most `limit` feature matrices in a Kaldi `scp` file (which contains pointers into `ark` files).  
  Returns the feature matrices in a list of 2-D numpy arrays, and their utterance ids in a list of strings.

* `writeArk(filename, features, uttids)`

  Takes a list of 2-D numpy arrays and a list of utterance ids, and writes them into a Kaldi `ark` file.  
  Returns a list of strings in the format "filename:offset", which can be used to write a Kaldi script file.

* `writeScp(filename, uttids, pointers)`

  Takes a list of utterance ids and a list of pointer strings in the format "filename:offset", and writes them to a Kaldi `scp` file.

## In `pfile.py`:

* `features, labels = readPfile(filename)`

  Reads the feature matrices (and labels) stored in a pfile.  
  Returns both the features and labels as a list of 2-D numpy arrays (although in most cases the label matrices will have a width of 1).  
  In the case where the pfile doesn't contain labels, `labels` will be `None`.

* `writePfile(filename, features, labels = None)`

  Writes feature matrices (and labels) to a pfile.  
  Both the features and labels should be presented as lists of 2-D numpy arrays.  
  In the case where there is only one label per frame, the label arrays can be 1-D.  

## In `TextGrid.py`:

* `annot = TextGrid.fromFile(filename)`

  Reads the annotations in a TextGrid file, and returns it as an annotation object.  
  An annotation object consists of tiers, which in turn consists of intervals, which have starting times, ending times, and labels.
