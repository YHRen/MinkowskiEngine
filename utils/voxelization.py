import numpy as np

import MinkowskiEngineBackend as MEB


def hash_vec(arr):
    """
    Given a numpy array of N X D, generate hash values using the same hash function used for ME
    """
    assert arr.ndim == 2
    # Floor first for negative coordinates
    arr = np.floor(arr).astype(np.uint64)
    hashed_arr = np.uint64(14695981039346656037) * \
        np.ones(arr.shape[0], dtype=np.uint64)
    for j in range(arr.shape[1]):
        hashed_arr *= np.uint64(1099511628211)
        hashed_arr = np.bitwise_xor(hashed_arr, arr[:, j])
    return hashed_arr


def SparseVoxelize(coords, feats, labels=None, ignore_label=255):
    """
    Given coordinates, and features (optionally labels), generate voxelized coords, features (and labels when given).
    """
    use_label = labels is not None
    assert coords.ndim == 2
    assert feats.ndim == 2
    assert coords.shape[0] == feats.shape[0]
    if use_label:
        assert coords.shape[0] == len(labels)

    # Quantize
    coords = np.floor(coords).astype(np.uint64)

    key = hash_vec(coords)  # floor happens by astype(np.uint64)
    inds, labels = MEB.SparseVoxelization(
        key, labels.astype(np.int32), ignore_label, use_label)

    if use_label:
        return coords[inds], feats[inds]
    else:
        return coords[inds], feats[inds], labels
