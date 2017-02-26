#!/bin/bash

docker run --rm -it -v `pwd`:/source -w /source continuumio/anaconda python main.py
