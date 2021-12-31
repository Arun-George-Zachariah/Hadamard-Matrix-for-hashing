from scipy.linalg import hadamard
import torch
import numpy as np

if __name__ == "__main__":
    num_class = 30
    d_vals = [16, 32, 64]

    for d in d_vals:
        ha_d = hadamard(d)
        ha_2d = np.concatenate((ha_d, -ha_d),0)

        if num_class <= d:
            hash_targets = torch.from_numpy(ha_d[0:num_class]).float()
            print('hash centers shape: {}'.format(hash_targets.shape))
        elif num_class > d:
            hash_targets = torch.from_numpy(ha_2d[0:num_class]).float()
            print('hash centers shape: {}'.format(hash_targets.shape))

        file_name = str(d) + '_hollywood2_' + str(num_class) + '_class.pkl'
        file_dir = '../raw/' + file_name
        f = open(file_dir, "wb")
        torch.save(hash_targets, f)
