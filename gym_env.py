from isaacgym import gymapi
from isaacgym import gymtorch
from isaacgym import gymutil
import numpy as np
import torch
import random
import argparse
import o3d_mesh


parser = argparse.ArgumentParser()

parser.add_argument('--num_envs', type=int, default=1, help='number of environments to simulate')
parser.add_argument('--object', type=str, default="cube", help='object to load')


args = parser.parse_args()

device = "cuda" if torch.cuda.is_available() else "cpu"

gym = gymapi.acquire_gym()

# setup base simulation parameters
sim_params = gymapi.SimParams()

sim_params.dt = 1 / 60
sim_params.substeps = 2
sim_params.up_axis = gymapi.UP_AXIS_Z
sim_params.gravity = gymapi.Vec3(0.0, 0.0, -9.81)

# set PhysX-specific parameters
sim_params.physx.use_gpu = True
sim_params.physx.solver_type = 1
sim_params.physx.num_position_iterations = 6
sim_params.physx.num_velocity_iterations = 1
sim_params.physx.contact_offset = 0.01
sim_params.physx.rest_offset = 0.0
sim_params.use_gpu_pipeline = True

# create simulation
sim = gym.create_sim(0,0, gymapi.SIM_PHYSX, sim_params)

# configure the ground plane
plane_params = gymapi.PlaneParams()
plane_params.normal = gymapi.Vec3(0,0,1) 
plane_params.static_friction = 1    
plane_params.dynamic_friction = 1      
plane_params.restitution = 0        

gym.add_ground(sim, plane_params)

# environment variables
num_envs = args.num_envs
envs_per_row = int(np.sqrt(num_envs))
spacing = 3
lower = gymapi.Vec3(-spacing, -spacing, -spacing)
upper = gymapi.Vec3(spacing, spacing, spacing)

envs = []
actor_handles = []
rotated_meshes = []

# asset creation
asset_opt = gymapi.AssetOptions()
asset_opt.fix_base_link = True
asset_root = "urdf"
asset_file = args.object + ".urdf"
print("Loading asset '%s' from '%s'" % (asset_file, asset_root))
asset = gym.load_asset(sim, asset_root, asset_file, asset_opt)

# create corresponding o3d mesh
mesh = o3d_mesh.create_mesh("mesh/" + args.object + ".obj")

for i in range(num_envs):
    env = gym.create_env(sim, lower, upper, envs_per_row)
    envs.append(env)

    pose = gymapi.Transform()
    pose.p = gymapi.Vec3(0,0,0)
    
    # quaternion variables, need to rotate cube on z axis
    x = 0
    y = 0
    z = random.uniform(-1,1)
    w = np.sqrt(1-z**2)
    pose.r = gymapi.Quat(x,y,z,w)

    # for o3d, quatermions are in the form (w,x,y,z)
    quat = np.array([w,x,y,z])

    # create corresponding rotation with o3d
    mesh_r = o3d_mesh.rotate_mesh(mesh, quat)
    rotated_meshes.append(mesh_r)

    # create actor handle
    box_num = str(i)
    actor_handle = gym.create_actor(env, asset, pose, "object "+ box_num, i, 1)
    actor_handles.append(actor_handle)

    gym.set_rigid_body_color(env, actor_handle, 0, gymapi.MESH_VISUAL_AND_COLLISION, gymapi.Vec3(0,0,1))
    
# camera and viewer setup
cam_props = gymapi.CameraProperties()
viewer = gym.create_viewer(sim, cam_props)


def draw_mesh(mesh):
    for j in range(num_envs):
        mesh_use = mesh[j]
        vertices = np.asarray(mesh_use.vertices)
        line_height = 0.01
        for i in range(len(vertices)):
            gym.add_lines(viewer, envs[j], 1, (float(vertices[i,0]), float(vertices[i,1]), float(vertices[i,2]), float(vertices[i,0]), float(vertices[i,1]), float(vertices[i,2]) + line_height), (1, 0, 0))

# plot lines in gym to visualize mesh
draw_mesh(rotated_meshes)

gym.viewer_camera_look_at(viewer, None, gymapi.Vec3(10, 10, 10), gymapi.Vec3(0, 0, 1))
gym.prepare_sim(sim)

frame_count = 0

while not gym.query_viewer_has_closed(viewer):
    gym.simulate(sim)
    gym.fetch_results(sim, True)

    gym.step_graphics(sim)
    gym.draw_viewer(viewer, sim, True)

gym.destroy_viewer(viewer)
gym.destroy_sim(sim)


