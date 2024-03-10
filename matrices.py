from manim import *
from my_imports import RT, VT, get_dims, render


def surround(mob, color, *args, **kwargs):
    return SurroundingRectangle(mob, color, *args, buff=0.25, corner_radius=0.4, fill_opacity=0.35, stroke_opacity=0.0, **kwargs)

def circumscribe(mob, color):
    return Circumscribe(mob, color=color, time_width=0.75, buff=0.25)


class MyArrow(Polygon):
    def __init__(self, direction=RIGHT, *args, **kwargs):
        x, y, z = np.asarray(direction) / np.linalg.norm(direction)
        super().__init__(
            [x, y, z], [-y, x, z], [y, -x, z], [x, y, z], *args, **kwargs
        )
        self.move_to(ORIGIN)


class LinearMap0(Scene):
    def construct(self):
        H, W = get_dims(self)

        # FASE INICIAL
        header = Paragraph(
            "FUNCIÓN",
            "MULTIVARIABLE",
            alignment="center",
            color=XKCD.BRICK,
            font="Noto Sans",
            weight=HEAVY,
        ).scale(2).shift(3 * UP)
        linear_map = MathTex(
            "T"
            r"\begin{pmatrix}"
            r"x \\ y"
            r"\end{pmatrix}"
            r"="
            r"\begin{pmatrix}"
            r"ax + by \\ cx + dy"
            r"\end{pmatrix}",
            color=XKCD.DARKBROWN,
        ).scale(2.5).shift(2 * DOWN)

        self.play(
            LaggedStart(
                *[FadeIn(line, shift=0.4*UP, run_time=0.6) for line in header],
                Write(linear_map, run_time=1.0),
                lag_ratio=0.2,
            ),
            run_time=1.1,
        )
        self.wait(0.5)

        # DESPLEGAR BARRA INFERIOR
        bottom_bar = Rectangle(
            XKCD.MUD, H/2, W, fill_opacity=1, stroke_opacity=0
        ).shift(H/4 * DOWN)
        examples = [
            VGroup(
                *[SingleStringMathTex(string, color=XKCD.BEIGE)
                for string in (
                    "T"
                    r"\begin{pmatrix}"
                    r"x \\ y"
                    r"\end{pmatrix}",

                    "=",

                    r"\begin{pmatrix}"
                    + content +
                    r"\end{pmatrix}",
                )]
            ).arrange_submobjects(RIGHT).scale(2.25).shift(3 * DOWN)
            for content in (r"x^2 + y^2 \\ 2xy", r"e^{x+y} \\ e^{x-y}", r"2x - 3y \\ x + 2y")
        ]
        footer = VGroup(
            *[Text(
                text,
                color=XKCD.SKYBLUE,
                font="Noto Sans",
                weight=HEAVY,
            ).scale(1.55)
            for text in ("FUNCIÓN", "CUADRÁTICA", "EXPONENCIAL", "LINEAL")]
        )
        cross = Cross(stroke_width=100).scale(1.75).shift(9*DOWN)
        mark = Text("✓", color=GREEN, weight=HEAVY).scale_to_fit_height(cross.height).move_to(cross)

        temp = footer[:2].arrange_submobjects(RIGHT, buff=0.5).shift(5.5 * DOWN)
        temp[1].align_to(temp[0], DOWN)
        self.play(
            LaggedStart(
                VGroup(header, linear_map).animate.shift(6 * UP),
                FadeIn(bottom_bar, shift=UP),
                *[FadeIn(mob, shift=0.5 * UP, run_time=0.7) for mob in (examples[0], temp, cross)],
                lag_ratio=0.25,
            ),
            run_time=1.0,
        )
        self.wait(0.4)

        # CUADRÁTICA -> EXPONENCIAL -> LINEAL
        footer[0].generate_target()
        temp = VGroup(
            footer[0].target, footer[2]
        ).arrange_submobjects(RIGHT, buff=0.5).shift(5.5 * DOWN)
        temp[1].align_to(temp[0], DOWN)
        self.play(
            MoveToTarget(footer[0], run_time=0.3),
            RT(examples[0], examples[1], run_time=0.5),
            LaggedStart(
                FadeOut(footer[1], shift=0.5 * UP),
                FadeIn(footer[2], shift=0.5 * UP),
                lag_ratio=0.5,
                run_time=0.5,
            ),
            run_time=0.5,
        )
        self.wait(0.6)

        temp = VGroup(
            footer[0].target, footer[3]
        ).arrange_submobjects(RIGHT, buff=0.5).shift(5.5 * DOWN)
        temp[1].align_to(temp[0], DOWN)
        self.play(
            MoveToTarget(footer[0], run_time=0.3),
            RT(examples[1], examples[2], run_time=0.5),
            LaggedStart(
                FadeOut(footer[2], shift=0.5 * UP),
                FadeIn(footer[3], shift=0.5 * UP),
                lag_ratio=0.5,
                run_time=0.5,
            ),
            LaggedStart(
                FadeOut(cross, shift=RIGHT),
                FadeIn(mark, shift=RIGHT),
                lag_ratio=0.5,
                run_time=0.5,
            ),
            run_time=0.5,
        )
        self.wait(1.2)

        atlas = ImageMobject("atlas.jpg").scale_to_fit_width(2.2*W)
        atlas.add(
            Rectangle(GRAY_D, atlas.height, atlas.width, stroke_opacity=0.0, fill_opacity=0.5),
            Paragraph(
                "ÁLGEBRA",
                "LINEAL",
                alignment="center",
                font="Noto Sans",
                weight=HEAVY,
            ).scale(2.75).shift(4.5*DOWN + 0.5*RIGHT),
            Text(
                "CÁLCULO",
                color=XKCD.BANANA,
                font="Noto Sans",
                weight=HEAVY,
            ).scale(3).shift(7.25*UP + LEFT),
        )
        atlas.move_to(0.5 * (atlas.height - H) * UP)
        
        self.add(atlas)

        t = VT(0.0)
        
        def updater(atlas):
            if ~t < 0.25:
                opacity = 0.5 * (1 - np.cos(TAU/2 * ~t/0.25))
            else:
                opacity = 1

            for i in 0, 2, 3:
                atlas[i].set_opacity(opacity)
            atlas[1].set_opacity(0.3 * opacity)
            atlas.move_to(UP * 0.5 * (atlas.height - H) * (1 - 2/7 * ~t - 0.3) + 0.5*RIGHT)

        atlas.add_updater(updater)

        self.play(t.animate.set_value(1.75), run_time=1.75, rate_func=linear)
        
        dark_rectangle = Rectangle(GRAY_E, H, W, stroke_opacity=0.0, fill_opacity=0.85)
        derivatives = VGroup(
            Text("DERIVADAS", color=XKCD.BEIGE, font="Noto Sans", weight=HEAVY).scale(1.5),
            MathTex(
                r"\frac{d}{dx}\left( f(x) + g(x) \right)"
                "="
                r"\frac{d}{dx}\left( f(x) \right)"
                "+"
                r"\frac{d}{dx}\left( g(x) \right)\\",

                r"\frac{d}{dx}\left( \alpha f(x) \right)"
                "="
                r"\alpha \frac{d}{dx}\left( f(x) \right)",
            ).arrange_submobjects(DOWN, buff=0.6),
        ).scale(1.4).arrange_submobjects(DOWN, buff=1.0).shift(6.5*UP)

        integrals = VGroup(
            Text("INTEGRALES", color=XKCD.BEIGE, font="Noto Sans", weight=HEAVY).scale(1.5),
            MathTex(
                r"\int \left( f(x) + g(x) \right) dx"
                "="
                r"\int f(x) dx"
                "+"
                r"\int g(x) dx\\",

                r"\int \alpha f(x) dx"
                "="
                r"\alpha \int f(x) dx",
            ).arrange_submobjects(DOWN, buff=0.6),
        ).scale(1.4).arrange_submobjects(DOWN, buff=1.0).shift(6.5*DOWN)

        note = VGroup(
            Text("Las derivadas e integrales son", font="Noto Sans").scale(1.1),
            Text("OPERADORES LINEALES", color=XKCD.SKYBLUE, font="Noto Sans", weight=HEAVY).scale(1.6),
        ).arrange_submobjects(DOWN)

        self.play(
            AnimationGroup(
                FadeIn(dark_rectangle),
                FadeIn(note, derivatives, integrals, shift=0.5*UP),
                rate_func=smooth,
            ),
            t.animate.set_value(2.15),
            run_time=0.3,
            rate_func=linear,
        )
        self.play(
            t.animate.set_value(4.25),
            run_time=2.1,
            rate_func=linear,
        )

        light_rectangle = dark_rectangle.copy().set_fill(GRAY_E, opacity=1.0)
        self.play(
            AnimationGroup(
                FadeIn(light_rectangle),
                rate_func=smooth,
            ),
            t.animate.set_value(4.5),
            run_time=0.25,
            rate_func=linear,
        )
        atlas.clear_updaters()
        self.remove(*self.mobjects)


