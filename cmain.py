# coding=utf-8
from optparse import OptionParser

import numpy as np
import pandas as pd
import tensorflow as tf

from data_prepare.cikm16data_read import load_data2
from data_prepare.load_dict import load_random
from data_prepare.rsyc15data_read import load_data
from data_prepare.rsyc15data_read_p import load_data_p
from util.Config import read_conf
from util.FileDumpLoad import dump_file, load_file
from util.Randomer import Randomer

# from data_prepare.load_dict import load_one_hot
# the data path.

root_path = '~'
project_name = '/projects/STAMP'

# the pretreatment data path.

rsc15_train = root_path + project_name + '/datas/data/rsc15_train_full.txt'
rsc15_test = root_path + project_name + '/datas/data/rsc15_test.txt'
mid_rsc15_train_data = "rsc15_train.data"
mid_rsc15_test_data = "rsc15_test.data"
mid_rsc15_emb_dict = "rsc15_emb_dict.data"
mid_rsc15_4_emb_dict = "rsc15_4_emb_dict.data"
mid_rsc15_64_emb_dict = "rsc15_64_emb_dict.data"

cikm16_train = root_path + project_name + '/datas/cikm16/cmki16_train_full.txt'
cikm16_test = root_path + project_name + '/datas/cikm16/cmki16_test.txt'
mid_cikm16_emb_dict = "cikm16_emb_dict.data"


def load_tt_datas(config={}, reload=True):
    '''
    loda data.
    config:
    nload:
    '''
    print(reload)
    print("HOLAAA")
    if reload:
        print("reload the datasets.")
        print(config['dataset'])
        if config['dataset'] == 'rsc15':
            train_data, test_data, item2idx = load_data(
                rsc15_train,
                rsc15_test,
                class_num=config['class_num']
            )
            data = pd.read_csv(rsc15_train, sep='\t', dtype={'ItemId': np.int64})
            itemids = data["ItemId"].unique()
            n_items = len(itemids)
            config["n_items"] = n_items
            emb_dict = load_random(item2idx, edim=config['hidden_size'], init_std=config['emb_stddev'])
            config['pre_embedding'] = emb_dict
            path = 'datas/mid_data'
            dump_file([emb_dict, path + mid_rsc15_emb_dict])
            print("-----")

        if config['dataset'] == 'rsc15_4':
            train_data, test_data, item2idx, n_items = load_data_p(
                rsc15_train,
                rsc15_test,
                pro=4
            )

            config["n_items"] = n_items - 1
            emb_dict = load_random(item2idx, edim=config['hidden_size'], init_std=config['emb_stddev'])
            config['pre_embedding'] = emb_dict
            path = 'datas/mid_data'
            dump_file([emb_dict, path + mid_rsc15_4_emb_dict])
            print("-----")

        if config['dataset'] == 'rsc15_64':
            train_data, test_data, item2idx, n_items = load_data_p(
                rsc15_train,
                rsc15_test,
                pro=64
            )

            config["n_items"] = n_items - 1
            emb_dict = load_random(item2idx, edim=config['hidden_size'], init_std=config['emb_stddev'])
            config['pre_embedding'] = emb_dict
            path = 'datas/mid_data'
            dump_file([emb_dict, path + mid_rsc15_64_emb_dict])
            print("-----")

        if config['dataset'] == 'cikm16':
            train_data, test_data, item2idx, n_items = load_data2(
                cikm16_train,
                cikm16_test,
                class_num=config['class_num']
            )
            config["n_items"] = n_items - 1
            emb_dict = load_random(item2idx, edim=config['hidden_size'], init_std=config['emb_stddev'])
            config['pre_embedding'] = emb_dict
            path = 'datas/mid_data'
            dump_file([emb_dict, path + mid_cikm16_emb_dict])
            print("-----")

    else:
        print("not reload the datasets.")
        print(config['dataset'])
        if config['dataset'] == 'rsc15':
            train_data, test_data, item2idx = load_data(
                rsc15_train,
                rsc15_test,
                class_num=config['class_num']
            )
            data = pd.read_csv(rsc15_train, sep='\t', dtype={'ItemId': np.int64})
            itemids = data["ItemId"].unique()  # 去重，return 唯一的itemid序列
            n_items = len(itemids)
            config["n_items"] = n_items

            path = 'datas/mid_data'
            emb_dict = load_file(path + mid_rsc15_emb_dict)
            config['pre_embedding'] = emb_dict[0]

            print("-----")

        if config['dataset'] == 'rsc15_4':
            train_data, test_data, item2idx, n_items = load_data_p(
                rsc15_train,
                rsc15_test,
                pro=4
            )

            config["n_items"] = n_items - 1
            path = 'datas/mid_data'
            emb_dict = load_file(path + mid_rsc15_4_emb_dict)
            config['pre_embedding'] = emb_dict[0]
            # path = 'datas/mid_data'
            # dump_file([emb_dict, path+mid_rsc15_emb_dict])
            print("-----")

        if config['dataset'] == 'rsc15_64':
            train_data, test_data, item2idx, n_items = load_data_p(
                rsc15_train,
                rsc15_test,
                pro=64
            )

            config["n_items"] = n_items - 1
            # emb_dict = load_random(n_items, edim=config['hidden_size'], init_std=config['emb_stddev'])
            # path = 'datas/train_emb/'
            # emb_dict = load_file(path + "rsc15_64_emb.data")
            path = 'datas/mid_data'
            emb_dict = load_file(path + mid_rsc15_64_emb_dict)
            config['pre_embedding'] = emb_dict[0]

            # dump_file([emb_dict, path + mid_rsc15_emb_dict])
            print("-----")

        if config['dataset'] == 'cikm16':
            train_data, test_data, item2idx, n_items = load_data2(
                cikm16_train,
                cikm16_test,
                class_num=config['class_num']
            )
            config["n_items"] = n_items - 1
            path = 'datas/mid_data'
            emb_dict = load_file(path + mid_cikm16_emb_dict)
            # path = 'datas/train_emb/'
            # emb_dict = load_file(path + "cikm16_emb.data")
            config['pre_embedding'] = emb_dict[0]
            print("-----")
            # if config['dataset'] == 'rsc15':
            #     train_data = pd.read_csv(rsc15_train, sep='\t', dtype={'ItemId': np.int64})
            #     test_data = pd.read_csv(rsc15_test, sep='\t', dtype={'ItemId': np.int64})


            # path = 'datas/mid_data/'
            # sample_list = []
            # for i in range(10):
            #     tmp = load_file(
            #         path +str(i)+ "_"+mid_rsc15_train_data
            #     )
            #     sample_list+= tmp[0]
            # sample_pack = Samplepack()
            # sample_pack.samples = sample_list
            # sample_pack.init_id2sample()
            # train_data = sample_pack
            # ret= load_file(
            #         path +mid_rsc15_test_data
            #     )
            # test_data = ret[0]

    return train_data, test_data


