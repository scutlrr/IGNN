#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# Developed by Shangchen Zhou <shangchenzhou@gmail.com>

import matplotlib
import os
# Fix problem: no $DISPLAY environment variable
matplotlib.use('Agg')

from argparse import ArgumentParser
from pprint import pprint

from config import cfg
from core.build import bulid_net
import torch

def get_args_from_command_line():
    parser = ArgumentParser(description='Parser of Runner of Network')
    parser.add_argument('--gpu', dest='gpu_id', help='GPU device to use', default=None, type=str)
    parser.add_argument('--phase', dest='phase', help='phase of CNN', default=cfg.NETWORK.PHASE, type=str)
    parser.add_argument('--scale', dest='scale', help='factor of upsampling', default=cfg.CONST.SCALE, type=int)
    parser.add_argument('--weights', dest='weights', help='Initialize network from the weights file', default=cfg.CONST.WEIGHTS, type=str)
    parser.add_argument('--dataset', dest='dataset_path', help='Set dataset root_path', default=cfg.DIR.DATASET_ROOT, type=str)
    parser.add_argument('--demodata', dest='demodata_path', help='Set demo test images path', default=cfg.DIR.IMAGE_LR_TEST_PATH, type=str)
    parser.add_argument('--out', dest='out_path', help='Set output path', default=cfg.DIR.OUT_PATH)
    args = parser.parse_args()
    return args

def main():
    # Get args from command line
    args = get_args_from_command_line()

    if args.gpu_id is not None:
        os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_id
    if args.phase is not None:
        cfg.NETWORK.PHASE = args.phase
    if args.scale is not None:
        cfg.CONST.SCALE = args.scale
    if args.weights is not None:
        cfg.CONST.WEIGHTS = args.weights
    if args.dataset_path is not None:
        cfg.DIR.DATASET_ROOT = args.dataset_path
    if args.demodata_path is not None:
        cfg.DIR.IMAGE_LR_TEST_PATH = args.demodata_path
        cfg.DATASET.DATASET_TEST_NAME = 'Demo'
    if args.out_path is not None:
        cfg.DIR.OUT_PATH = args.out_path

    cfg.CONST.NUM_GPU = torch.cuda.device_count()

    # Print config
    print('Use config:')
    pprint(cfg)

    # Set GPU to use
    print('Using GPUs NUMBER: '+ str(cfg.CONST.NUM_GPU))

    # Setup Network & Start train/test process
    bulid_net(cfg)

if __name__ == '__main__':
    main()
