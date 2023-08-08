import open3d as o3d
import numpy as np
import copy
import random
import isaacgym

def create_mesh(filename):
    # linking mesh with o3d
    print("Connecting Open3D...")
    mesh = o3d.io.read_triangle_mesh(filename)
    mesh.compute_triangle_normals()
    
    return mesh

def rotate_mesh(mesh, quat):
    # apply rotation to open3d mesh as well, in order to grab vertex coordinates
    mesh_r = copy.deepcopy(mesh)
    R = mesh.get_rotation_matrix_from_quaternion(quat)

    # rotate cube around the 0
    mesh_r.rotate(R, center=(0,0,0))

    return mesh_r

