**Visualizing Meshes in Isaac Gym**

This repo uses Open3D in order to get access to vertices in Isaac Gym. Objects with random rotation are spawned in Isaac Gym, with the vertices of the mesh visualized using O3D. New objects can be loaded in, just follow naming convention and provide .urdf and .obj file.

Usage

    python gym_env.py
    
- use --num_envs and --object flags in command line
