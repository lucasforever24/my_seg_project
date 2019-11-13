#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Division of Medical Image Computing, German Cancer Research Center (DKFZ)
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

import os
import torch
from os.path import exists

from configs.Config_chd import get_config
from datasets.chd_dataset.preprocessing import preprocess_data
from datasets.chd_dataset.create_splits import create_splits
from experiments.FCNExperiment import FCNExperiment
from experiments.ChdExperiment import CHDExperiment
from datasets.downsanpling_data import downsampling_image

import datetime
import time


def training():


    c = get_config()

    dataset_name = 'tapvc_dataset'


    if not exists(os.path.join(os.path.join(c.data_root_dir, dataset_name), 'preprocessed')):
        print('Preprocessing data. [STARTED]')
        preprocess_data(root_dir=os.path.join(c.data_root_dir, dataset_name))
        create_splits(output_dir=c.split_dir, image_dir=c.data_dir)
        print('Preprocessing data. [DONE]')
    else:
        print('The data has already been preprocessed. It will not be preprocessed again. Delete the folder to enforce it.')

    create_splits(excel_path=os.path.join(c.split_dir, 'pvo_1.xlsx'), output_dir=c.split_dir, image_dir=c.data_dir)

    exp = FCNExperiment(config=c, name='tapvc_experiment', n_epochs=c.n_epochs,
                        seed=42, append_rnd_to_name=c.append_rnd_string)   # visdomlogger_kwargs={"auto_start": c.start_visdom}

    exp.run()
    exp.run_test(setup=False)

def testing():

    c = get_config()

    c.do_load_checkpoint = True
    #c.checkpoint_dir = c.base_dir + '/20190424-020641_unet_experiment' + '/checkpoint/checkpoint_current' # dice_cost train
    # c.checkpoint_dir = c.base_dir + '/20190424-234657_unet_experiment' + '/checkpoint/checkpoint_last' # SDG
    c.checkpoint_dir = c.base_dir + '/20191108-115239_chd_experiment' + '/checkpoint/checkpoint_current'



    exp = FCNExperiment(config=c, name='tapvc', n_epochs=c.n_epochs,
                               seed=42, globs=globals())
    exp.run_test(setup=True)



if __name__ == "__main__":
    training()