"""
The codes are from Chen Yunpeng: https://github.com/cypw/PyTorch-MFNet
Modified by Yuan Li to video hashing
"""
import os
import json
import logging
import argparse
import socket

import torch.nn.parallel
import torch.distributed as dist

import dataset
from train_model import train_model
from network.symbol_builder import get_symbol

parser = argparse.ArgumentParser(description="PyTorch Video Hashing")
parser.add_argument('--debug-mode', type=bool, default=True,
                    help="print all setting for debugging.")
parser.add_argument('--hash_bit',type=int,  default=64,
                    help="define the length of hash bits.")
parser.add_argument('--dataset', default='SVW', choices=['UCF101', 'HMDB51', 'Kinetics', 'MSR_VTT', 'SVW'],
                    help="path to dataset")
parser.add_argument('--clip-length', default=16,
                    help="define the length of each input sample.")
parser.add_argument('--train-frame-interval', type=int, default=2,
                    help="define the sampling interval between frames.")
parser.add_argument('--val-frame-interval', type=int, default=2,
                    help="define the sampling interval between frames.")
parser.add_argument('--task-name', type=str, default='',
                    help="name of current task, leave it empty for using folder name")
parser.add_argument('--model-dir', type=str, default="./exps/models",
                    help="set logging file.")
parser.add_argument('--log-file', type=str, default="",
                    help="set logging file.")
parser.add_argument('--gpus', type=str, default="0,1,2,3,4,5,6,7",
                    help="define gpu id")
parser.add_argument('--network', type=str, default='MFNet_3D',
                    choices=['MFNet_3D'],
                    help="chose the base network")
parser.add_argument('--pretrained_2d', type=bool, default=True,
                    help="load default 2D pretrained model.")
parser.add_argument('--resume-epoch', type=int, default=-1,
                    help="resume train")
parser.add_argument('--fine-tune', type=bool, default=True,
                    help="apply different learning rate for different layers")
parser.add_argument('--batch-size', type=int, default=64,
                    help="batch size")
parser.add_argument('--lr-base', type=float, default=0.005,
                    help="learning rate")
parser.add_argument('--lr-steps', type=list, default=[int(1e5*x) for x in [2, 4, 6, 7]],
                    help="number of samples to pass before changing learning rate") # 1e6 million
parser.add_argument('--lr-factor', type=float, default=0.1,
                    help="reduce the learning with factor")
parser.add_argument('--save-frequency', type=float, default=1,
                    help="save once after N epochs")
parser.add_argument('--end-epoch', type=int, default=100,
                    help="maxmium number of training epoch")
parser.add_argument('--random-seed', type=int, default=1,
                    help='random seed (default: 1)')
parser.add_argument('--backend', default='nccl', type=str, choices=['gloo', 'nccl'],
                    help='Name of the backend to use')
parser.add_argument('--world-size', default=1, type=int,
                    help='number of distributed processes')
parser.add_argument('--dist-url', default='tcp://192.168.0.11:23456', type=str,
                    help='url used to set up distributed training')

def autofill(args):
    # customized
    if not args.task_name:
        args.task_name = os.path.basename(os.getcwd())
    if not args.log_file:
        if os.path.exists("./exps/logs"):
            args.log_file = "./exps/logs/{}_at-{}.log".format(args.task_name, socket.gethostname())
        else:
            args.log_file = ".{}_at-{}.log".format(args.task_name, socket.gethostname())

    args.model_prefix = os.path.join(args.model_dir, args.task_name)
    return args

def set_logger(log_file='', debug_mode=False):
    if log_file:
        if not os.path.exists("./"+os.path.dirname(log_file)):
            os.makedirs("./"+os.path.dirname(log_file))
        handlers = [logging.FileHandler(log_file), logging.StreamHandler()]
    else:
        handlers = [logging.StreamHandler()]

    """ add '%(filename)s:%(lineno)d %(levelname)s:' to format show source file """
    logging.basicConfig(level=logging.DEBUG if debug_mode else logging.INFO,
                format='%(asctime)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                handlers = handlers)

if __name__ == "__main__":

    # set args
    args = parser.parse_args()
    args = autofill(args)

    set_logger(log_file=args.log_file, debug_mode=args.debug_mode)
    logging.info("Using pytorch {} ({})".format(torch.__version__, torch.__path__))
    logging.info("Start training with args:\n" +
                 json.dumps(vars(args), indent=4, sort_keys=True))

    # set device states
    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpus # before using torch
    assert torch.cuda.is_available(), "CUDA is not available"
    torch.manual_seed(args.random_seed)
    torch.cuda.manual_seed(args.random_seed)

    # distributed training
    args.distributed = args.world_size > 1
    if args.distributed:
        import re, socket
        rank = int(re.search('192.168.0.(.*)', socket.gethostname()).group(1))
        logging.info("Distributed Training (rank = {}), world_size = {}, backend = `{}'".format(
                     rank, args.world_size, args.backend))
        dist.init_process_group(backend=args.backend, init_method=args.dist_url, rank=rank,
                                group_name=args.task_name, world_size=args.world_size)

    # load dataset related configuration
    dataset_cfg = dataset.get_config(name=args.dataset)

    # creat model with all parameters initialized
    net, input_conf = get_symbol(name=args.network,
                     pretrained=args.pretrained_2d if args.resume_epoch < 0 else None,
                     print_net=True if args.distributed else False,
                     hash_bit = args.hash_bit,
                     **dataset_cfg)

    # training
    kwargs = {}
    kwargs.update(dataset_cfg)
    kwargs.update({'input_conf': input_conf})
    kwargs.update(vars(args))
    print(f'-----------------------dataset/SVW/raw/{args.hash_bit}_svw_30_class.pkl-----------------')
    Hash_center = torch.load(f'dataset/SVW/raw/{args.hash_bit}_svw_30_class.pkl')
    train_model(Hash_center, sym_net=net, **kwargs)