class LinearMap1(ThreeDScene):
    def construct(self):
        H, W = get_dims(self)
        self.camera.background_color = GRAY_E
        self.set_camera_orientation(TAU/5, -TAU/5, 0)
        self.begin_ambient_camera_rotation(0.035)

        plane = Surface(
            lambda u, v: np.array([u, v, 0]),
            u_range=[-20, 20],
            v_range=[-20, 20],
            resolution=20,
            checkerboard_colors=[XKCD.MAIZE, XKCD.REDDISHBROWN],
            fill_opacity=0.1, stroke_opacity=0.0,
        )
        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[-1, 3.5],
            x_length=12,
            y_length=12,
            z_length=9,
        )

        def bicubic_bezier_surface(points):
            def func(u, v):
                point = np.zeros(3)
                for i, ci in enumerate((1, 3, 3, 1)):
                    for j, cj in enumerate((1, 3, 3, 1)):
                        point += ci * cj * (u ** (3-i)) * ((1-u) ** i) * (v ** (3-j)) * ((1-v) ** j) * points[i, j]

                return point
            
            return func

        faces = []

        with open("teapot_bezier") as file:
            line = file.readline()
            while line:
                line = line.strip()
                if line == "array(":
                    array = []
                    for _ in range(4):
                        inner_array = []
                        for _ in range(4):
                            line = file.readline().strip()
                            if line.startswith("array( "):
                                line = line[7:]
                            line = line[4:-3] # remove "pt( " and " )," or " );"
                            while line.endswith(" )"):
                                line = line[:-2]
                            point = list(map(float, line.split(", ")))
                            inner_array.append(point)
                        array.append(inner_array)
                    array = np.array(array)
                    bicubic = bicubic_bezier_surface(array)
                    points = np.array([[bicubic(i/3, j/3) for j in range(4)] for i in range(4)])
                    for i in range(3):
                        for j in range(3):
                            (p1, p2), (p4, p3) = points[i:i+2, j:j+2]
                            face = ThreeDVMobject(
                                color=GRAY, fill_opacity=1.0, stroke_opacity=0.0,
                            ).set_points_as_corners([p1, p2, p3, p4, p1])
                            faces.append(face)

                line = file.readline()

        teapot = VGroup(*faces).rotate_about_origin(TAU/4, RIGHT)
        p1, p2 = teapot.get_corner(IN + DOWN + LEFT), teapot.get_corner(OUT + UP + RIGHT)
        w, h, d = p2 - p1
        box = []

        kwargs = {"thickness": 0.01, "resolution": [1, 4], "fill_opacity": 0.75, "stroke_opacity": 0.0}
        for start in (p1, p1 + h*UP, p1 + h*UP + d*OUT, p1 + d*OUT):
            box.append(Line3D(start, start + w*RIGHT, color=RED, **kwargs))
        for start in (p1, p1 + w*RIGHT, p1 + w*RIGHT + d*OUT, p1 + d*OUT):
            box.append(Line3D(start, start + h*UP, color=GREEN, **kwargs))
        for start in (p1, p1 + w*RIGHT, p1 + w*RIGHT + h*UP, p1 + h*UP):
            box.append(Line3D(start, start + d*OUT, color=BLUE, **kwargs))

        box = VGroup(*box)
        teapot.add(box)

        axis_labels = axes.get_axis_labels()
        for i, color in enumerate([RED, GREEN, BLUE]):
            VGroup(axes[i], axis_labels[i]).set_color(color)
        VGroup(plane, axes, axis_labels, teapot, box).shift(4*IN)

        self.add(plane, axes, axis_labels, teapot)

        rectangle = Rectangle(GRAY_E, H, W, fill_opacity=1.0, stroke_opacity=0.0)
        self.add_fixed_in_frame_mobjects(rectangle)
        self.wait(1/30)
        self.play(
            FadeOut(rectangle),
            run_time=0.25,
        )
        self.wait(0.5)

        R = MathTex(
            r"R \begin{pmatrix} x \\ y \\ z \end{pmatrix}"
            "="
            r"\begin{pmatrix} -y \\ x \\ z \end{pmatrix}",
            color=XKCD.BEIGE
        ).scale(1.45).shift(3.75*LEFT + 6*UP)
        R_text = Paragraph(
            "rotación de 90°",
            "en el plano XY",
            alignment="center",
            color=RED_B,
            font="Open Sans",
        ).next_to(R, UP, buff=0.8)

        self.add_fixed_in_frame_mobjects(R, R_text)
        
        self.play(FadeIn(R, R_text), run_time=0.3)
        self.play(Rotate(teapot, TAU/4), run_time=0.7)
        self.wait(0.5)

        S = MathTex(
            r"S \begin{pmatrix} x \\ y \\ z \end{pmatrix}"
            "="
            r"\begin{pmatrix} 0.5x \\ y \\ 2z \end{pmatrix}",
            color=XKCD.BEIGE
        ).scale(1.45).shift(3.75*RIGHT + 6*UP)
        S_text = Paragraph(
            "escalado",
            "(estirar z al doble",
            "y comprimir x",
            "a la mitad)",
            alignment="center",
            color=BLUE_B,
            font="Open Sans",
        ).next_to(S, UP, buff=0.8)

        self.add_fixed_in_frame_mobjects(S, S_text)
        
        self.play(FadeIn(S, S_text), run_time=0.3)
        self.play(
            teapot.animate.apply_points_function_about_point(
                lambda points: np.array([0.5, 1, 2]) * points,
                about_point=4*IN,
            ),
            run_time=0.7,
        )
        self.wait(0.5)

        TP_text = Paragraph(
            "La traslación y el cambio",
            "de perspectiva requieren",
            "4 dimensiones para ser",
            "lineales",
            alignment="center",
            font="Open Sans",
        ).scale(1.35).move_to(7*DOWN)

        self.add_fixed_in_frame_mobjects(TP_text)

        self.play(
            FadeIn(TP_text, run_time=0.5),
            teapot.animate.shift(OUT + 2*UP),
            run_time=0.7,
        )
        self.wait(0.5)

        self.move_camera(TAU/5, -TAU/5, 0, None, 4, run_time=0.7)
        self.wait(0.75)

        rectangle = Rectangle(XKCD.MAIZE, H, W, fill_opacity=1.0, stroke_opacity=0.0)

        self.add_fixed_in_frame_mobjects(rectangle)

        self.play(FadeIn(rectangle), run_time=0.25)


