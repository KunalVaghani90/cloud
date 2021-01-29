# Copyright 2020 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TensorFlow utilities."""

import json
import os
from typing import Text
import tensorflow  as tf
from tensorboard.backend.event_processing import directory_watcher
from tensorboard.backend.event_processing import event_file_loader
from tensorboard.backend.event_processing import io_wrapper


def get_version():
    return tf.__version__


def get_tensorboard_log_watcher_from_path(
        path: Text):
    """Create an event generator for file or directory at given path string.

    This method creates an event generator using tensorboard directory_watcher.
    The generator.load() method will return event logs as they become available.
    The generator does not repeat events.

    Args:
        path: Text representing a directory, file, or Google Cloud Storage
        (GCS) for tensorboard logs.
    Returns:
        A tensorboard directory_watcher event generator.
    Raises:
        ValueError: if path is not defined.
    """
    if not path:
        raise ValueError("path must be a valid string")
    if io_wrapper.IsSummaryEventsFile(path):
        return event_file_loader.EventFileLoader(path)
    return directory_watcher.DirectoryWatcher(
        path,
        event_file_loader.EventFileLoader,
        io_wrapper.IsSummaryEventsFile,
    )


def is_mwms(strategy):
    """Checks if strategy is a subclass of MultiWorkerMirroredStrategy.

    Args:
        strategy: object to be classified, can be None.
    Returns:
        True if strategy is an instance or a subclass of
        Tensorflow.distribute.MultiWorkerMirroredStrategy and False otherwise.
    """
    if strategy is not None and issubclass(
        tf.distribute.experimental.MultiWorkerMirroredStrategy,
        strategy.__class__):
        return True
    return False


def is_chief():
    """Checks if the current worker is Chief.

    Returns:
      True if the current worker is chief.

    Raises:
      ValueError if TF_CONFIG env variable is not defined.
    """
    if "TF_CONFIG" not in os.environ:
        raise ValueError("TF_CONFIG is not defined.")

    config_task = json.loads(os.environ["TF_CONFIG"])["task"]
    return config_task.get("type", "") == "chief"
