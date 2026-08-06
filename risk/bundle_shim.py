# risk/bundle_shim.py
from dataclasses import dataclass

@dataclass
class DeployedBundle:
    model: object
    scaler: object
    feature_list: list
    class_mapping: dict
