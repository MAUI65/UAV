# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/api/30_camera.gst_cam.ipynb.

# %% auto 0
__all__ = []

# %% ../../nbs/api/30_camera.gst_cam.ipynb 6
import time, os, sys

from UAV.logging import logging
from UAV.mavlink.mavcom import MAVCom, time_since_boot_ms, time_UTC_usec, date_time_str
from UAV.mavlink.component import Component, mavutil, mavlink, MAVLink

import cv2

from UAV.utils.general import boot_time_str, With, find_config_dir, read_camera_dict_from_toml
from UAV.camera.gst_cam import *