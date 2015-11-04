import numpy as np
import scipy as sp
from itertools import product
from learn_multiclass_novelty import learn
from test_multiclass_novelty import score, squared_euclidean_distances
from sklearn import metrics

class KernelNullSpaceClassifier(object):
    def __init__(self, threshold=0.5, metric='hik'):
        self.metric = self._get_metric(metric)
        self.threshold = threshold

    def _hik(self, x,y):
        '''
        Implements the histogram intersection kernel.
        '''
        return np.minimum(x, y).sum()

    # def _get_pairwise_min_dist(self):
    #     dist = np.inf
    #     for pt1, pt2 in product(self.target_points, self.target_points):
    #         if pt1 != pt2:
    #             if 

    def _get_metric(self, kernel):
        '''
        Returns the kernel function to be passed into the pairwise_kernels function
        '''
        if kernel == 'hik':
            return self._hik
        else:
            return kernel

    def fit(self, X, y, sample_weight=None):
        kernel_mat = metrics.pairwise_kernels(X, metric=self.metric)
        proj, target_points = learn(kernel_mat, y)

        self.projection = proj
        self.target_points = target_points
        self.X_train = X

        return self

    def predict(self, X):
        '''
        Returns +1 if the sample is predicted to be novel, -1 otherwise.

        The threshold is selected between 0 and the minimum distance between
        two target points.
        '''
        ks = metrics.pairwise_kernels(X=self.X_train, Y=X, metric=self.metric)
        scores = score(self.projection, self.target_points, ks)
        # min_dist = self._get_pairwise_min_dist()
        prediction = np.array([1 if sc > self.threshold else -1 for sc in scores])

        return scores
