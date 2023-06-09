from numpy import array, arange, sin, cos, power, pi
from solution import solve
from manim import *


config.frame_rate = 30
config.pixel_height = 720
config.pixel_width = 1280


class Phase_Space(Scene):
    def __init__(self, start_angle, b, g, l, m, T):
        super().__init__()

        self.Pendulum_Point = 3.5 * LEFT + 0.5 * UP
        self.Scale_Pendulum = 3
        self.Phase_Point = 2.5 * RIGHT
        self.Scale_Phase = 4.5 / 3.2

        self.T = T

        self.continuous_angles, self.continuous_speeds = solve(
            start_angle, b, g, l, m, T
        )

    def phase(self, t):
        continuous_angles_t = self.continuous_angles(t)
        return self.Phase_Point + self.Scale_Phase * array(
            (
                continuous_angles_t,
                self.continuous_speeds(t),
                0,
            )
        )

    def pend(self, t):
        continuous_angles_t = self.continuous_angles(t)
        return self.Pendulum_Point + self.Scale_Pendulum * array(
            (
                sin(continuous_angles_t),
                -cos(continuous_angles_t),
                0,
            )
        )

    def construct(self):
        t = ValueTracker(0)

        ### Axes

        axes = Axes(
            x_range=[-3.2, 3.2],
            y_range=[-2.6, 2.6],
            x_length=6.4 * self.Scale_Phase,
            y_length=5.2 * self.Scale_Phase,
            axis_config={
                "include_tip": True,
                # "color": GREY,
                "stroke_width": 2,
                "font_size": 24,
                "tick_size": 0.07,
                "longer_tick_multiple": 1.5,
                "line_to_number_buff": 0.15,
                "decimal_number_config": {
                    # "color": ORANGE,
                    "num_decimal_places": 0
                },
            },
            x_axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
                "numbers_to_include": arange(-3, 4, 1),
                "numbers_with_elongated_ticks": [-1, 1],
            },
            y_axis_config={
                "tip_width": 0.15,
                "tip_height": 0.15,
                "numbers_to_include": arange(-2, 3, 1),
                "tick_size": 0.08,
                "font_size": 25,
                "numbers_with_elongated_ticks": [-1, 1],
            },
        ).move_to(self.Phase_Point)
        x_lab = axes.get_x_axis_label("\\varphi", direction=UP, buff=0.2)
        y_lab = axes.get_y_axis_label("\\varphi'", direction=RIGHT, buff=0.2)
        labels = VGroup(x_lab.scale(1), y_lab.scale(1))

        self.play(Write(axes, run_time=1), lag_ratio=0.2)

        ### Phase space

        point = always_redraw(
            lambda: Dot(self.phase(t.get_value()), radius=0.07, z_index=2).set_color(
                BLUE
            )
        )
        trace1 = TracedPath(
            point.get_center,
            dissipating_time=self.T,
            stroke_opacity=[1, 1],
            stroke_color=YELLOW,
            stroke_width=6,
            z_index=1,
        )
        self.play(Write(labels))

        ### Pendulum

        dashed_line = DashedLine(
            ORIGIN + self.Pendulum_Point,
            self.Scale_Pendulum * DOWN + self.Pendulum_Point,
        ).set_color(GRAY)
        mass = always_redraw(
            lambda: Dot(self.pend(t.get_value()), radius=0.3).set_color(BLUE)
        )
        line = always_redraw(
            lambda: Line(ORIGIN + self.Pendulum_Point, self.pend(t.get_value()))
        )
        trace2 = TracedPath(
            mass.get_center,
            dissipating_time=0.3,
            stroke_opacity=[0, 1],
            stroke_color="#FF8C00",
            stroke_width=10,
            z_index=1,
        )

        ### Angle

        def theta(x):
            if x >= 0:
                return Angle(
                    dashed_line,
                    line,
                    radius=1,
                    quadrant=(1, 1),
                    stroke_width=8,
                    other_angle=False,
                    color=YELLOW,
                )
            else:
                return Angle(
                    dashed_line,
                    line,
                    radius=1,
                    quadrant=(1, 1),
                    stroke_width=8,
                    other_angle=True,
                    color=YELLOW,
                )

        def label_scale(x):
            if x > pi:
                while x > pi:
                    x = x - 2 * pi
            elif x < -pi:
                while x < -pi:
                    x = x + 2 * pi

            x = abs(x)

            if x > 1:
                return 1
            else:
                return power(x, 1 / 3)

        angle_phi = always_redraw(lambda: theta(self.continuous_angles(t.get_value())))
        label_phi = always_redraw(
            lambda: MathTex("\\varphi", color=YELLOW, z_index=1)
            .scale(1.5 * label_scale(self.continuous_angles(t.get_value())))
            .next_to(angle_phi, DOWN)
        )

        ### launch

        self.add(trace1)

        self.play(
            AnimationGroup(
                Create(dashed_line),
                Create(line),
                Create(angle_phi),
                Write(label_phi),
                DrawBorderThenFill(mass),
                FadeIn(point),
                lag_ratio=0.1,
                run_time=1,
            )
        )

        self.add(trace2)

        self.wait()

        self.play(t.animate.set_value(self.T), run_time=self.T, rate_func=linear)
