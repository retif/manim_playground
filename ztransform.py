from manim import *
import numpy as np

class ZTransform(ThreeDScene):
    def construct(self):
        # Parameters for the simple filter
        grid_res = 50  # Grid resolution for visualization
        epsilon = 1e-10  # Small value to avoid division by zero

        # Define the z-plane grid
        z_real = np.linspace(-1.5, 1.5, grid_res)
        z_imag = np.linspace(-1.5, 1.5, grid_res)
        z_real, z_imag = np.meshgrid(z_real, z_imag)
        z = z_real + 1j * z_imag

        # Define the transfer function H(z) = (z - 0.5) / (z - 0.9)
        numerator = z - 0.5
        denominator = z - 0.9

        # Compute the Z-transform magnitude
        H_z = numerator / (denominator + epsilon)  # Avoid division by zero
        H_z_magnitude = np.abs(H_z)

        # Cap the Z-transform magnitude for visualization clarity
        max_z_cap = 10  # Set a reasonable cap for the Z-axis
        H_z_magnitude = np.clip(H_z_magnitude, 0, max_z_cap)

        # Create 3D axes with capped Z-range
        axes = ThreeDAxes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            z_range=[0, max_z_cap, max_z_cap / 5],
            x_length=7,
            y_length=7,
            z_length=5
        )
        
        # Define a continuous surface with proper integer indexing
        def surface_func(u, v):
            i = int(np.clip((u + 1.5) / 3 * (grid_res - 1), 0, grid_res - 1))
            j = int(np.clip((v + 1.5) / 3 * (grid_res - 1), 0, grid_res - 1))
            z_val = H_z_magnitude[i, j]
            return axes.coords_to_point(u, v, z_val)

        surface = Surface(
            surface_func,
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(grid_res, grid_res),
            fill_opacity=0.8,
            stroke_width=0.5
        )

        # Set up the 3D scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play(Create(axes), Create(surface))
        
        self.interactive_embed()
