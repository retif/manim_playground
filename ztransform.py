from manim import *
import numpy as np

# run command:
# manim -qm ztransform.py ZTransform --renderer=opengl -p
# manim render ztransform.py ZTransform --renderer=opengl -qh --fps 30 --format webm
#


class ZTransform(ThreeDScene):
    def construct(self):
        # Parameters for the simple filter
        grid_res = 50  # Grid resolution for visualization
        epsilon = 1e-10  # Small value to avoid division by zero

        # Define the z-plane grid range from -1.5 to 1.5
        z_range_min, z_range_max = -1.5, 1.5
        z_real = np.linspace(z_range_min, z_range_max, grid_res)
        z_imag = np.linspace(z_range_min, z_range_max, grid_res)
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
            x_range=[z_range_min, z_range_max, 0.5],
            y_range=[z_range_min, z_range_max, 0.5],
            z_range=[0, max_z_cap, max_z_cap / 5],
            x_length=7,
            y_length=7,
            z_length=5
        )

        # Add axis labels
        x_label = Text("Real", font_size=24).next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("Imaginary", font_size=24).next_to(axes.y_axis.get_end(), UP)
        z_label = Text("Magnitude", font_size=24).next_to(axes.z_axis.get_end(), OUT)

        # Define the surface function representing H(z) magnitude
        def surface_func(u, v):
            z_val = complex(u, v)
            H_val = (z_val - 0.5) / (z_val - 0.9 + epsilon)  # Compute H(z) with epsilon
            magnitude = np.abs(H_val)
            magnitude = np.clip(magnitude, 0, max_z_cap)  # Cap the magnitude
            return axes.coords_to_point(u, v, magnitude)

        # Create the surface representing the magnitude of H(z)
        surface = Surface(
            surface_func,
            u_range=[z_range_min, z_range_max],
            v_range=[z_range_min, z_range_max],
            resolution=(grid_res, grid_res),
            fill_opacity=0.8,
            stroke_width=0.5
        )

        # Add the Z-transform transfer function label
        self.add_fixed_in_frame_mobjects(MathTex(r"H(z) = \frac{z - 0.5}{z - 0.9}").to_corner(UL))

        # Set up the 3D scene with the new camera orientation
        self.set_camera_orientation(phi=30 * DEGREES, theta=10 * DEGREES)
        self.camera.move_to([-0.5, 0, 0])

        # Add axes, surface, and labels instantly
        self.add(axes, surface, x_label, y_label, z_label)

        # Add the unit circle, scaled according to the Z-plane
        unit_circle_radius = (axes.x_axis.get_length() / (z_range_max - z_range_min))  # Adjusted to match Z-plane scaling
        unit_circle = Circle(radius=unit_circle_radius, color=YELLOW, stroke_width=4)
        unit_circle.move_to(axes.c2p(0, 0, 0))  # Center at the origin
        unit_circle.rotate_about_origin(PI/2, axis=OUT)  # Align with the real-imaginary plane
        self.add(unit_circle)

        # Add zero at z = 0.5, marked as a small empty circle
        zero_marker = Circle(radius=0.1, color=BLUE, stroke_width=4)
        zero_position = axes.c2p(0.5, 0, 0)
        zero_marker.move_to(zero_position)
        self.add(zero_marker)

        # Add pole at z = 0.9, marked as a cross
        pole_marker = Cross(stroke_color=RED, stroke_width=4)
        pole_marker.scale(0.2)  # Adjust size of the cross
        pole_position = axes.c2p(0.9, 0, 0)
        pole_marker.move_to(pole_position)
        self.add(pole_marker)

        # Define points of interest in the new order, including (0, 0) and (1, 0)
        points_of_interest = [
            (0.5, 0.5), (0.5, -0.5), (0.5, 0.5), (0.5, -0.5), (0.5, 0.5), 
            (0, 0), (0.5, -0.5), (0,0), (0.5, 0.5), (0,0), (0.5, -0.5),
            (0, 0), (1, 0), (0, 0), (1, 0), (0, 0), (1, 0),
            (0.5, -0.5), (-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5)
        ]

        scaled_points = [axes.c2p(real, imag, 0) for real, imag in points_of_interest]

        # Visualize each point of interest as a sphere
        for i, (real, imag) in enumerate(points_of_interest):
            poi_dot = Sphere(radius=0.05, color=GREEN)  # Use spheres for better visibility
            poi_dot.move_to(axes.c2p(real, imag, 0))
            self.add(poi_dot)
            # Add a label for each POI and place it near the point
            label = MathTex(f"({real}, {imag})").scale(0.5)
            label.next_to(poi_dot, UP + RIGHT, buff=0.1)  # Position label near the point
            self.add(label)  # Add label to the 3D scene so it moves with the view

        # Add animated vertical pointer on Z-plane
        pointer = Dot3D(color=GREEN, radius=0.1)
        pointer.move_to(scaled_points[0])  # Start at the first point of interest
        self.add(pointer)

        # Create a fixed-position text box showing Re(z), Im(z), and H(z) in LaTeX
        def get_characteristics_text():
            # Convert the 3D point back to real and imaginary parts
            x, y, _ = axes.point_to_coords(pointer.get_center())

            # Compute H(z) for the current position
            z_val = complex(x, y)
            H_val = (z_val - 0.5) / (z_val - 0.9)

            # LaTeX representation of H(z) with substituted values
            H_substituted = MathTex(
                r"H(z) = \frac{" +
                f"({x:.2f} {'+' if y >= 0 else '-'} {abs(y):.2f}j) - 0.5" +
                "}{" +
                f"({x:.2f} {'+' if y >= 0 else '-'} {abs(y):.2f}j) - 0.9" +
                r"} = " +
                f"{H_val.real:.2f} {'+' if H_val.imag >= 0 else '-'} {abs(H_val.imag):.2f}j"
            )

            re_text = MathTex(f"\\text{{Re}}(z) = {x:.2f}").align_to(LEFT)
            im_text = MathTex(f"\\text{{Im}}(z) = {y:.2f}").align_to(LEFT)
            h_text = H_substituted.align_to(LEFT)

            # Arrange and align texts to the left
            return VGroup(re_text, im_text, h_text).arrange(DOWN, aligned_edge=LEFT).to_corner(DL)

        characteristics_text = always_redraw(get_characteristics_text)
        self.add_fixed_in_frame_mobjects(characteristics_text)

        # Animate the pointer sequentially through the scaled points of interest
        for point in scaled_points:
            self.play(pointer.animate.move_to(point), run_time=5)

        self.wait(5)

        self.interactive_embed()
