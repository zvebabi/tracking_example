from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths
import os
import os.path as osp
import cv2
import logging
import argparse
import motmetrics as mm
import numpy as np
import torch
from collections import defaultdict

from tracker.multitracker import JDETracker
from tracking_utils import visualization as vis
import wrappers.visualisation as vis2

from tracking_utils.log import logger
from tracking_utils.timer import Timer

from tracking_utils.utils import mkdir_if_missing

def eval_seq_with_trajectory(opt, dataloader, save_dir=None, show_image=True, frame_rate=30, use_cuda=True):
    if save_dir:
        mkdir_if_missing(save_dir)
    tracker = JDETracker(opt, frame_rate=frame_rate)
    timer = Timer()
    frame_id = 0
    trajectories = defaultdict(list)
    topview_canvas = cv2.imread(opt.topview_path)
    #for path, img, img0 in dataloader:
    for i, (path, img, img0) in enumerate(dataloader):
        #if i % 8 != 0:
            #continue
        if frame_id % 20 == 0:
            logger.info('Processing frame {} ({:.2f} fps)'.format(frame_id, 1. / max(1e-5, timer.average_time)))

        # run tracking
        timer.tic()
        if use_cuda:
            blob = torch.from_numpy(img).cuda().unsqueeze(0)
        else:
            blob = torch.from_numpy(img).unsqueeze(0)
        online_targets = tracker.update(blob, img0)
        online_tlwhs = []
        online_ids = []
        #online_scores = []
        for t in online_targets:
            tlwh = t.tlwh
            tid = t.track_id
            vertical = tlwh[2] / tlwh[3] > 1.6
            if tlwh[2] * tlwh[3] > opt.min_box_area and not vertical:
                online_tlwhs.append(tlwh)
                online_ids.append(tid)
                trajectories[tid].append(tlwh)
                #online_scores.append(t.score)
        timer.toc()
        
        if show_image or save_dir is not None:
            online_im = vis.plot_tracking(img0, online_tlwhs, online_ids, frame_id=frame_id,
                                          fps=1. / timer.average_time)
            online_im, num_poses = vis2.plot_trajectory(online_im, trajectories, online_ids, opt.track_history)
            #test homography
            if topview_canvas is not None:
                topview = vis2.plot_homography(topview_canvas, trajectories, online_ids, num_poses, i)
                online_im = np.vstack((online_im, topview))
        if show_image:
            cv2.imshow('online_im', online_im)
        if save_dir is not None:
            cv2.imwrite(os.path.join(save_dir, '{:05d}.jpg'.format(frame_id)), online_im)
        frame_id += 1
    return frame_id, timer.average_time, timer.calls
