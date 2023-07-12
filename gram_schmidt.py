from manim import *
import numpy as np


class Vector3D(Arrow3D):
    def __init__(self, axes, end, **kwargs):
        super().__init__(axes.c2p(0, 0, 0), axes.c2p(*end), resolution=[1, 8], **kwargs)


class PolygonFromVectors(Polygon):
    def __init__(self, axes, _v1, _v2, **kwargs):
        super().__init__(
            axes.c2p(0, 0, 0), axes.c2p(*_v1), axes.c2p(*(_v1+_v2)), axes.c2p(*_v2),
            **kwargs
        )


class MyPlane(PolygonFromVectors):
    def __init__(self, axes, _v1, _v2, stroke_width=0.5, fill_opacity=0.15, **kwargs):
        super().__init__(
            axes, _v1, _v2,
            stroke_width=stroke_width, fill_opacity=fill_opacity,
            **kwargs
        )


class MyElbow(PolygonFromVectors):
    def __init__(self, axes, _v1, _v2, stroke_width=2, fill_opacity=0.4, **kwargs):
        super().__init__(
            axes, _v1/(5*np.linalg.norm(_v1)), _v2/(5*np.linalg.norm(_v2)),
            stroke_width=stroke_width, fill_opacity=fill_opacity,
            **kwargs
        )


