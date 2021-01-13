import json
from typing import Tuple, Callable, T

import bson
import numpy as np
from tifffile import imread


class BsonContainer:
    version = 2
    numSets = 0
    indexImg = ""
    labelMapping = {}
    labelSets = {}
    segmentationSource = {}

    def __init__(self):
        self.version = 1
        self.numSets = 0
        self.indexImg = ""
        self.labelMapping = {}
        self.labelSets = {}

    @classmethod
    def fromValues(cls, version: int = 1, numsets: int = 0, indeximg: str = "", labelmapping: dict = {},
                   label_sets: dict = {}, segmentation_source: dict = {}):
        obj = BsonContainer()
        obj.numSets = numsets
        obj.indexImg = indeximg
        obj.labelMapping = labelmapping
        obj.labelSets = label_sets
        obj.version = version
        obj.segmentationSource = segmentation_source
        return obj

    @classmethod
    def fromDict(cls, data: dict):
        obj = BsonContainer()
        obj.version = data["version"]
        obj.numSets = data["numSets"]
        obj.indexImg = data["indexImg"]
        obj.labelMapping = data["labelMapping"]
        obj.labelSets = data["labelSets"]
        obj.segmentationSource = data["segmentationSource"]
        return obj

    def encode(self):
        return bson.encode(vars(self))

    def encode_and_save(self, path: str):
        data = bson.encode(vars(self))
        with open(path, 'wb+') as f:
            f.write(data)

    def encodewithfunc(self, path: str, func: Callable[[T], int]):
        for labelset in self.labelSets.values():
            i = 0
            for label in labelset:
                t = func(label)
                labelset[i] = t
                i += 1

        data = bson.encode(vars(self))
        with open(path, 'wb+') as f:
            f.write(data)

    def save_as_json(self, path: str):
        with open(path, 'w') as outfile:
            json.dump(vars(self), outfile)

    @staticmethod
    def decode(path: str):
        with open(path, 'rb') as f:
            data = bson.decode(f.read())
            return BsonContainer.fromValues(data["version"], data["numSets"], data["indexImg"], data["labelMapping"],
                                            data["labelSets"], data["segmentation_source"])

    @staticmethod
    def decode_withfunc(path, func: Callable[[int], T]):
        with open(path, 'rb') as f:
            data = bson.decode(f.read())
            transformed_labelsets = {}
            for key, labelset in data['labelSets'].items():
                transformed_labelsets[key] = set()
                for label in labelset:
                    transformed_labelsets[key].add(func(label))

            return BsonContainer.fromValues(data["version"], data["numSets"], data["indexImg"], data["labelMapping"],
                                            transformed_labelsets, data["segmentation_source"])

    def get_image(self):
        return imread(self.indexImg)