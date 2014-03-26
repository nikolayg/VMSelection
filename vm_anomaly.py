#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

"""
A simple client to create a CLA anomaly detection model for hotgym.
The script prints out all records that have an abnoramlly high anomaly
score.
"""

import csv
import datetime
import logging

from nupic.data.datasethelpers import findDataset
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.predictionmetricsmanager import MetricsManager

import model_params
import time

_LOGGER = logging.getLogger(__name__)

_DATA_PATH = "extra/hotgym/rec-center-hourly.csv"


def createModel():
  return ModelFactory.create(model_params.MODEL_PARAMS)


def runVMAnomaly():
  model = createModel()
  model.enableInference({'predictedField': 'cpuUtil'})
  
  headers = ["timestamp", "cpuUtil", "ramUtil", "diskUtil", "numUsers"];
  records = [[0.2, 0.2, 0.2, 100], 
    [0.2,  0.2,  0.2,  100], 
    [0.3,  0.2,  0.2,  100], 
    [0.2,  0.2,  0.2,  100],
    [0.2,  0.2,  0.2,  100],
    [0.2,  0.2,  0.2,  100],
    [0.2,  0.2,  0.2,  100],
    [0.2,  0.2,  0.2,  100],
    [0.2,  0.2,  0.2,  100],
    [0.2,  0.2,  0.2,  100],
    [0.2,  0.2,  0.2,  100],
    [0.2,  0.2,  0.2,  100],
    [0.2,  0.2,  0.2,  100],
    [0.22,  0.3,  0.3,  110],
    [0.24,  0.4,  0.35, 120],
    [0.26,  0.5,  0.45, 130],
    [0.28,  0.6,  0.50, 140],
    [0.3,  0.7,  0.55, 150],
    [0.32,  0.8,  0.60, 160],
    [0.34,  0.9,  0.65, 170],
    [0.36,  0.95, 0.70, 180],
    [0.38,  0.99, 0.65, 190],
    [0.40,  0.99, 0.60, 200],
    [0.2,  0.2,  0.2,  100],
    [0.5,  0.2,  0.2,  101]]
  
  for record in records:
    modelInput = dict(zip(headers, [None] + record ))
    modelInput["timestamp"] = datetime.datetime.now()
    
    modelInput["cpuUtil"] = float(modelInput["cpuUtil"])
    modelInput["ramUtil"] = float(modelInput["ramUtil"])
    modelInput["numUsers"] = float(modelInput["numUsers"])
        
    result = model.run(modelInput)
    anomalyScore = result.inferences['anomalyScore']
    _LOGGER.info("Time [%s]. Record %s, Anomaly score: %f.",
                    result.rawInput["timestamp"], 
                    dict(zip(headers[1:], record )), 
                    anomalyScore)
    time.sleep(1)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  runVMAnomaly()