class LinearMap2(Scene):
    def construct(self):
        self.camera.background_color = XKCD.CINNAMON
        H, W = get_dims(self)
        
        top_bar = Rectangle(
            XKCD.MAIZE, H, W, fill_opacity=1, stroke_opacity=0
        )
        self.add(top_bar)

        linear_map = SingleStringMathTex(
            "T"
            r"\begin{pmatrix}"
            r"x \\ y"
            r"\end{pmatrix}"
            r"="
            r"\begin{pmatrix}"
            r"ax + by \\ cx + dy"
            r"\end{pmatrix}",
            color=XKCD.DARKBROWN,
            z_index=1,
        ).scale(2.5)
        coefficients = VGroup(*[linear_map[i] for i in (7, 10, 12, 15)]).set_z_index(1)
        coefficients.set_color(RED_E)

        self.play(FadeIn(linear_map, shift=UP), run_time=0.35)
        self.wait(1.0)

        matrix_group = VGroup(
            Text("MATRIZ", color=XKCD.SALMON, font="Noto Sans", weight=HEAVY).scale(2.25),
            SingleStringMathTex(
                r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}",
                color=XKCD.MAIZE,
            ).scale(3.2),
        ).arrange_submobjects(DOWN, buff=1.0).move_to(H/4 * DOWN).set_z_index(-1)
        matrix_group[1][1:-1].set_color(RED_B)

        coeffs_text = Text(
            "COEFICIENTES", color=XKCD.MAIZE, font="Open Sans", weight=HEAVY
        ).scale(2.25).move_to(matrix_group[0])

        self.play(
            AnimationGroup(
                AnimationGroup(
                    top_bar.animate.shift(H/2 * UP),
                    linear_map.animate.shift(H/4 * UP),
                    run_time=1.0,
                ),
                LaggedStart(
                    RT(coefficients.copy(), matrix_group[1][1:-1]),
                    FadeIn(coeffs_text),
                    run_time=1.5,
                    lag_ratio=0.25,
                ),
                run_time=1.25,
            ),
            run_time=1.2,
        )
        self.wait(0.3)

        self.play(
            LaggedStart(
                FadeOut(coeffs_text, shift=0.5*DOWN),
                FadeIn(matrix_group[0], matrix_group[1][0], matrix_group[1][-1], shift=0.5*DOWN),
                lag_ratio=0.5,
            ),
            run_time=0.6,
        )
        self.wait(0.35)
        
        bottom_bar = Rectangle(
            XKCD.MUD, H, W, fill_opacity=1, stroke_opacity=0
        ).shift(H * DOWN)

        matrix_map = SingleStringMathTex(
            r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}"
            r"\begin{pmatrix} x \\ y \end{pmatrix}"
            "="
            r"\begin{pmatrix} ax + by \\ cx + dy \end{pmatrix}",
            color=XKCD.MAIZE,
            z_index=1,
        ).scale(2.25).shift(H/3 * DOWN)
        VGroup(*[matrix_map[i] for i in (*range(1, 5), 12, 15, 17, 20)]).set_color(RED_B) # a, b, c, d
        VGroup(*[matrix_map[i] for i in (*range(6, 10), 13, 16, 18, 21)]).set_color(GREEN) # x, y

        self.play(
            LaggedStart(
                AnimationGroup(
                    top_bar.animate.shift(H/6 * UP),
                    bottom_bar.animate.shift(H/3 * UP),
                    matrix_group.animate.move_to(ORIGIN),
                    linear_map.animate.move_to(H/3 * UP),
                    RT(matrix_group[1].copy().set_z_index(1), matrix_map[:6]),
                    run_time=1.0,
                ),
                Write(matrix_map[6:], run_time=1.1),
                lag_ratio=0.45,
            ),
            run_time=1.3,
        )
        self.wait(0.6)

        info_text = VGroup(
            *[Text(string, color=color, font="Noto Sans", weight=weight)
            for string, color, weight in zip(
                ["ENORME", "fuente de", "INFORMACIÓN", "que describe una", "TRANSFORMACIÓN LINEAL"],
                [XKCD.ORANGEISH if i % 2 == 0 else XKCD.BEIGE for i in range(5)],
                [HEAVY if i % 2 == 0 else NORMAL for i in range(5)],
            )]
        ).arrange_submobjects(RIGHT, buff=0.25)
        for submob in info_text[1:]:
            submob.align_to(info_text[0], DOWN)
        VGroup(info_text[:3], info_text[3], info_text[4:]).arrange_submobjects(DOWN, buff=0.35)
        info_text[4].scale(1.25).shift(0.15 * UP)
        VGroup(matrix_group.generate_target(), info_text).arrange_submobjects(DOWN, buff=1.0)

        self.play(
            LaggedStart(
                AnimationGroup(
                    top_bar.animate.shift(H/12 * UP),
                    bottom_bar.animate.shift(H/12 * DOWN),
                    linear_map.animate.shift(H/24 * UP),
                    matrix_map.animate.shift(H/24 * DOWN),
                    MoveToTarget(matrix_group),
                ),
                FadeIn(info_text, shift=0.5*UP),
                lag_ratio=0.2,
            ),
            run_time=0.6,
        )
        self.wait(1.25)

        VGroup(matrix_group, info_text).set_z_index(-1)

        self.play(
            top_bar.animate.shift(H/4 * DOWN),
            bottom_bar.animate.shift(H/4 * UP),
            FadeOut(linear_map, shift=H/4 * UP),
            FadeOut(matrix_map, shift=H/4 * DOWN),
            run_time=0.45,
            rate_func=rush_into,
        )


