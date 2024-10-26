from manim import *
import numpy as np

# run command:
# manim -qm sinesum.py SineSum --renderer=opengl -p
# manim render sinesum.py SineSum --renderer=opengl -qh --fps 30 --format webm
#

class SineSum(Scene):  # Scene name is 'Sine'
    def construct(self):
        # Parameters for the sine waves
        num_points = 1400
        frequency1 = 10  # 10 Hz
        frequency2 = 5   # 5 Hz
        duration = 1  # 1 second

        # Generate discrete time values over 1 second
        t = np.linspace(0, duration, num_points)

        # Generate 10 Hz sine wave values over 1 second
        y1 = np.sin(2 * np.pi * frequency1 * t)
        # Generate 5 Hz sine wave values over 1 second
        y2 = np.sin(2 * np.pi * frequency2 * t)

        # Create axes with specified labels
        axes = Axes(
            x_range=[0, duration, 0.1],
            y_range=[-2.5, 2.5, 0.5],
            x_length=10,
            y_length=4,
            axis_config={"include_tip": False}
        ).add_coordinates()

        # Add axis labels
        x_label = axes.get_x_axis_label("Time (s)")
        y_label = axes.get_y_axis_label("Amplitude")

        # Plot the axes and labels
        self.play(Create(axes), Write(x_label), Write(y_label))

        # Animate the creation of dots for the first sine wave (10 Hz)
        dots1 = VGroup()
        for i in range(num_points):
            dot = Dot(point=axes.coords_to_point(t[i], y1[i]), color=BLUE, opacity=1.0)
            dots1.add(dot)

        # Animate the creation of dots for the second sine wave (5 Hz)
        dots2 = VGroup()
        for i in range(num_points):
            dot = Dot(point=axes.coords_to_point(t[i], y2[i]), color=RED, opacity=1.0)
            dots2.add(dot)

        # Add a text label for the summed wave    
        sum_label = Text("Sum of 10 Hz and 5 Hz", font_size=24).next_to(axes, UP)

        # Display the LaTeX formula for the sum of two sines
        formula = MathTex(
            r"y(t) = \sin(2\pi \cdot 10 \, t) + \sin(2\pi \cdot 5 \, t)",
            font_size=36
        ).next_to(axes, DOWN, buff=0.5)
        
        self.play(Create(dots1), Create(dots2), Write(sum_label), Write(formula), run_time=3)

        # Generate the sum of the two sine waves
        y_sum = y1 + y2

        # Set opacity of the original waves to 0.1 where the sum wave is drawn
        self.play(
            dots1.animate.set_opacity(0.1),
            dots2.animate.set_opacity(0.1),
        )

        # Animate the creation of dots for the summed wave
        dots_sum = VGroup()
        for i in range(num_points):
            dot = Dot(point=axes.coords_to_point(t[i], y_sum[i]), color=GREEN)
            dots_sum.add(dot)

        # Save original states of dots1 and dots2
        dots1.save_state()
        dots2.save_state()

        for _ in range(3):
            # Forward transformation to sum
            self.play(
                Transform(dots1, dots_sum),
                Transform(dots2, dots_sum),
                run_time=2
            )

            # Backward transformation to original states
            self.play(
                dots1.animate.restore(),
                dots2.animate.restore(),
                run_time=2
            )

        self.play(FadeIn(dots_sum))
        self.wait(5)

        self.interactive_embed()