class GramSchmidt(ThreeDScene):
    def rotate(self, mob, **kwargs):
        rot_matrix = self.camera.generate_rotation_matrix()
        #self.camera.add_fixed_orientation_mobjects(mob)
        mob.apply_points_function_about_point(
            lambda points: np.dot(points, rot_matrix), mob.get_center(), **kwargs
        )
        return mob

    def construct(self):
        self.camera.background_color = GRAY_E

        _u = np.array([1.5, -1, 1.5])
        _v = np.array([-1, 2, 1])
        _w = np.array([-0.5, -1, 2])

        _q1 = _u / np.linalg.norm(_u)

        _proj_q1_v = np.dot(_v, _q1) * _q1
        _v1 = _v - _proj_q1_v
        _q2 = _v1 / np.linalg.norm(_v1)

        _proj_q1_w = np.dot(_w, _q1) * _q1
        _proj_q2_w = np.dot(_w, _q2) * _q2
        _w1 = _w - _proj_q1_w
        _w2 = _w1 - _proj_q2_w
        _q3 = _w2 / np.linalg.norm(_w2)

        axes = ThreeDAxes(num_axis_pieces=1).scale(2.5).shift(3*IN)

        u  = Vector3D(axes, _u,  color=RED_A)
        q1 = Vector3D(axes, _q1, color=RED_A)
        v  = Vector3D(axes, _v,  color=GREEN_A)
        v1 = Vector3D(axes, _v1, color=GREEN_A)
        q2 = Vector3D(axes, _q2, color=GREEN_A)
        w  = Vector3D(axes, _w,  color=BLUE_A)
        w1 = Vector3D(axes, _w1, color=BLUE_A)
        w2 = Vector3D(axes, _w2, color=BLUE_A)
        q3 = Vector3D(axes, _q3, color=BLUE_A)

        OU = OUT+UP
        OD = OUT+DOWN

        u_label  = MathTex(r"{{ \bold{u} }}",                                                                              color=RED_A  ).next_to(u[-1],  OD)
        u1_label = MathTex(r"{{ \bold{u} }} \over {{ r_{11} }}",                                                                        ).next_to(q1[-1], OD)
        q1_label = MathTex(r"\bold{q}_1",                                                                                  color=RED_D  ).next_to(q1[-1], OD)
        v_label  = MathTex(r"{{ \bold{v} }}",                                                                              color=GREEN_A).next_to(v[-1],  OU)
        v1_label = MathTex(r"{{ \bold{v} }} - {{ r_{12} }}{{\bold{q}_1}}",                                                              ).next_to(v1[-1], OU)
        v2_label = MathTex(r"{{ \bold{v} }} - {{ r_{12} }}{{\bold{q}_1}} \over {{ r_{22} }}",                                           ).next_to(q2[-1], OU)
        q2_label = MathTex(r"\bold{q}_2",                                                                                  color=GREEN_D).next_to(q2[-1], OU)
        w_label  = MathTex(r"{{ \bold{w} }}",                                                                              color=BLUE_A ).next_to(w[-1],  OD)
        w1_label = MathTex(r"{{ \bold{w} }} - {{ r_{13} }}{{\bold{q}_1}}",                                                              ).next_to(w1[-1], OD)
        w2_label = MathTex(r"{{ \bold{w} }} - {{ r_{13} }}{{\bold{q}_1}} - {{ r_{23} }}{{\bold{q}_2}}",                                 ).next_to(w2[-1], OD)
        w3_label = MathTex(r"{{ \bold{w} }} - {{ r_{13} }}{{\bold{q}_1}} - {{ r_{23} }}{{\bold{q}_2}} \over {{ r_{33} }}",              ).next_to(q3[-1], OD)
        q3_label = MathTex(r"\bold{q}_3",                                                                                  color=BLUE_D ).next_to(q3[-1], OD)

        u_text_0 = MathTex(r"{ {{ \bold{u} }} \over {{ r_{11} }} } = {{\bold{q}_1}}")
        u_text_f  = MathTex(r"{{ \bold{u} }} = {{ r_{11} }}{{\bold{q}_1}} + {{ 0 }}{{\bold{q}_2}} + {{ 0 }}{{\bold{q}_3}}")
        u_text_f[4:].set_opacity(0)
        v_text_0 = MathTex(r"{ {{ \bold{v} }} - {{ r_{12} }}{{\bold{q}_1}} \over {{ r_{22} }} } = {{\bold{q}_2}}")
        v_text_1 = MathTex(r"{{ \bold{v} }} - {{ r_{12} }}{{\bold{q}_1}} = {{ r_{22} }}{{\bold{q}_2}}")
        v_text_f = MathTex(r"{{ \bold{v} }} = {{ r_{12} }}{{\bold{q}_1}} + {{ r_{22} }}{{\bold{q}_2}} + {{ 0 }}{{\bold{q}_3}}")
        v_text_f[7:].set_opacity(0)
        w_text_0 = MathTex(r"{ {{ \bold{w} }} - {{ r_{13} }}{{\bold{q}_1}} - {{ r_{23} }}{{\bold{q}_2}} \over {{ r_{33} }} } = {{\bold{q}_3}}")
        w_text_1 = MathTex(r"{{ \bold{w} }} - {{ r_{13} }}{{\bold{q}_1}} - {{ r_{23} }}{{\bold{q}_2}} = {{ r_{33} }}{{\bold{q}_3}}")
        w_text_f = MathTex(r"{{ \bold{w} }} = {{ r_{13} }}{{\bold{q}_1}} + {{ r_{23} }}{{\bold{q}_2}} + {{ r_{33} }}{{\bold{q}_3}}")

        u_text_matrix = MathTex(r"{{ \bold{u} }} = {{\Bigg(}} {{\bold{q}_1}} \ {{\bold{q}_2}} \ {{\bold{q}_3}} {{\Bigg)}} \begin{pmatrix} \quad \\ \quad \\ \quad \end{pmatrix} {{ r_{11} }} {{ 0 }} {{ 0 }}")
        u_text_matrix[14].move_to(u_text_matrix[11]).shift(0.05*UP)
        u_text_matrix[12].next_to(u_text_matrix[14], UP).shift(0.1*DOWN)
        u_text_matrix[16].next_to(u_text_matrix[14], DOWN).shift(0.05*UP)
        v_text_matrix = MathTex(r"{{ \bold{v} }} = {{\Bigg(}} {{\bold{q}_1}} \ {{\bold{q}_2}} \ {{\bold{q}_3}} {{\Bigg)}} \begin{pmatrix} \quad \\ \quad \\ \quad \end{pmatrix} {{ r_{12} }} {{ r_{22} }} {{ 0 }}")
        v_text_matrix[14].move_to(v_text_matrix[11]).shift(0.05*DOWN)
        v_text_matrix[12].next_to(v_text_matrix[14], UP)
        v_text_matrix[16].next_to(v_text_matrix[14], DOWN).shift(0.05*UP)
        w_text_matrix = MathTex(r"{{ \bold{w} }} = {{\Bigg(}} {{\bold{q}_1}} \ {{\bold{q}_2}} \ {{\bold{q}_3}} {{\Bigg)}} \begin{pmatrix} \quad \\ \quad \\ \quad \end{pmatrix} {{ r_{13} }} {{ r_{23} }} {{ r_{33} }}")
        w_text_matrix[14].move_to(w_text_matrix[11]).shift(0.05*DOWN)
        w_text_matrix[12].next_to(w_text_matrix[14], UP)
        w_text_matrix[16].next_to(w_text_matrix[14], DOWN)

        u_text_matrix_2 = MathTex(r"{{ \bold{u} }} = {{Q}} \begin{pmatrix} \quad \\ \quad \\ \quad \end{pmatrix} {{ r_{11} }} {{ 0 }} {{ 0 }}")
        u_text_matrix_2[6].move_to(u_text_matrix_2[3]).shift(0.05*UP)
        u_text_matrix_2[4].next_to(u_text_matrix_2[6], UP).shift(0.1*DOWN)
        u_text_matrix_2[8].next_to(u_text_matrix_2[6], DOWN).shift(0.05*UP)
        v_text_matrix_2 = MathTex(r"{{ \bold{v} }} = {{Q}} \begin{pmatrix} \quad \\ \quad \\ \quad \end{pmatrix} {{ r_{12} }} {{ r_{22} }} {{ 0 }}")
        v_text_matrix_2[6].move_to(v_text_matrix_2[3]).shift(0.05*DOWN)
        v_text_matrix_2[4].next_to(v_text_matrix_2[6], UP)
        v_text_matrix_2[8].next_to(v_text_matrix_2[6], DOWN).shift(0.05*UP)
        w_text_matrix_2 = MathTex(r"{{ \bold{w} }} = {{Q}} \begin{pmatrix} \quad \\ \quad \\ \quad \end{pmatrix} {{ r_{13} }} {{ r_{23} }} {{ r_{33} }}")
        w_text_matrix_2[6].move_to(w_text_matrix_2[3]).shift(0.05*DOWN)
        w_text_matrix_2[4].next_to(w_text_matrix_2[6], UP)
        w_text_matrix_2[8].next_to(w_text_matrix_2[6], DOWN)
        
        uvw_text_1 = MathTex(
            r"{{\Bigg(}} {{ \bold{u} }} \ {{ \bold{v} }} \ {{ \bold{w} }} {{\Bigg)}}"
            r"= {{\Bigg(}} {{Q}}{{ \begin{pmatrix} \quad \\ \quad \\ \quad \end{pmatrix} }} \ {{Q}}{{ \begin{pmatrix} \quad \\ \quad \\ \quad \end{pmatrix} }} \ {{Q}}{{ \begin{pmatrix} \quad \\ \quad \\ \quad \end{pmatrix} }}{{\Bigg)}}"
            r"{{ r_{11} }} {{ 0 }} {{ 0 }} {{ r_{12} }} {{ r_{22} }} {{ 0 }} {{ r_{13} }} {{ r_{23} }} {{ r_{33} }}"
        )
        uvw_text_1[23].move_to(uvw_text_1[13]).shift(0.05*UP)
        uvw_text_1[21].next_to(uvw_text_1[23], UP).shift(0.1*DOWN)
        uvw_text_1[25].next_to(uvw_text_1[23], DOWN).shift(0.05*UP)
        uvw_text_1[29].move_to(uvw_text_1[16])
        uvw_text_1[27].next_to(uvw_text_1[29], UP)
        uvw_text_1[31].next_to(uvw_text_1[29], DOWN).shift(0.05*UP)
        uvw_text_1[35].move_to(uvw_text_1[19])
        uvw_text_1[33].next_to(uvw_text_1[35], UP)
        uvw_text_1[37].next_to(uvw_text_1[35], DOWN)
        for i in (22, 24, 26, 28, 30, 32, 34, 36):
            uvw_text_1[i].move_to(uvw_text_1)
        uvw_text_1.move_to(ORIGIN)

        uvw_text_2 = MathTex(
            r"{{\Bigg(}} {{ \bold{u} }} \ {{ \bold{v} }} \ {{ \bold{w} }} {{\Bigg)}}"
            r"= {{Q}}"
            r"{{\Bigg(}} {{ \begin{pmatrix} \quad \\ \quad \\ \quad \end{pmatrix} }} \ {{ \begin{pmatrix} \quad \\ \quad \\ \quad \end{pmatrix} }} \ {{ \begin{pmatrix} \quad \\ \quad \\ \quad \end{pmatrix} }} {{\Bigg)}}"
            r"{{ r_{11} }} {{ 0 }} {{ 0 }} {{ r_{12} }} {{ r_{22} }} {{ 0 }} {{ r_{13} }} {{ r_{23} }} {{ r_{33} }}"
        )
        uvw_text_2[22].move_to(uvw_text_2[13]).shift(0.05*UP)
        uvw_text_2[20].next_to(uvw_text_2[22], UP).shift(0.1*DOWN)
        uvw_text_2[24].next_to(uvw_text_2[22], DOWN).shift(0.05*UP)
        uvw_text_2[28].move_to(uvw_text_2[15])
        uvw_text_2[26].next_to(uvw_text_2[28], UP)
        uvw_text_2[30].next_to(uvw_text_2[28], DOWN).shift(0.05*UP)
        uvw_text_2[34].move_to(uvw_text_2[17])
        uvw_text_2[32].next_to(uvw_text_2[34], UP)
        uvw_text_2[36].next_to(uvw_text_2[34], DOWN)
        for i in (18, 21, 23, 25, 27, 29, 31, 33, 35):
            uvw_text_2[i].move_to(uvw_text_2)
        uvw_text_2.move_to(ORIGIN)

        uvw_text_3 = MathTex(
            r"{{\Bigg(}} {{ \bold{u} }} \ {{ \bold{v} }} \ {{ \bold{w} }} {{\Bigg)}}"
            r"= {{Q}}"
            r"\begin{pmatrix} \quad & \quad & \quad \\ \quad & \quad & \quad \\ \quad & \quad & \quad \end{pmatrix}"
            r"{{ r_{11} }} {{ 0 }} {{ 0 }} {{ r_{12} }} {{ r_{22} }} {{ 0 }} {{ r_{13} }} {{ r_{23} }} {{ r_{33} }}"
        )
        uvw_text_3[20].move_to(uvw_text_3[11]).shift(0.05*DOWN)
        uvw_text_3[12].next_to(uvw_text_3[20], UL)
        uvw_text_3[14].next_to(uvw_text_3[12], DOWN).shift(0.1*UP)
        uvw_text_3[16].next_to(uvw_text_3[14], DOWN).shift(0.05*UP)
        uvw_text_3[18].next_to(uvw_text_3[20], UP)
        uvw_text_3[22].next_to(uvw_text_3[20], DOWN).shift(0.1*UP)
        uvw_text_3[24].next_to(uvw_text_3[20], UR)
        uvw_text_3[26].next_to(uvw_text_3[20], RIGHT)
        uvw_text_3[28].next_to(uvw_text_3[20], DR)
        for i in (13, 15, 17, 19, 21, 23, 25, 27):
            uvw_text_3[i].move_to(uvw_text_3)
        uvw_text_3.move_to(ORIGIN)

        uvw_text_4 = MathTex(
            r"{{\Bigg(}} {{ \bold{u} }} \ {{ \bold{v} }} \ {{ \bold{w} }} {{\Bigg)}}"
            r"= {{\Bigg(}} {{\bold{q}_1}} \ {{\bold{q}_2}} \ {{\bold{q}_3}} {{\Bigg)}}"
            r"\begin{pmatrix} \quad & \quad & \quad \\ \quad & \quad & \quad \\ \quad & \quad & \quad \end{pmatrix}"
            r"{{ r_{11} }} {{ 0 }} {{ 0 }} {{ r_{12} }} {{ r_{22} }} {{ 0 }} {{ r_{13} }} {{ r_{23} }} {{ r_{33} }}"
        )
        uvw_text_4[28].move_to(uvw_text_4[19]).shift(0.05*DOWN)
        uvw_text_4[20].next_to(uvw_text_4[28], UL)
        uvw_text_4[22].next_to(uvw_text_4[20], DOWN).shift(0.1*UP)
        uvw_text_4[24].next_to(uvw_text_4[22], DOWN).shift(0.05*UP)
        uvw_text_4[26].next_to(uvw_text_4[28], UP)
        uvw_text_4[30].next_to(uvw_text_4[28], DOWN).shift(0.1*UP)
        uvw_text_4[32].next_to(uvw_text_4[28], UR)
        uvw_text_4[34].next_to(uvw_text_4[28], RIGHT)
        uvw_text_4[36].next_to(uvw_text_4[28], DR)
        for i in (21, 23, 25, 27, 29, 31, 33, 35):
            uvw_text_4[i].move_to(uvw_text_4)
        uvw_text_4.move_to(ORIGIN)

        r11_text = MathTex(r"{{ r_{11} }} = \lVert {{ \bold{u} }} \rVert")
        r12_text = MathTex(r"{{ r_{12} }} = {{ \bold{q}_1 }} \cdot {{ \bold{v} }}")
        r22_text = MathTex(r"{{ r_{22} }} = \lVert {{ \bold{v} }} - {{ r_{12} }}{{\bold{q}_1}} \rVert")
        r13_text = MathTex(r"{{ r_{13} }} = {{ \bold{q}_1 }} \cdot {{ \bold{w} }}")
        r23_text = MathTex(r"{{ r_{23} }} = {{ \bold{q}_2 }} \cdot {{ \bold{w} }}")
        r33_text = MathTex(r"{{ r_{33} }} = \lVert {{ \bold{w} }} - {{ r_{13} }}{{\bold{q}_1}} - {{ r_{23} }}{{\bold{q}_2}} \rVert")

        title = Paragraph("Ortonormalización", "de Gram-Schmidt", color=YELLOW, alignment="center").scale(1.5)

        u_time = MathTex(r"{{ \bold{u} }} \rightarrow {{\bold{q}_1}}").scale(1.25)
        u_step_1 = Tex(r"{{(1)}} Normalizar {{$\bold{u}$}} \\ (dividiendo por su norma)").scale(0.75)
        u_step_1[3:].align_to(u_step_1[1], LEFT)

        v_time = MathTex(r"{{ \bold{v} }} \rightarrow {{\bold{q}_2}}").scale(1.25)
        v_step_1 = Tex(r"{{(1)}} Ortogonalizar {{$\bold{v}$}} \\ respecto de {{$\bold{q}_1$}} \\ (restando su \\ {{proyección sobre }}{{$\bold{q}_1$}})").scale(0.75)
        v_step_1[3:5].align_to(v_step_1[1], LEFT)
        v_step_1[5].align_to(v_step_1[1], LEFT)
        v_step_1[6:].align_to(v_step_1[1], LEFT)
        v_step_2 = Tex(r"{{(2)}} Normalizar el resultado \\ {{de }}{{(1)}}{{ (dividiendo}} \\ por su norma)").scale(0.75)
        v_step_2[2:5].align_to(v_step_2[1], LEFT)
        v_step_2[5].align_to(v_step_2[1], LEFT)

        w_time = MathTex(r"{{ \bold{w} }} \rightarrow {{\bold{q}_3}}").scale(1.25)
        w_step_1 = Tex(r"{{(1)}} Ortogonalizar {{$\bold{w}$}} \\ respecto de {{$\bold{q}_1$}} \\ (restando su \\ {{proyección sobre }}{{$\bold{q}_1$}})").scale(0.75)
        w_step_1[3:5].align_to(w_step_1[1], LEFT)
        w_step_1[5].align_to(w_step_1[1], LEFT)
        w_step_1[6:].align_to(w_step_1[1], LEFT)
        w_step_2 = Tex(r"{{(2)}} Ortogonalizar el \\ {{resultado de }}{{(1)}} \\ respecto de {{$\bold{q}_2$}} \\ (restando su \\ {{proyección sobre }}{{$\bold{q}_2$}})").scale(0.75)
        w_step_2[2:4].align_to(w_step_2[1], LEFT)
        w_step_2[4:6].align_to(w_step_2[1], LEFT)
        w_step_2[6].align_to(w_step_2[1], LEFT)
        w_step_2[7:].align_to(w_step_2[1], LEFT)
        w_step_3 = Tex(r"{{(3)}} Normalizar el resultado \\ {{de }}{{(2)}}{{ (dividiendo}} \\ por su norma)").scale(0.75)
        w_step_3[2:5].align_to(w_step_3[1], LEFT)
        w_step_3[5].align_to(w_step_3[1], LEFT)

        for label in (
            u1_label,
            v1_label, v2_label,
            w1_label, w2_label, w3_label,
            u_text_0, u_text_f,
            v_text_0, v_text_1, v_text_f,
            w_text_0, w_text_1, w_text_f,
            u_text_matrix, v_text_matrix, w_text_matrix,
            u_text_matrix_2, v_text_matrix_2, w_text_matrix_2,
            uvw_text_1, uvw_text_2, uvw_text_3, uvw_text_4,
            r11_text,
            r12_text, r22_text,
            r13_text, r23_text, r33_text,  
            u_time, u_step_1,
            v_time, v_step_1, v_step_2,
            w_time, w_step_1, w_step_2, w_step_3,
        ):
            for tex, color in (
                (r"\bold{u}", RED_A), (r"\bold{v}", GREEN_A), (r"\bold{w}", BLUE_A),
                (r"\bold{q}_1", RED_D), (r"\bold{q}_2", GREEN_D), (r"\bold{q}_3", BLUE_D),
                (r"r_{11}", RED),
                (r"r_{12}", YELLOW_B), (r"r_{22}", GREEN),
                (r"r_{13}", LIGHT_PINK), (r"r_{23}", TEAL_B), (r"r_{33}", BLUE),
                ("0", "#666666"), # Punto medio entre GRAY_C y GRAY_D
                ("(1)", YELLOW), ("(2)", YELLOW), ("(3)", YELLOW),
            ):
                label.set_color_by_tex(tex, color)

        for label in (u_time, v_time, w_time):
            label.insert(0, SurroundingRectangle(label, buff=0.25, fill_opacity=1, fill_color=GRAY_E))
            label.to_edge(UL)
            self.camera.add_fixed_in_frame_mobjects(label)

        u_step_1.next_to(u_time, DOWN).to_edge(LEFT)
        v_step_1.next_to(v_time, DOWN).to_edge(LEFT)
        v_step_2.next_to(v_step_1, DOWN).to_edge(LEFT)
        w_step_1.next_to(w_time, DOWN).to_edge(LEFT)
        w_step_2.next_to(w_step_1, DOWN).to_edge(LEFT)
        w_step_3.next_to(w_step_2, DOWN).to_edge(LEFT)

        for label in (u_step_1, v_step_1, v_step_2, w_step_1, w_step_2, w_step_3):
            label.insert(0, SurroundingRectangle(label, buff=0.1, stroke_opacity=0, fill_opacity=0.75, fill_color=GRAY_E))

        for label in (r11_text, r12_text, r22_text, r13_text, r23_text, r33_text):
            label.insert(0, SurroundingRectangle(label, buff=0.25, fill_opacity=1, fill_color=GRAY_E))
            label.to_edge(DR)
            self.camera.add_fixed_in_frame_mobjects(label)

        uvw_texts_f = VGroup(u_text_f, v_text_f, w_text_f)
        self.camera.add_fixed_in_frame_mobjects(*uvw_texts_f, u_text_0, v_text_0, v_text_1, w_text_0, w_text_1)
        uvw_texts_f.arrange_submobjects(DOWN)
        v_text_f.shift([u_text_f[1].get_center()[0] - v_text_f[1].get_center()[0], 0, 0])
        w_text_f.shift([u_text_f[1].get_center()[0] - w_text_f[1].get_center()[0], 0, 0])
        uvw_texts_f.to_edge(UR)

        u_text_0.move_to(u_text_f.get_center() + 0.4*DOWN)
        v_text_0.move_to(v_text_f.get_center() + 0.4*DOWN)
        v_text_1.move_to(v_text_f.get_center())
        w_text_0.move_to(w_text_f.get_center() + 0.4*DOWN)
        w_text_1.move_to(w_text_f.get_center())

        plane_12a = MyPlane(axes, _q1, _v,  color=YELLOW)
        plane_12b = MyPlane(axes, _q1, _v1, color=YELLOW)
        plane_13a = MyPlane(axes, _q1, _w,  color=PINK)
        plane_13b = MyPlane(axes, _q1, _w1, color=PINK)
        plane_13c = MyPlane(axes, _q1, _w2, color=PINK)
        plane_23a = MyPlane(axes, _q2, _w1, color=TEAL)
        plane_23b = MyPlane(axes, _q2, _w2, color=TEAL)

        elbow_12  = MyElbow(axes, _q1, _q2, color=YELLOW)
        elbow_13a = MyElbow(axes, _q1, _w1, color=PINK)
        elbow_13b = MyElbow(axes, _q1, _q3, color=PINK)
        elbow_23  = MyElbow(axes, _q2, _q3, color=TEAL)


        self.camera.add_fixed_in_frame_mobjects(title, u_step_1, v_step_1, v_step_2, w_step_1, w_step_2, w_step_3)
        self.wait()
        self.play(Write(title))
        self.wait(2)

        # Inicio: mostrar todo
        self.set_camera_orientation(phi=65*DEGREES, theta=-18*DEGREES)
        self.begin_ambient_camera_rotation()
        for label in (u_label, v_label, w_label):
            label = self.rotate(label)
        
        self.play(FadeOut(title), FadeIn(axes, u, v, w, u_label, v_label, w_label))
        self.wait(2)
        
        # Normalizar u para obtener q1
        self.play(FadeIn(u_time))
        self.play(VGroup(v, w, v_label, w_label).animate.set_opacity(0.05))
        self.play(FadeIn(u_step_1))
        self.wait(2)
        u1_label = self.rotate(u1_label)
        self.play(
            ReplacementTransform(u, q1), TransformMatchingTex(u_label, u1_label),
            FadeIn(r11_text),
        )
        self.wait(3)
        q1_label = self.rotate(q1_label)
        self.play(
            q1.animate.set_color(RED_D), ReplacementTransform(u1_label, q1_label),
            FadeOut(r11_text),
            FadeIn(u_text_0)
        )
        self.wait(2)
        self.play(TransformMatchingTex(u_text_0, u_text_f))
        self.wait(3)
        self.play(FadeOut(u_time, u_step_1))
        self.wait(0.5)

        # Ortonormalizar v para obtener q2
        self.play(FadeIn(v_time))
        self.play(VGroup(v, v_label).animate.set_opacity(1))
        self.play(FadeIn(v_step_1))
        self.wait(2)
        self.play(FadeIn(plane_12a))
        v1_label = self.rotate(v1_label)
        self.play(
            ReplacementTransform(v, v1), TransformMatchingTex(v_label, v1_label),
            ReplacementTransform(plane_12a, plane_12b),
            FadeIn(r12_text),
        )
        self.play(FadeIn(elbow_12))
        self.play(FadeOut(plane_12b), run_time=0.5)

        self.wait(2)
        self.play(FadeOut(r12_text))
        self.play(FadeIn(v_step_2))
        self.wait(2)
        v2_label = self.rotate(v2_label)
        self.play(
            ReplacementTransform(v1, q2), TransformMatchingTex(v1_label, v2_label),
            FadeIn(r22_text),
        )
        self.wait(3)
        q2_label = self.rotate(q2_label)
        self.play(
            q2.animate.set_color(GREEN_D), ReplacementTransform(v2_label, q2_label),
            FadeOut(r22_text),
            FadeIn(v_text_0),
        )
        self.wait(2)
        self.play(TransformMatchingTex(v_text_0, v_text_1))
        self.wait()
        self.play(TransformMatchingTex(v_text_1, v_text_f))
        self.wait(3)
        self.play(FadeOut(v_time, v_step_1, v_step_2))
        self.wait(0.5)
        

        # Ortonormalizar w para obtener q3
        self.play(FadeIn(w_time))
        self.play(VGroup(w, w_label).animate.set_opacity(1))
        self.play(FadeIn(w_step_1))
        self.wait(2)
        self.play(FadeIn(plane_13a))
        w1_label = self.rotate(w1_label)
        self.play(
            ReplacementTransform(w, w1), TransformMatchingTex(w_label, w1_label),
            ReplacementTransform(plane_13a, plane_13b),
            FadeIn(r13_text),
        )
        self.play(FadeIn(elbow_13a))
        self.wait(2)
        self.play(FadeOut(r13_text))
        self.play(FadeIn(w_step_2))
        self.wait(2)
        self.play(FadeIn(plane_23a))
        w2_label = self.rotate(w2_label)
        self.play(
            ReplacementTransform(w1, w2), TransformMatchingTex(w1_label, w2_label),
            ReplacementTransform(plane_13b, plane_13c), ReplacementTransform(plane_23a, plane_23b),
            ReplacementTransform(elbow_13a, elbow_13b),
            FadeIn(r23_text),   
        )
        self.play(FadeIn(elbow_23))
        self.play(FadeOut(plane_13c), FadeOut(plane_23b), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(r23_text))
        self.play(FadeIn(w_step_3))
        self.wait(2)
        w3_label = self.rotate(w3_label)
        self.play(
            ReplacementTransform(w2, q3), TransformMatchingTex(w2_label, w3_label),
            FadeIn(r33_text),
        )
        self.wait(3)
        q3_label = self.rotate(q3_label)
        self.play(
            q3.animate.set_color(BLUE_D), ReplacementTransform(w3_label, q3_label),
            FadeOut(r33_text),
            FadeIn(w_text_0),
        )
        self.wait(3)
        self.play(TransformMatchingTex(w_text_0, w_text_1))
        self.wait()
        self.play(TransformMatchingTex(w_text_1, w_text_f))
        self.wait(3)
        
        
        # Desaparecer el espacio y agrandar las ecuaciones para u, v y w
        self.play(
            FadeOut(axes, q1, q2, q3, q1_label, q2_label, q3_label, elbow_12, elbow_13b, elbow_23, w_time, w_step_1, w_step_2, w_step_3),
            uvw_texts_f.animate.move_to(ORIGIN).scale(1.2),
        )
        self.stop_ambient_camera_rotation()
        self.set_camera_orientation(phi=0, theta=-90*DEGREES)
        self.wait(3)

        # Transformar la ecuación para w
        w_text_matrix.scale(1.2).align_to(w_text_f, LEFT).shift(DOWN)
        q1_rect = RoundedRectangle(width=0.7, height=1.8, corner_radius=0.2, stroke_opacity=0, fill_opacity=0.2, color=RED  ).move_to(w_text_matrix[4])
        q2_rect = RoundedRectangle(width=0.7, height=1.8, corner_radius=0.2, stroke_opacity=0, fill_opacity=0.2, color=GREEN).move_to(w_text_matrix[6])
        q3_rect = RoundedRectangle(width=0.7, height=1.8, corner_radius=0.2, stroke_opacity=0, fill_opacity=0.2, color=BLUE ).move_to(w_text_matrix[8])
        self.play(
            LaggedStart(
                AnimationGroup(
                    VGroup(u_text_f, v_text_f).animate.shift(UP),
                    TransformMatchingTex(w_text_f, w_text_matrix),
                ),
                FadeIn(q1_rect, q2_rect, q3_rect),
                lag_ratio=0.25,
            ),
            run_time=1.5,
        )
        w_text_matrix.add(q1_rect, q2_rect, q3_rect)
        self.wait(2)

        # Transformar la ecuación para v
        v_text_matrix.scale(1.2).move_to(v_text_f.get_center()).align_to(v_text_f, LEFT).shift(0.25*DOWN)
        self.play(v_text_f[7:].animate.set_opacity(1))
        self.wait()
        q1_rect = q1_rect.copy().move_to(v_text_matrix[4])
        q2_rect = q2_rect.copy().move_to(v_text_matrix[6])
        q3_rect = q3_rect.copy().move_to(v_text_matrix[8])
        self.play(
            LaggedStart(
                AnimationGroup(
                    u_text_f.animate.shift(0.5*UP),
                    w_text_matrix.animate.shift(0.7*DOWN),
                    TransformMatchingTex(v_text_f, v_text_matrix),
                ),
                FadeIn(q1_rect, q2_rect, q3_rect),
                lag_ratio=0.25,
            ),
            run_time=1.5,   
        )
        v_text_matrix.add(q1_rect, q2_rect, q3_rect)
        self.wait(2)

        # Transformar la ecuación para u
        u_text_matrix.scale(1.2).move_to(u_text_f).align_to(u_text_f, LEFT).shift(0.1*UP)
        self.play(u_text_f[4:].animate.set_opacity(1))
        self.wait()
        q1_rect = q1_rect.copy().move_to(u_text_matrix[4])
        q2_rect = q2_rect.copy().move_to(u_text_matrix[6])
        q3_rect = q3_rect.copy().move_to(u_text_matrix[8])
        self.play(
            LaggedStart(
                AnimationGroup(
                    VGroup(v_text_matrix, w_text_matrix).animate.shift(0.8*DOWN),
                    TransformMatchingTex(u_text_f, u_text_matrix),
                ),
                FadeIn(q1_rect, q2_rect, q3_rect),
                lag_ratio=0.25,
            ),
            run_time=1.5,
        )
        u_text_matrix.add(q1_rect, q2_rect, q3_rect)
        self.wait(3)

        # Transformar todas las matrices (q1, q2, q3) en Q
        u_text_matrix_2.scale(1.2).move_to(u_text_matrix)
        v_text_matrix_2.scale(1.2).move_to(v_text_matrix)
        w_text_matrix_2.scale(1.2).move_to(w_text_matrix)
        q1_rect = q1_rect.copy()
        q2_rect = q2_rect.copy()
        q3_rect = q3_rect.copy()
        self.play(
            *[AnimationGroup(
                Transform(VGroup(*tex_1[2:11], *tex_1[-3:]), tex_2[2]),
                VGroup(*tex_1[:2]).animate.move_to(VGroup(*tex_2[:2])),
                VGroup(*tex_1[11:-3]).animate.move_to(VGroup(*tex_2[3:])),
            )
            for (tex_1, tex_2) in ((u_text_matrix, u_text_matrix_2), (v_text_matrix, v_text_matrix_2), (w_text_matrix, w_text_matrix_2))
            ],
        )
        self.remove(*self.mobjects)
        self.add(u_text_matrix_2, v_text_matrix_2, w_text_matrix_2)
        self.wait(2)

        # Agrupar las ecuaciones en una sola ecuación matricial
        uvw_text_1.scale(1.2).to_edge(DOWN).set_opacity(0)
        u_rect = RoundedRectangle(width=0.5, height=1.8, corner_radius=0.2, stroke_opacity=0, fill_opacity=0.2, color=RED_A  ).move_to(uvw_text_1[2])
        v_rect = RoundedRectangle(width=0.5, height=1.8, corner_radius=0.2, stroke_opacity=0, fill_opacity=0.2, color=GREEN_A).move_to(uvw_text_1[4])
        w_rect = RoundedRectangle(width=0.6, height=1.8, corner_radius=0.2, stroke_opacity=0, fill_opacity=0.2, color=BLUE_A ).move_to(uvw_text_1[6])
        VGroup(*[uvw_text_1[i] for i in (0,8,9,10,20)]).set_opacity(1)
        self.play(
            LaggedStart(
                AnimationGroup(
                    FadeIn(uvw_text_1),
                    FadeOut(w_text_matrix_2[1]),
                    *[w_text_matrix_2[start].animate.move_to(uvw_text_1[end])
                    for start, end in ((0,6), (2,18), (3,19), (4,33), (6,35), (8,37))],
                ),
                FadeIn(w_rect),
                lag_ratio=0.25,
            ),
            run_time=2,
        )
        self.wait(0.5)
        self.play(
            LaggedStart(
                AnimationGroup(
                    FadeOut(v_text_matrix_2[1]),
                    *[v_text_matrix_2[start].animate.move_to(uvw_text_1[end])
                    for start, end in ((0,4), (2,15), (3,16), (4,27), (6,29), (8,31))],
                ),
                FadeIn(v_rect),
                lag_ratio=0.25,
            ),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            LaggedStart(
                AnimationGroup(
                    FadeOut(u_text_matrix_2[1]),
                    *[u_text_matrix_2[start].animate.move_to(uvw_text_1[end])
                    for start, end in ((0,2), (2,12), (3,13), (4,21), (6,23), (8,25))],
                ),
                FadeIn(u_rect),
                lag_ratio=0.25,
            ),
            run_time=1.5
        )
        self.wait(0.5)
        self.remove(*self.mobjects)
        uvw_text_1.set_opacity(1)
        self.add(uvw_text_1, u_rect, v_rect, w_rect)
        uvw_text_1.add(u_rect, v_rect, w_rect)
        self.play(uvw_text_1.animate.move_to(ORIGIN))
        uvw_text_1.remove(u_rect, v_rect, w_rect)
        self.wait(2)

        # Transformar la ecuación matricial
        uvw_text_2.scale(1.2).move_to(ORIGIN)
        uvw_text_3.scale(1.2).move_to(ORIGIN)
        uvw_text_4.scale(1.2).move_to(ORIGIN)
        self.play(
            u_rect.animate.move_to(uvw_text_2[2]),
            v_rect.animate.move_to(uvw_text_2[4]),
            w_rect.animate.move_to(uvw_text_2[6]),
            TransformMatchingTex(uvw_text_1, uvw_text_2),
        )
        self.remove(*self.mobjects)
        self.add(uvw_text_2, u_rect, v_rect, w_rect)
        self.wait()

        self.play(
            u_rect.animate.move_to(uvw_text_3[2]),
            v_rect.animate.move_to(uvw_text_3[4]),
            w_rect.animate.move_to(uvw_text_3[6]),
            VGroup(*uvw_text_2[:11]).animate.move_to(VGroup(*uvw_text_3[:11])),
            *[uvw_text_2[i].animate.move_to(uvw_text_3[i-8]) for i in range(20, 37, 2)],
            FadeOut(*[uvw_text_2[i] for i in (13, 15, 17)]),
            Transform(VGroup(uvw_text_2[11], uvw_text_2[19]), uvw_text_3[11]),
        )
        self.remove(*self.mobjects)
        self.add(uvw_text_3, u_rect, v_rect, w_rect)
        self.wait(2)
        q1_rect = q1_rect.copy().move_to(uvw_text_4[12])
        q2_rect = q2_rect.copy().move_to(uvw_text_4[14])
        q3_rect = q3_rect.copy().move_to(uvw_text_4[16])
        self.play(
            u_rect.animate.move_to(uvw_text_4[2]),
            v_rect.animate.move_to(uvw_text_4[4]),
            w_rect.animate.move_to(uvw_text_4[6]),
            VGroup(*uvw_text_3[:10]).animate.move_to(VGroup(*uvw_text_4[:10])),
            VGroup(*uvw_text_3[11:]).animate.move_to(VGroup(*uvw_text_4[19:])),
            Transform(uvw_text_3[10], VGroup(*uvw_text_4[10:19], q1_rect, q2_rect, q3_rect)),
        )
        self.remove(*self.mobjects)
        self.add(uvw_text_4, u_rect, v_rect, w_rect, q1_rect, q2_rect, q3_rect)
        self.wait(3)

        qr_equation = MathTex(r"{{V}} = {{Q}}{{R}}").scale(1.75).shift(2.5*DOWN)

        self.play(Transform(VGroup(*uvw_text_4[:9]).copy(), qr_equation[0]))
        self.play(Transform(uvw_text_4[9].copy(), qr_equation[1]))
        self.play(Transform(VGroup(*uvw_text_4[10:19]).copy(), qr_equation[2]))
        self.play(Transform(VGroup(*uvw_text_4[19:]).copy(), qr_equation[3]))
        self.play(Create(SurroundingRectangle(qr_equation, buff=0.4)))
        self.wait(1)

        qr_title = Text(r"Factorización QR", color=YELLOW).scale(1.75).shift(2.4*UP)
        self.play(Write(qr_title))
        self.wait(4)
        self.play(FadeOut(*self.mobjects))
        self.wait()