class LinearMap3(Scene):
    def construct(self):
        H, W = get_dims(self)

        # Preparación
        bottom_bar = Rectangle(
            XKCD.MUD, H/2, W, fill_opacity=1, stroke_opacity=0
        ).shift(H/4 * DOWN)

        self.add(bottom_bar)

        # Inicio: matriz superior
        matrix_str = r"\begin{pmatrix} 2 & 3 \\ -1 & 4 \\ 5 & 1 \end{pmatrix}"

        strings = [
            matrix_str,
            r"\begin{pmatrix} x \\ y \end{pmatrix}",
            r"= \begin{pmatrix} 2x + 3y \\ -x + 4y \\ 5x + y \end{pmatrix}",
        ]
        linear_maps = VGroup(*[
            MathTex(*strings[:i], color=XKCD.DARKBROWN).shift(H/4 * UP)
            for i in (1, 2, 3)
        ])
        linear_maps[:2].scale(2.0)
        linear_maps[2].scale(1.45)

        # Inicio: máquina de transformación
        machine = Polygon(
            [3, 0, 0],
            [1, 2, 0],
            [-3, 2, 0],
            [-3, -2, 0],
            [1, -2, 0],
            [3, 0, 0],
            fill_color=XKCD.GREYBROWN,
            fill_opacity=1.0,
            stroke_color=XKCD.BEIGE,
            stroke_opacity=1.0,
        ).scale(0.75).shift(H/4 * DOWN)
        machine.add(
            SingleStringMathTex(
                matrix_str, color=XKCD.BEIGE
            ).scale(1.25).shift(H/4 * DOWN + 0.5 * LEFT)
        )

        self.play(
            FadeIn(linear_maps[0], machine, shift=0.5*DOWN),
            run_time=0.4,
        )

        # 2 columnas - Dimensión de entrada: 2
        two_columns = VGroup(
            Text("2", color=RED_E, font="Noto Sans", weight=HEAVY).scale(1.6),
            Text("columnas", color=XKCD.BRICK, font="Noto Sans"),
            MyArrow(DOWN, color=RED_E).scale(0.3),
        ).arrange_submobjects(DOWN, buff=0.3).next_to(linear_maps[0], UP, buff=0.5)

        upper_subtexts = VGroup(
            *[Text(string, color=XKCD.BRICK, font="Noto Sans").scale(1.1)
            for string in ["n° columnas = dimensión de entrada", "n° filas = dimensión de salida"]]
        ).arrange_submobjects(DOWN, buff=0.35).next_to(linear_maps[0], DOWN, buff=1.35)
        lower_subtexts = upper_subtexts.copy().set_color(RED_A).shift(H/2 * DOWN)

        input_vector = SingleStringMathTex(
            r"\begin{pmatrix} -1 \\ 2 \end{pmatrix}",
            color=XKCD.BEIGE,
        ).scale(1.4).next_to(machine, LEFT, buff=1.4)

        two_d = VGroup(
            Text("vector", color=XKCD.ORANGEISH, font="Noto Sans"),
            Text("2D", color=RED, font="Noto Sans", weight=HEAVY).scale(1.6),
            MyArrow(DOWN, color=RED).scale(0.3),
        ).arrange_submobjects(DOWN, buff=0.3).next_to(input_vector, UP, buff=0.5)

        self.play(
            FadeIn(two_columns, shift=0.5*DOWN),
            run_time=0.35,
        )
        self.wait(0.25)

        self.play(
            LaggedStart(
                AnimationGroup(
                    RT(linear_maps[0][0], linear_maps[1][0]),
                    two_columns.animate.next_to(linear_maps[1][0], UP, buff=0.5),
                ),
                FadeIn(
                    linear_maps[1][1],
                    input_vector,
                    two_d,
                    upper_subtexts[0],
                    lower_subtexts[0],
                    shift=0.5*UP,
                ),
                lag_ratio=0.5,
            ),
            run_time=1.0,
        )
        self.wait(0.7)
        
        # 3 filas - Dimensión de salida: 3
        three_rows = VGroup(
            Text("3", color=RED_E, font="Noto Sans", weight=HEAVY).scale(1.6),
            Text("filas", color=XKCD.BRICK, font="Noto Sans"),
            MyArrow(RIGHT, color=RED_E).scale(0.3),
        ).arrange_submobjects(DOWN, buff=0.3)
        three_rows[2].next_to(three_rows[:2], RIGHT)
        three_rows.next_to(linear_maps[1], LEFT, buff=0.5)

        output_vector = SingleStringMathTex(
            r"\begin{pmatrix} 4 \\ 9 \\ -3 \end{pmatrix}",
            color=XKCD.BEIGE,
        ).scale(1.4).next_to(machine, RIGHT, buff=1.4)

        three_d = VGroup(
            Text("vector", color=XKCD.ORANGEISH, font="Noto Sans"),
            Text("3D", color=RED, font="Noto Sans", weight=HEAVY).scale(1.6),
            MyArrow(DOWN, color=RED).scale(0.3),
        ).arrange_submobjects(DOWN, buff=0.3).next_to(output_vector, UP, buff=0.5)

        self.play(
            FadeIn(three_rows, shift=0.5*RIGHT),
            run_time=0.35,
        )
        self.wait(0.25)

        self.play(
            LaggedStart(
                AnimationGroup(
                    RT(linear_maps[1][:2], linear_maps[2][:2]),
                    two_columns.animate.scale(0.8).next_to(linear_maps[2][0], UP, buff=0.4),
                    three_rows.animate.scale(0.8).next_to(linear_maps[2][0], LEFT, buff=0.4),
                ),
                FadeIn(linear_maps[2][2], shift=0.4 * UP),
                lag_ratio=0.5,
            ),
            run_time=1.0,
        )
        self.play(
            LaggedStart(
                GrowFromPoint(
                    input_vector.copy(),
                    machine.get_left() + 0.2*RIGHT,
                    run_time=0.65,
                    reverse_rate_function=True,
                ),
                GrowFromPoint(output_vector, machine.get_right() + 0.2*LEFT, run_time=0.65),
                FadeIn(three_d, upper_subtexts[1], lower_subtexts[1], shift=0.5*DOWN, run_time=0.5),
                lag_ratio=0.4,
            ),
            run_time=1.0,
        )
        self.wait(1.1)

        # QUITAR TODOS LOS MOBJECTS
        to_remove = list(self.mobjects)
        to_remove.remove(bottom_bar)

        self.play(FadeOut(*to_remove), run_time=0.3)


