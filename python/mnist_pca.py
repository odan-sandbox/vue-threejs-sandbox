import os
import json
import random

from shutil import copyfileobj
from pathlib import Path

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


def main():
    random.seed(42)
    fetch_mnist()
    mnist = fetch_mldata('MNIST original', data_home='data')

    pca = PCA(n_components=3)
    pca_vec = pca.fit_transform(mnist.data / 255)

    N = mnist.data.shape[0]
    images_dir = Path('data/images')
    images_dir.mkdir(exist_ok=True)

    data = []
    for i in tqdm(range(N)):
        path = str(images_dir / '{:05}.bmp'.format(i))
        Image.fromarray(mnist.data[i].reshape(28, 28)).save(path)
        data.append({
            'vector': pca_vec[i].tolist(),
            'path': path,
            'label': mnist.target[i]
        })

    random.shuffle(data)
    Path('data/mnist_pca.json').write_text(json.dumps(data))


if __name__ == '__main__':
    main()