class GramSchmidtThumbnail(ThreeDScene):
    def rotate(self, mob, **kwargs):
        rot_matrix = self.camera.generate_rotation_matrix()
        #self.camera.add_fixed_orientation_mobjects(mob)
        mob.apply_points_function_about_point(
            lambda points: np.dot(points, rot_matrix), mob.get_center(), **kwargs
        )
        return mob

    def construct(self):
        self.camera.background_color = GRAY_E

        _u = np.array([1.5, -1, 1.5])
        _v = np.array([-1, 2, 1])
        _w = np.array([-0.5, -1, 2])

        _q1 = _u / np.linalg.norm(_u)

        _proj_q1_v = np.dot(_v, _q1) * _q1
        _v1 = _v - _proj_q1_v
        _q2 = _v1 / np.linalg.norm(_v1)

        _proj_q1_w = np.dot(_w, _q1) * _q1
        _proj_q2_w = np.dot(_w, _q2) * _q2
        _w1 = _w - _proj_q1_w
        _w2 = _w1 - _proj_q2_w
        _q3 = _w2 / np.linalg.norm(_w2)

        axes = ThreeDAxes(num_axis_pieces=1).scale(4).shift(1.5*IN)

        q1 = Vector3D(axes, _q1, color=RED)
        q2 = Vector3D(axes, _q2, color=GREEN)
        q3 = Vector3D(axes, _q3, color=BLUE)

        OU = OUT+UP
        OD = OUT+DOWN

        q1_label = MathTex(r"\bold{q}_1", color=RED_D  ).next_to(q1[-1], OD)
        q2_label = MathTex(r"\bold{q}_2", color=GREEN_D).next_to(q2[-1], OU)
        q3_label = MathTex(r"\bold{q}_3", color=BLUE_D ).next_to(q3[-1], OD)

        elbow_12 = MyElbow(axes, _q1, _q2, color=YELLOW)
        elbow_13 = MyElbow(axes, _q1, _q3, color=PINK)
        elbow_23 = MyElbow(axes, _q2, _q3, color=TEAL)

        upper_title = Text("Ortonormalización").scale(1.25).to_edge(UP)
        lower_title = Text("de Gram-Schmidt").scale(1.25).to_edge(DOWN)

        upper_rectangle = Rectangle(width=16, height=1.6, stroke_opacity=0, fill_opacity=1, color=BLACK).to_edge(UP, buff=0)
        lower_rectangle = upper_rectangle.copy().to_edge(DOWN, buff=0)

        self.camera.add_fixed_in_frame_mobjects(upper_rectangle, lower_rectangle, upper_title, lower_title)
        # Inicio: mostrar todo
        self.set_camera_orientation(phi=80*DEGREES, theta=55*DEGREES)
        for label in (q1_label, q2_label, q3_label):
            label = self.rotate(label)
        self.add(upper_rectangle, lower_rectangle, upper_title, lower_title, axes, q1, q2, q3, q1_label, q2_label, q3_label, elbow_12, elbow_13, elbow_23)


