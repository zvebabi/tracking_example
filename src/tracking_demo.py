from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import os.path as osp

from FairMOT.src._init_paths import add_path

# Add FairMOT lib to PYTHONPATH
this_dir = osp.dirname(__file__)
lib_path = osp.join(this_dir, './FairMOT/src')
add_path(lib_path)

# from opts import opts
from tracking_utils.utils import mkdir_if_missing
from tracking_utils.log import logger
# import datasets.dataset.jde as datasets
from wrappers.dataset import LoadVideoFixed 
from wrappers.track import eval_seq_with_trajectory
from wrappers.opts import opts_v2 as opts
logger.setLevel(logging.INFO)

def demo(opt):
    result_root = opt.output_root if opt.output_root != '' else '.'
    print("Result root is {}".format(result_root))
    mkdir_if_missing(result_root)

    logger.info('Starting tracking...')
    print(opt.img_size)
    # exit(0)
    dataloader = LoadVideoFixed(opt.input_video, opt.img_size)
    frame_rate = dataloader.frame_rate

    frame_dir = None if opt.output_format == 'text' else osp.join(result_root, 'frame')
    eval_seq_with_trajectory(opt, dataloader,
             save_dir=frame_dir, show_image=False, frame_rate=frame_rate,
             use_cuda=opt.gpus!=[-1])

    if opt.output_format == 'video':
        result_video_name = 'results_' + os.path.basename(opt.input_video)
        output_video_path = osp.join(result_root, result_video_name)
        cmd_str = 'ffmpeg -y -f image2 -i {}/%05d.jpg -b 5000k -c:v mpeg4 {}'.format(osp.join(result_root, 'frame'), output_video_path)
        os.system(cmd_str)

if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    opt = opts().init()
    demo(opt)
