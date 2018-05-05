import os
import json
import random

from shutil import copyfileobj
from pathlib import Path

import numpy as np

from six.moves import urllib
from sklearn.datasets.base import get_data_home
from sklearn.datasets import fetch_mldata
from sklearn.decomposition import PCA
from PIL import Image
from tqdm import tqdm

# https://github.com/scikit-learn/scikit-learn/issues/8588#issuecomment-292707231


def fetch_mnist(data_home=None):
    mnist_alternative_url = "https://github.com/amplab/datascience-sp14/raw/master/lab7/mldata/mnist-original.mat"
    data_home = get_data_home(data_home=data_home)
    data_home = os.path.join(data_home, 'mldata')
    if not os.path.exists(data_home):
        os.makedirs(data_home)
    mnist_save_path = os.path.join(data_home, "mnist-original.mat")
    if not os.path.exists(mnist_save_path):
        mnist_url = urllib.request.urlopen(mnist_alternative_url)
        with open(mnist_save_path, "wb") as matlab_file:
            copyfileobj(mnist_url, matlab_file)

def f(vec, feature_range=(-1, 1)):
    min_ = min(vec)
    max_ = max(vec)
    ret = [(x - min_) / (max_ - min_) for x in vec]
    ret = [2 * x - 1 for x in ret]
    return np.array(ret)

def main():
    data = []
    indexes = np.random.permutation(70000)[:1000]

    # 10 x 100 だけ画像を並べる
    sprite = Image.new('L', (28 * 10, 28 * 100))

    for cnt, i in tqdm(enumerate(indexes)):
        image = mnist.data[i].reshape(28, 28)
        box = (28 * (cnt // 10), 28 * (cnt % 100))
        sprite.paste(Image.fromarray(image), box)
        data.append({
            'vector': pca_vec[i].tolist(),
            'box': box,
            'label': mnist.target[i],
        })

    sprite.save('data/mnist_sprite.bmp')
    Path('data/mnist_pca.json').write_text(json.dumps(data))


if __name__ == '__main__':
    main()
