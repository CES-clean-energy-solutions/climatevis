import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

def plot_rotated_box(rotation_deg):
    def get_box_vertices():
        return np.array([
            [-0.5, -0.5, -0.5],
            [ 0.5, -0.5, -0.5],
            [ 0.5,  0.5, -0.5],
            [-0.5,  0.5, -0.5],
            [-0.5, -0.5,  0.5],
            [ 0.5, -0.5,  0.5],
            [ 0.5,  0.5,  0.5],
            [-0.5,  0.5,  0.5],
        ])

    faces = [
        [0, 1, 2, 3],  # bottom
        [4, 5, 6, 7],  # top
        [0, 1, 5, 4],  # front (South)
        [2, 3, 7, 6],  # back (North)
        [1, 2, 6, 5],  # right (East)
        [3, 0, 4, 7],  # left (West)
    ]
    face_labels = ['', 'Horizontal', 'South', 'North', 'East', 'West']

    def rotate_z(points, deg):
        theta = np.radians(deg)
        rotation_matrix = np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta),  np.cos(theta), 0],
            [0, 0, 1]
        ])
        return points @ rotation_matrix.T

    vertices = get_box_vertices()
    rotated_vertices = rotate_z(vertices, rotation_deg)

    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='3d')

    for i, face in enumerate(faces):
        poly3d = [rotated_vertices[face]]
        ax.add_collection3d(Poly3DCollection(poly3d, facecolors='lightblue', linewidths=1, edgecolors='k', alpha=0.6))
        center = rotated_vertices[face].mean(axis=0)
        ax.text(*center, face_labels[i], ha='center', va='center')

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_box_aspect([1,1,1])
    ax.axis('off')
    ax.view_init(elev=32, azim=-90)

    return fig