class Outro(Scene):
    def construct(self):
        self.camera.background_color = GRAY_E

        instagram_logo = Group(
            Text("Sígueme en Instagram:", font="sans").scale(0.45),
            ImageMobject('instagram-logo.png').scale_to_fit_height(1),
            Text("@nomechomath", font="sans", color=BLUE).scale(0.45),
        ).arrange_submobjects(DOWN).to_edge(DL)

        patreon_logo = Group(
            Text("¿Quieres apoyar el proyecto?", font="sans").scale(0.45),
            ImageMobject('patreon-logo.png').scale_to_fit_height(1),
            Text("¡Hazte mecena en Patreon!", font="sans", color=ORANGE).scale(0.45),
        ).arrange_submobjects(DOWN).to_edge(DR)

        banner = ManimBanner().scale(0.23).to_edge(DOWN).shift(0.45*LEFT)
        text = Text("Animación creada con", font="sans", color=GRAY_B).scale(0.45).next_to(banner, UP)

        self.play(FadeIn(instagram_logo), FadeIn(patreon_logo))
        self.play(banner.create())
        self.play(banner.expand(), Write(text))
        self.wait(9)
        self.play(Unwrite(banner), Unwrite(text))
        self.play(FadeOut(instagram_logo), FadeOut(patreon_logo))
        self.wait()
