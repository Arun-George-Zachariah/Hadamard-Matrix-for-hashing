import logging

def get_config(name):

    config = {}

    if name.upper() == 'UCF101':
        config['num_classes'] = 101
    elif name.upper() == 'HMDB51':
        config['num_classes'] = 51
    elif name.upper() == 'KINETICS':
        config['num_classes'] = 400
    elif name.upper() == 'HOLLYWOOD2':
        config['num_classes'] = 12
    elif name.upper() == 'MSR_VTT':
        config['num_classes'] = 20
    elif name.upper() == 'SVW':
        config['num_classes'] = 30
    else:
        logging.error("Configs for dataset '{}'' not found".format(name))
        raise NotImplemented

    logging.debug("Target dataset: '{}', configs: {}".format(name.upper(), config))

    return config


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)

    logging.info(get_config("ucf101"))
    logging.info(get_config("HMDB51"))
    logging.info(get_config("Kinetics"))
    logging.info(get_config("Hollywood2"))
    logging.info(get_config("MSR_VTT"))
    logging.info(get_config("SVW"))