class LinearMap4(Scene):
    def construct(self):
        self.camera.background_color = XKCD.REDDISHBROWN
        H, W = get_dims(self)
        
        # Preparación
        top_bar = Rectangle(
            XKCD.MAIZE, H/2, W, fill_opacity=1, stroke_opacity=0
        ).shift(H/4 * UP)
        bottom_bar = Rectangle(
            XKCD.MUD, H/2, W, fill_opacity=1, stroke_opacity=0
        ).shift(H/4 * DOWN)
        
        self.add(top_bar, bottom_bar)


        # MOSTRAR AMBAS TRANSFORMACIONES LINEALES
        matrix = r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}"
        x_vector = r"\begin{pmatrix} x \\ y \end{pmatrix}"
        bases = [r"\begin{pmatrix} 1 \\ 0 \end{pmatrix}", r"\begin{pmatrix} 0 \\ 1 \end{pmatrix}"]
        columns = [r"\begin{pmatrix} a \\ c \end{pmatrix}", r"\begin{pmatrix} b \\ d \end{pmatrix}"]
        
        linear_comb = f"x {columns[0]} + y {columns[1]}"
        result_str = r"\begin{pmatrix} ax + by \\ cx + dy \end{pmatrix}"

        column_title = VGroup(
            Text("combinación lineal de", color=XKCD.BRICK, font="Noto Sans").scale(1.3),
            Text("COLUMNAS", color=XKCD.BRICK, font="Noto Sans", weight=HEAVY).scale(2.2),
        ).arrange_submobjects(DOWN)
        row_title = VGroup(
            Text("productos punto con", color=XKCD.BABYBLUE, font="Noto Sans").scale(1.3),
            Text("FILAS", color=BLUE_B, font="Noto Sans", weight=HEAVY).scale(2.2),
        ).arrange_submobjects(DOWN)
        row_title[1].shift(0.15 * UP)

        column_maps = VGroup(
            *[
                MathTex(
                    matrix, vector, "=", result, color=XKCD.DARKBROWN
                ).scale(1.7).shift(H/4 * UP)
                for vector, result in zip(
                    [x_vector, x_vector, x_vector, bases[0], bases[0]],
                    [
                        result_str,
                        r"\begin{pmatrix} ax \\ cx \end{pmatrix} + \begin{pmatrix} by \\ dy \end{pmatrix}",
                        linear_comb,
                        f"1 {columns[0]} + 0 {columns[1]}",
                        columns[0], 
                    ],
                )
            ]
        )
        # Num elems: 12, 13, 11
        column_indices_dict = {
            "a": ([1], [1], [2]),
            "b": ([4], [8], [8]),
            "c": ([6], [3], [3]),
            "d": ([9], [10], [9]),
            "x": ([2, 7], [2, 4], [0]),
            "y": ([5, 10], [9, 11], [6]),
            "(": ([0], [0, 7], [1, 7]),
            ")": ([11], [12, 5], [10, 4]),
            "+": ([3, 8], [6], [5]),
        }
        try:
            column_groups_dict = {
                key: [
                    VGroup(*[column_maps[i][3][j] for j in ind_arr])
                    for i, ind_arr in enumerate(val)
                ]
                for key, val in column_indices_dict.items()
            }
        except:
            for key, val in column_indices_dict.items():
                for i, ind_arr in enumerate(val):
                    for j in ind_arr:
                        try:
                            column_maps[i][3][j]
                        except Exception as e:
                            print(f"DICT['{key}'][{i}] = {ind_arr}, but can't use column_maps[{i}][3][{j}]")
                            raise e

        row_maps = VGroup(
            *[
                MathTex(
                    matrix, x_vector, "=", string, color=XKCD.BEIGE
                ).scale(1.7).shift(H/4 * DOWN)
                for string in (
                    result_str,
                    r"\begin{pmatrix} (a, b) \cdot (x, y) \\ (c, d) \cdot (x, y) \end{pmatrix}",
                )
            ]
        )
        # Num elems: 12, 24
        row_indices_dict = {
            "a": ([1], [2]),
            "b": ([4], [4]),
            "c": ([6], [13]),
            "d": ([9], [15]),
            "x": ([2, 7], [8, 19]),
            "y": ([5, 10], [10, 21]),
            "(": ([0], [0]),
            ")": ([11], [23]),
        }
        row_groups_dict = {
            key: [
                VGroup(*[row_maps[i][3][j] for j in ind_arr])
                for i, ind_arr in enumerate(val)
            ]
            for key, val in row_indices_dict.items()
        }

        self.play(
            FadeIn(column_maps[0], row_maps[0], shift=0.4*RIGHT),
            run_time=0.4,
        )
        self.wait(0.75)

        upper_rects, lower_rects = [VGroup() for _ in range(2)]

        # ANIMACIÓN COMPLEJA DE CAMBIOS DE ESTADO
        for index, maps, title, groups_dict, direction, num_states, to_fade_out, to_fade_in, colors, to_color, rect_group in [
            (0, column_maps, column_title, column_groups_dict, UP, 3, [[], []], [[], []], [RED_E, BLUE_E, GREEN_E], [range(1, 5), range(7, 11), [0, 6]], upper_rects),
            (1, row_maps, row_title, row_groups_dict, DOWN, 2, [[3, 8]], [[1, 3, 5, 6, 7, 9, 11, 12, 14, 16, 17, 18, 20, 22]], [PURPLE_A, TEAL, GREEN], [range(1, 6), range(12, 17), [*range(7, 12), *range(18, 23)]], lower_rects),
        ]:

            for state in range(num_states - 1):
                self.play(
                    RT(maps[state][:3], maps[state+1][:3]),
                    *[
                        Transform(groups[state], groups[state+1])
                        for groups in groups_dict.values()
                    ],
                    (
                        FadeOut(*[maps[state][3][i] for i in to_fade_out[state]])
                        if to_fade_out[state]
                        else Wait()
                    ),
                    (
                        FadeIn(*[maps[state+1][3][i] for i in to_fade_in[state]])
                        if to_fade_in[state]
                        else Wait()
                    ),
                    run_time=0.6,
                )
                self.remove(*[groups[state] for groups in groups_dict.values()])
                self.add(maps[state + 1])

            g00, g01 = (
                VGroup(*[maps[num_states-1][0][i] for i in ((1, 3) if index == 0 else (1, 2))]),
                VGroup(*[maps[num_states-1][3][i] for i in to_color[0]]),
            )
            g10, g11 = (
                VGroup(*[maps[num_states-1][0][i] for i in ((2, 4) if index == 0 else (3, 4))]),
                VGroup(*[maps[num_states-1][3][i] for i in to_color[1]]),
            )
            s00, s01 = [surround(g, colors[0]) for g in (g00, g01)]
            s10, s11 = [surround(g, colors[1]) for g in (g10, g11)]
            self.play(
                LaggedStart(
                    VGroup(
                        maps[num_states-1][1],
                        *[maps[num_states-1][3][i] for i in to_color[2]],
                    ).animate.set_color(colors[2]),
                    AnimationGroup(
                        *[circumscribe(g, colors[0]) for g in (g00, g01)],
                        VGroup(g00, g01).animate.set_color(colors[0]),
                    ),
                    FadeIn(s00, s01),
                    AnimationGroup(
                        *[circumscribe(g, colors[1]) for g in (g10, g11)],
                        VGroup(g10, g11).animate.set_color(colors[1]),
                    ),
                    FadeIn(s10, s11),
                    lag_ratio=0.15,
                ),
                run_time=1.7,
            )
            rect_group.add(s00, s01, s10, s11)

            group = VGroup(maps[num_states-1], rect_group)
            target = group.generate_target()
            VGroup(title, target).arrange_submobjects(DOWN, buff=1.35).move_to(H/4 * direction)
            target.align_to(group, LEFT)
            self.play(
                LaggedStart(
                    MoveToTarget(group),
                    FadeIn(title),
                    lag_ratio=0.25,
                ),
                run_time=0.7,
            )
            self.wait(0.15)

        self.wait(0.6)

        # Preparación
        lower_rects_2 = upper_rects.copy().shift(H/2 * DOWN)
        lower_rects_2[:2].set_color(RED_A)
        lower_rects_2[2:].set_color(BLUE_A)

        # Transformación superior
        column_maps[3:].move_to(column_maps[2])
        VGroup(
            *[column_maps[3][0][i] for i in (1, 3)],
            column_maps[3][1],
            *[column_maps[3][3][i] for i in (0, *range(1, 5), 6)],
            *[column_maps[4][0][i] for i in (1, 3)],
            column_maps[4][1::2],
        ).set_color(RED_E)
        VGroup(
            *[column_maps[3][0][i] for i in (2, 4)],
            *[column_maps[3][3][i] for i in range(7, 11)],
            *[column_maps[4][0][i] for i in (2, 4)],
        ).set_color(BLUE_E)

        base_1_text = VGroup(
            Text("1°", font="Open Sans", weight=HEAVY).scale(1.75),
            Text("vector", font="Open Sans").scale(0.9),
            Text("canónico", font="Open Sans").scale(0.9),
            MyArrow(DOWN).scale(0.3),
        ).set_color(RED_E).arrange_submobjects(DOWN, buff=0.125).next_to(column_maps[4][1], UP, buff=0.4)
        column_1_text = VGroup(
            Text("1°", font="Open Sans", weight=HEAVY).scale(1.75),
            Text("columna", font="Open Sans").scale(0.9),
            MyArrow(DOWN).scale(0.3),
        ).set_color(RED_E).arrange_submobjects(DOWN, buff=0.125).next_to(column_maps[4][3], UP, buff=0.6)
        VGroup(base_1_text[-1], column_1_text[-1]).shift(0.1 * DOWN)

        s00, s01, s10, s11 = upper_rects

        self.play(
            RT(column_maps[2], column_maps[3]),
            *[rect.animate.move_to(
                VGroup(*[column_maps[3][i][j] for j in arr])
            ) for rect, (i, arr) in zip(
                upper_rects,
                [(0, [1, 3]), (3, range(1, 5)), (0, [2, 4]), (3, range(7, 11))],
            )],
            run_rime=0.6,
        )
        self.play(
            LaggedStart(
                FadeOut(
                    column_maps[3][3][0],
                    column_maps[3][3][5:],
                    upper_rects[-1],
                    column_title,
                ),
                AnimationGroup(
                    RT(column_maps[3][:3], column_maps[4][:3]),
                    RT(column_maps[3][3][1:5], column_maps[4][3]),
                    *[rect.animate.move_to(
                        VGroup(*[column_maps[4][i][j] for j in arr])
                    ) for rect, (i, arr) in zip(
                        upper_rects[:3],
                        [(0, [1, 3]), (3, range(4)), (0, [2, 4])],
                    )] 
                ),
                FadeIn(base_1_text, column_1_text, shift=0.5*DOWN),
                lag_ratio=0.25,
            ),
            run_time=1.0,
        )
        self.wait(0.5)

        # Transformación inferior
        column_maps_2 = VGroup(
            *[
                MathTex(
                    matrix, vector, "=", result, color=XKCD.BEIGE
                ).scale(1.7).move_to(row_maps[-1])
                for vector, result in zip(
                    (x_vector, bases[1], bases[1]),
                    (
                        linear_comb,
                        f"0 {columns[0]} + 1 {columns[1]}",
                        columns[1],
                    ),
                )
            ]
        )
        VGroup(
            *[column_maps_2[0][0][i] for i in (1, 3)],
            *[column_maps_2[0][3][i] for i in range(1, 5)],

            *[column_maps_2[1][0][i] for i in (1, 3)],
            *[column_maps_2[1][3][i] for i in range(1, 5)],

            *[column_maps_2[2][0][i] for i in (1, 3)],
        ).set_color(RED_B)

        VGroup(
            *[column_maps_2[0][0][i] for i in (2, 4)],
            *[column_maps_2[0][3][i] for i in range(7, 11)],

            *[column_maps_2[1][0][i] for i in (2, 4)],
            column_maps_2[1][1],
            *[column_maps_2[1][3][i] for i in (0, 6, *range(7, 11))],

            *[column_maps_2[2][0][i] for i in (2, 4)],
            column_maps_2[2][1::2],
        ).set_color(BLUE_B)

        VGroup(
            column_maps_2[0][1],
            column_maps_2[0][3][::6],
        ).set_color(GREEN)

        column_title_2 = column_title.copy().move_to(row_title).set_color(RED_B)

        base_2_text = VGroup(
            Text("2°", font="Open Sans", weight=HEAVY).scale(1.75),
            Text("vector", font="Open Sans").scale(0.9),
            Text("canónico", font="Open Sans").scale(0.9),
            MyArrow(DOWN).scale(0.3),
        ).set_color(BLUE_B).arrange_submobjects(DOWN, buff=0.125).next_to(column_maps_2[2][1], UP, buff=0.4)
        column_2_text = VGroup(
            Text("2°", font="Open Sans", weight=HEAVY).scale(1.75),
            Text("columna", font="Open Sans").scale(0.9),
            MyArrow(DOWN).scale(0.3),
        ).set_color(BLUE_B).arrange_submobjects(DOWN, buff=0.125).next_to(column_maps_2[2][3], UP, buff=0.6)
        VGroup(base_2_text[-1], column_2_text[-1]).shift(0.1 * DOWN)

        self.play(
            LaggedStart(
                FadeOut(row_maps[-1], row_title, lower_rects, shift=0.5*UP),
                FadeIn(column_maps_2[0], column_title_2, lower_rects_2, shift=0.5 * UP),
                lag_ratio=0.5,
            ),
            run_time=0.5,
        )
        
        self.play(
            RT(column_maps_2[0], column_maps_2[1]),
            *[rect.animate.move_to(
                VGroup(*[column_maps_2[1][i][j] for j in arr])
            ) for rect, (i, arr) in zip(
                lower_rects_2,
                [(0, [1, 3]), (3, range(1, 5)), (0, [2, 4]), (3, range(7, 11))],
            )],
            run_rime=0.6,
        )

        self.play(
            LaggedStart(
                FadeOut(
                    column_maps_2[1][3][:7],
                    lower_rects_2[1],
                    column_title_2,
                ),
                AnimationGroup(
                    RT(column_maps_2[1][:3], column_maps_2[2][:3]),
                    RT(column_maps_2[1][3][7:11], column_maps_2[2][3]),
                    *[rect.animate.move_to(
                        VGroup(*[column_maps_2[2][i][j] for j in arr])
                    ) for rect, (i, arr) in zip(
                        [lower_rects_2[r] for r in (0, 2, 3)],
                        [(0, [1, 3]), (0, [2, 4]), (3, range(4))],
                    )] 
                ),
                FadeIn(base_2_text, column_2_text, shift=0.5*DOWN),
                lag_ratio=0.3,
            ),
            run_time=1.0,
        )
        self.wait(0.8)

        g1 = VGroup(column_maps[-1], upper_rects[:3], base_1_text, column_1_text)
        g2 = VGroup(column_maps_2[-1], lower_rects_2[0], lower_rects_2[2:], base_2_text, column_2_text)

        inner_matrix = SingleStringMathTex(
            r"\begin{pmatrix} 2 & -1 \\ 1 & 1 \end{pmatrix}",
            color=XKCD.MAIZE,
        ).scale(3.0).set_z_index(-1)
        VGroup(*[inner_matrix[i] for i in (1, 4)]).set_color(RED_B)
        VGroup(*[inner_matrix[i] for i in (2, 3, 5)]).set_color(BLUE_B)

        my_axes = lambda: Axes(
            x_range=[-1, 2], y_range=[-1, 1.5], x_length=3.0, y_length=2.5,
            axis_config={"include_ticks": False, "include_tip": False},
        )

        text_1 = VGroup(
            my_axes(),
            SingleStringMathTex(r"\begin{pmatrix} 1 \\ 0 \end{pmatrix}").scale(1.6),
            Text("se", font="Open Sans").scale(0.9),
            Text("vuelve", font="Open Sans").scale(0.9),
            SingleStringMathTex(r"\begin{pmatrix} 2 \\ 1 \end{pmatrix}").scale(1.6),
            my_axes(),
        ).arrange_submobjects(DOWN, buff=0.425)
        ax1, ax2 = text_1[0], text_1[-1]
        ax1.add(Arrow(ax1.c2p(0), ax1.c2p([RIGHT]), buff=0.0))
        ax2.add(Arrow(ax2.c2p(0), ax2.c2p([[2, 1, 0]]), buff=0.0))
        text_1[3:].shift(0.3 * UP)
        text_1[1:-1].set_color(RED_B)
        text_1.add(MyArrow(RIGHT, color=RED_B).scale(0.3).next_to(text_1[1:-1], RIGHT, buff=0.4))
        text_1.next_to(inner_matrix, LEFT, buff=0.5)
        ax1[-1].set_color(RED)
        ax2[-1].set_color(RED)

        text_2 = VGroup(
            my_axes(),
            SingleStringMathTex(r"\begin{pmatrix} 0 \\ 1 \end{pmatrix}").scale(1.5),
            Text("se", font="Open Sans").scale(0.9),
            Text("vuelve", font="Open Sans").scale(0.9),
            SingleStringMathTex(r"\begin{pmatrix} -1 \\ 1 \end{pmatrix}").scale(1.5),
            my_axes(),
        ).arrange_submobjects(DOWN, buff=0.475)
        ax1, ax2 = text_2[0], text_2[-1]
        ax1.add(Arrow(ax1.c2p(0), ax1.c2p([UP]), buff=0.0))
        ax2.add(Arrow(ax2.c2p(0), ax2.c2p([[-1, 1, 0]]), buff=0.0))
        text_2[3:].shift(0.35 * UP)
        text_2[1:-1].set_color(BLUE_B)
        text_2.add(MyArrow(LEFT, color=BLUE_B).scale(0.3).next_to(text_2[1:-1], LEFT, buff=0.4))
        text_2.next_to(inner_matrix, RIGHT, buff=0.5)
        ax1[-1].set_color(BLUE)
        ax2[-1].set_color(BLUE) 

        self.add(inner_matrix)

        self.play(
            top_bar.animate.shift(H/4 * UP),
            bottom_bar.animate.shift(H/4 * DOWN),
            g1.animate.shift((3*H/8 - g1.get_center()[1]) * UP),
            g2.animate.shift((3*H/8 + g2.get_center()[1]) * DOWN),
            run_time=0.7,
        )
        self.wait(0.2)
        
        self.play(
            LaggedStart(
                FadeIn(text_1, shift=0.5*RIGHT),
                FadeIn(text_2, shift=0.5*LEFT),
                lag_ratio=0.75,
            ),
            run_time=0.8,
        )

        self.wait()

        self.play(
            VGroup(top_bar, g1).animate.shift(H/4 * UP),
            VGroup(bottom_bar, g2).animate.shift(H/4 * DOWN),
            VGroup(inner_matrix, text_1, text_2).animate.shift((H/4 - 1) * UP),
            run_time=0.8,
        )

        
        my_axes = lambda: Axes(
            x_range=[-1, 2], y_range=[-1, 2.0], x_length=5.0, y_length=5.0,
            axis_config={"include_ticks": False, "include_tip": False},
        )

        ax1, ax2 = my_axes(), my_axes()

        for ax, coords, colors in [
            (ax1, [RIGHT, UP, UR], [RED, BLUE, GREEN_B]), 
            (ax2, [2*RIGHT + UP, UL, RIGHT + 2*UP], [RED, BLUE, GREEN_B]),
        ]:
            for coord, color in zip(coords, colors):
                ax.add(Arrow(ax.c2p(0), ax.c2p([coord]), buff=0.0, color=color))
            for i in 0, 1:
                ax.add(DashedLine(ax.c2p([coords[i]]), ax.c2p([coords[2]]), color=colors[1-i]))

        arrow_ax, arrow_vec = [Vector(RIGHT).scale(1.65) for _ in range(2)]
        group = VGroup(
            ax1, arrow_ax, ax2
        ).arrange_submobjects(RIGHT, buff=0.6).shift(8*DOWN)

        xy = SingleStringMathTex(x_vector, color=GREEN_B).scale(1.6).next_to(ax1, UP, buff=1.0)
        xb1_yb2 = MathTex("x", bases[0], "+", "y", bases[1]).scale(1.6).move_to(xy)
        xc1_yc2 = MathTex("x", r"\begin{pmatrix} 2 \\ 1 \end{pmatrix}", "+", "y", r"\begin{pmatrix} -1 \\ 1 \end{pmatrix}").scale(1.6).next_to(ax2, UP, buff=1.0)
        VGroup(xb1_yb2[1], xc1_yc2[1]).set_color(RED)
        VGroup(xb1_yb2[4], xc1_yc2[4]).set_color(BLUE)
        VGroup(xb1_yb2[::3], xc1_yc2[::3]).set_color(GREEN_B)

        arrow_vec.move_to([arrow_ax.get_center()[0], xy.get_center()[1], 0])

        self.play(
            FadeIn(ax1, xy, shift=0.5*UP),
            run_time=0.4,
        )
        self.wait(1.2)
        self.play(RT(xy, xb1_yb2), run_time=0.75)
        self.wait()

        self.play(
            LaggedStart(
                AnimationGroup(
                    RT(ax1.copy(), ax2),
                    RT(xb1_yb2.copy(), xc1_yc2),
                ),
                AnimationGroup(
                    *[GrowArrow(arrow, shift=0.5*RIGHT, run_time=0.65) for arrow in (arrow_ax, arrow_vec)],
                ),
                lag_ratio=0.4,
            ),
            run_time=1.2,
        )
        self.wait(1.8)

        self.add(inner_matrix) # weird behavior if we don't use this
        to_remove = list(self.mobjects)
        to_remove.remove(inner_matrix)

        plane = NumberPlane(
            x_range=[-2.88, 2.88], y_range=[-6.48, 6.48], x_length=4*3.6, y_length=9*3.6,
            background_line_style={"stroke_color": XKCD.ORANGEISH}
        )
        colors = [RED, BLUE, GREEN_B]
        directions = [UR, UL, UR]
        vectors = VGroup(*[
            Vector(plane.c2p([coords]), color=color)
            for coords, color in zip(
                [[1, 0], [0, 1], [1, 1], [2, 1], [-1, 1], [1, 2]],
                colors + colors,
            )
        ])
        labels = VGroup(*[
            MathTex(string, color=color).scale(1.5).next_to(vec, direction)
            for string, color, vec, direction in zip(
                [
                    r"\begin{pmatrix} 1 \\ 0 \end{pmatrix}",
                    r"\begin{pmatrix} 0 \\ 1 \end{pmatrix}",
                    r"\begin{pmatrix} x \\ y \end{pmatrix}",
                    r"\begin{pmatrix} 2 \\ 1 \end{pmatrix}",
                    r"\begin{pmatrix} -1 \\ 1 \end{pmatrix}",
                    r"x \begin{pmatrix} 2 \\ 1 \end{pmatrix} + y \begin{pmatrix} -1 \\ 1 \end{pmatrix}",
                ],
                colors + colors,
                vectors,
                directions + directions,
            )
        ])
        labels[-1].shift(2.3*LEFT)
        for label in labels:
            label.insert(0, surround(label, XKCD.REDDISHBROWN))

        start_vectors, end_vectors = vectors[:3], vectors[3:]
        start_labels, end_labels = labels[:3], labels[3:]

        inner_matrix.set_z_index(0).insert(0, surround(inner_matrix, XKCD.REDDISHBROWN))

        self.play(
            Succession(
                AnimationGroup(
                    inner_matrix.animate.move_to(4.0 * DOWN),
                    run_time=1.5,
                ),
                Wait(0.6),
                run_time=2.1,
            ),
            Succession(
                FadeOut(*to_remove, run_time=0.75),
                LaggedStart(
                    DrawBorderThenFill(plane),
                    AnimationGroup(*[GrowArrow(v) for v in start_vectors]),
                    FadeIn(start_labels, shift=0.5*UP),
                    lag_ratio=0.125,
                    run_time=1.35,
                ),
                run_time=2.1,
            ),
            run_time=1.9,
        )

        top_bar, bottom_bar = [
            Rectangle(
                XKCD.DARKBROWN, height=H/5, width=W, fill_opacity=1.0, stroke_opacity=0.0
            ).shift((1/2 + 3/10) * H * direction)
            for direction in [UP, DOWN]
        ]

        top_text = VGroup(
            Text("Las", color=XKCD.BEIGE, font="Open Sans").scale(1.75),
            Text("MATRICES", color=RED_B, font="Open Sans", weight=HEAVY).scale(2.75),
        )
        top_text.arrange_submobjects(DOWN).move_to(top_bar)
        top_text[0].shift(0.25 * UP)
        top_bar.add(top_text)

        bottom_text = VGroup(
            Text("representan", color=XKCD.BEIGE, font="Open Sans").scale(1.5),
            Text("TRANSFORMACIONES", color=BLUE_B, font="Open Sans", weight=HEAVY).scale(1.75),
            Text("LINEALES", color=BLUE_B, font="Open Sans", weight=HEAVY).scale(1.75),
        )
        bottom_text.arrange_submobjects(DOWN).move_to(bottom_bar)
        bottom_bar.add(bottom_text)

        back_plane = plane.copy().set_opacity(0.2)
        self.add(back_plane)

        self.play(
            plane.animate.apply_matrix(np.array([[2, -1], [1, 1]])),
            Transform(start_vectors, end_vectors),
            Transform(start_labels, end_labels),
            top_bar.animate.shift(2*H/5 * DOWN),
            bottom_bar.animate.shift(2*H/5 * UP),
            run_time=1.25,
        )
        self.wait(1.2)

        R = 0.5 * np.sqrt(H*H + W*W)
        circle_stroke = Circle(R, color=XKCD.MAIZE)
        circle_fill = Circle(R, color=XKCD.MAIZE, fill_opacity=1.0, stroke_opacity=1.0)

        self.play(
            GrowFromPoint(circle_stroke, ORIGIN, rate_func=linear),
            GrowFromPoint(circle_fill, ORIGIN, rate_func=rush_into),
            run_time=0.65,
        )



if __name__ == "__main__":
    scenes = [LinearMap0, LinearMap1, LinearMap2, LinearMap3, LinearMap4]
    for i in [4]:
        render(scenes[i])