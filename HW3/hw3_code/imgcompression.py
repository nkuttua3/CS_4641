import numpy as np


class ImgCompression(object):
    def __init__(self):
        pass

    def svd(self, X):  # [5pts]
        """
        Do SVD. You could use numpy SVD.
        Your function should be able to handle black and white
        images ((N,D) arrays) as well as color images ((N,D,3) arrays)
        In the image compression, we assume that each column of the image is a feature. Perform SVD on the channels of
        each image (1 channel for black and white and 3 channels for RGB)
        Image is the matrix X.

        Args:
            X: (N,D) numpy array corresponding to black and white images / (N,D,3) numpy array for color images

        Return:
            U: (N,N) numpy array for black and white images / (N,N,3) numpy array for color images
            S: (min(N,D), ) numpy array for black and white images / (min(N,D),3) numpy array for color images
            V^T: (D,D) numpy array for black and white images / (D,D,3) numpy array for color images
        """
        if len(X.shape) < 3:
            return np.linalg.svd(X)

        temp = np.linalg.svd(
            np.transpose(
                X,
                (2, 0, 1)
            )
        )
        return \
        np.transpose(
            temp[0],
            (1, 2, 0)
        ), \
        np.transpose(
            temp[1],
            (1, 0)
        ), \
        np.transpose(
            temp[2],
            (1, 2, 0)
        )

    def rebuild_svd(self, U, S, V, k):  # [5pts]
        """
        Rebuild SVD by k componments.

        Args:
            U: (N,N) numpy array for black and white images / (N,N,3) numpy array for color images
            S: (min(N,D), ) numpy array for black and white images / (min(N,D),3) numpy array for color images
            V: (D,D) numpy array for black and white images / (D,D,3) numpy array for color images
            k: int corresponding to number of components

        Return:
            Xrebuild: (N,D) numpy array of reconstructed image / (N,D,3) numpy array for color images

        Hint: numpy.matmul may be helpful for reconstructing color images
        """
        if len(U.shape) < 3:
            return np.dot(
                U[:, : k],
                np.dot(
                    np.diag(S[: k]),
                    V[: k]
                )
            )

        temp = np.zeros((3, k, k))
        temp[
            :,
            np.arange(k),
            np.arange(k)
        ] = np.transpose(
            S,
            (1, 0)
        )[:, : k]

        return np.transpose(
            np.transpose(
                U,
                (2, 0, 1)
            )[:, :, : k] @ temp @ np.transpose(
                V,
                (2, 0, 1)
            )[:, : k],
            (1, 2, 0)
        )

    def compression_ratio(self, X, k):  # [5pts]
        """
        Compute the compression ratio of an image: (num stored values in compressed)/(num stored values in original)

        Args:
            X: (N,D) numpy array corresponding to black and white images / (N,D,3) numpy array for color images
            k: int corresponding to number of components

        Return:
            compression_ratio: float of proportion of storage used by compressed image
        """
        return k * (X.shape[0] + X.shape[1] + 1) / (X.shape[0] * X.shape[1])

    def recovered_variance_proportion(self, S, k):  # [5pts]
        """
        Compute the proportion of the variance in the original matrix recovered by a rank-k approximation

        Args:
           S: (min(N,D), ) numpy array black and white images / (min(N,D),3) numpy array for color images
           k: int, rank of approximation

        Return:
           recovered_var: float (array of 3 floats for color image) corresponding to proportion of recovered variance
        """
        return sum(S[: k] ** 2) / sum(S ** 2)