def load_conf(model, modelconf):
    '''
    model: 需要加载的模型
    modelconf: model config文件所在的路径
    '''
    # load model config
    model_conf = read_conf(model, modelconf)
    if model_conf is None:
        raise Exception("wrong model config path.", model_conf)
    module = model_conf['module']
    obj = model_conf['object']
    params = model_conf['params']
    params = params.split("/")
    paramconf = ""
    model = params[-1]
    for line in params[:-1]:
        paramconf += line + "/"
    paramconf = paramconf[:-1]
    # load super params.
    param_conf = read_conf(model, paramconf)
    return module, obj, param_conf


def option_parse():
    '''
    parse the option.
    '''
    parser = OptionParser()
    parser.add_option(
        "-m",
        "--model",
        action='store',
        type='string',
        dest="model",
        default='gru4rec'
    )
    parser.add_option(
        "-d",
        "--dataset",
        action='store',
        type='string',
        dest="dataset",
        default='rsc15'
    )
    parser.add_option(
        "-r",
        "--reload",
        action='store_true',
        dest="reload",
        default=False
    )
    parser.add_option(
        "-c",
        "--classnum",
        action='store',
        type='int',
        dest="classnum",
        default=3
    )

    parser.add_option(
        "-a",
        "--nottrain",
        action='store_true',
        dest="not_train",
        default=False
    )
    parser.add_option(
        "-n",
        "--notsavemodel",
        action='store_true',
        dest="not_save_model",
        default=False
    )
    parser.add_option(
        "-p",
        "--modelpath",
        action='store',
        type='string',
        dest="model_path",
        default='/home/herb/code/WWW18/ckpt/seq2seqlm.ckpt-3481-201709251759-lap'
    )
    parser.add_option(
        "-i",
        "--inputdata",
        action='store',
        type='string',
        dest="input_data",
        default='test'
    )
    parser.add_option(
        "-e",
        "--epoch",
        action='store',
        type='int',
        dest="epoch",
        default=10
    )
    (option, args) = parser.parse_args()
    return option


def main(options, modelconf="config/model.conf"):
    '''
    model: 需要加载的模型
    dataset: 需要加载的数据集
    reload: 是否需要重新加载数据，yes or no
    modelconf: model config文件所在的路径
    class_num: 分类的类别
    use_term: 是否是对aspect term 进行分类
    '''
    model = options.model
    dataset = options.dataset
    reload = options.reload
    class_num = options.classnum
    is_train = not options.not_train
    is_save = not options.not_save_model
    model_path = options.model_path
    input_data = options.input_data
    epoch = options.epoch

    module, obj, config = load_conf(model, modelconf)
    config['model'] = model
    print(model)
    config['dataset'] = dataset
    config['class_num'] = class_num
    config['nepoch'] = epoch
    train_data, test_data = load_tt_datas(config, reload)
    module = __import__(module, fromlist=True)

    # setup randomer

    Randomer.set_stddev(config['stddev'])

    with tf.Graph().as_default():
        # build model
        model = getattr(module, obj)(config)
        model.build_model()
        if is_save or not is_train:
            saver = tf.train.Saver(max_to_keep=30)
        else:
            saver = None
        # run
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            if is_train:
                print(dataset)
                if dataset == "cikm16":
                    model.train(sess, train_data, test_data, saver, threshold_acc=config['cikm_threshold_acc'])
                else:
                    model.train(sess, train_data, test_data, saver, threshold_acc=config['recsys_threshold_acc'])
                    # if dataset == "rsc15":
                    #     model.train(sess, train_data, test_data, saver, threshold_acc=config['recsys_threshold_acc'])

            else:
                if input_data is "test":
                    sent_data = test_data
                elif input_data is "train":
                    sent_data = train_data
                else:
                    sent_data = test_data
                saver.restore(sess, model_path)
                model.test(sess, sent_data)


if __name__ == '__main__':
    options = option_parse()
    main(options)
