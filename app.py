from flask import Flask, render_template, request
import plotly.graph_objects as go
import numpy as np
import plotly.io as pio

app = Flask(__name__)


# Функция для создания матрицы преобразований
def transformation_matrix(scale=1, rotation=(0, 0, 0), translation=(0, 0, 0)):
    rx, ry, rz = rotation
    tx, ty, tz = translation
    s = scale

    # Матрица масштабирования
    scale_matrix = np.array([
        [s, 0, 0, 0],
        [0, s, 0, 0],
        [0, 0, s, 0],
        [0, 0, 0, 1]
    ])

    # Матрицы поворота
    rx_matrix = np.array([
        [1, 0, 0, 0],
        [0, np.cos(rx), -np.sin(rx), 0],
        [0, np.sin(rx), np.cos(rx), 0],
        [0, 0, 0, 1]
    ])
    ry_matrix = np.array([
        [np.cos(ry), 0, np.sin(ry), 0],
        [0, 1, 0, 0],
        [-np.sin(ry), 0, np.cos(ry), 0],
        [0, 0, 0, 1]
    ])
    rz_matrix = np.array([
        [np.cos(rz), -np.sin(rz), 0, 0],
        [np.sin(rz), np.cos(rz), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    # Матрица переноса
    translation_matrix = np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

    # Итоговая матрица преобразования
    transformation = translation_matrix @ rz_matrix @ ry_matrix @ rx_matrix @ scale_matrix
    return transformation


# Применение матрицы преобразования к массиву координат
def apply_transformation(vertices, matrix):
    transformed_vertices = []
    for vertex in vertices:
        v = np.array([*vertex, 1])  # Добавляем 1 для работы с матрицей 4x4
        transformed_vertex = matrix @ v
        transformed_vertices.append(transformed_vertex[:3])  # Убираем 4-й элемент (1)
    return np.array(transformed_vertices)


# Вершины буквы "L"
vertices = np.array([
    [0, 0, 0], [0, 1, 0], [0.2, 1, 0], [0.2, 0.2, 0], [1, 0.2, 0], [1, 0, 0],  # Передняя грань
    [0, 0, -0.2], [0, 1, -0.2], [0.2, 1, -0.2], [0.2, 0.2, -0.2], [1, 0.2, -0.2], [1, 0, -0.2]  # Задняя грань
])

# Треугольники (грани)
triangles = [
    [0, 1, 2], [0, 2, 3], [0, 3, 5], [3, 4, 5],  # Передняя грань
    [6, 7, 8], [6, 8, 9], [6, 9, 11], [9, 10, 11],  # Задняя грань
    [0, 1, 7], [0, 6, 7],  # Левая грань
    [5, 4, 10], [5, 11, 10],  # Правая грань
    [1, 2, 8], [1, 7, 8],  # Верхняя грань
    [3, 4, 10], [3, 9, 10]  # Нижняя грань
]


# Функция для создания 3D-графика
def create_3d_plot(vertices, triangles):
    fig = go.Figure()

    # Добавляем 3D модель
    fig.add_trace(go.Mesh3d(
        x=vertices[:, 0],
        y=vertices[:, 1],
        z=vertices[:, 2],
        i=[t[0] for t in triangles],
        j=[t[1] for t in triangles],
        k=[t[2] for t in triangles],
        color='lightblue',
        opacity=0.7
    ))

    # Добавляем оси XYZ
    fig.add_trace(go.Scatter3d(
        x=[0, 1, 0, 0],
        y=[0, 0, 1, 0],
        z=[0, 0, 0, 1],
        mode='lines+text',
        line=dict(width=5, color=["red", "green", "blue"]),
        text=["X", "Y", "Z"],
        textfont=dict(size=12, color='black'),
        textposition='top center'
    ))

    # Добавляем точку пересечения осей
    fig.add_trace(go.Scatter3d(
        x=[0],
        y=[0],
        z=[0],
        mode='markers',
        marker=dict(size=5, color='black')
    ))

    # Настройки камеры и осей
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[-1, 2], title="X", backgroundcolor="white", gridcolor="lightgray",
                       zerolinecolor="lightgray"),
            yaxis=dict(range=[-1, 2], title="Y", backgroundcolor="white", gridcolor="lightgray",
                       zerolinecolor="lightgray"),
            zaxis=dict(range=[-1, 2], title="Z", backgroundcolor="white", gridcolor="lightgray",
                       zerolinecolor="lightgray"),
            aspectratio=dict(x=1, y=1, z=1)
        ),
        title='3D Model of Letter L',
        width=800,
        height=800
    )

    return fig


# Функция для создания ортографических проекций
def create_projection_plot(vertices, triangles, plane):
    fig = go.Figure()

    # Ортографическая проекция на плоскость XY
    if plane == 'xy':
        for triangle in triangles:
            fig.add_trace(go.Scatter(
                x=[vertices[triangle[0]][0], vertices[triangle[1]][0], vertices[triangle[2]][0],
                   vertices[triangle[0]][0]],  # X координаты
                y=[vertices[triangle[0]][1], vertices[triangle[1]][1], vertices[triangle[2]][1],
                   vertices[triangle[0]][1]],  # Y координаты
                mode='lines',
                line=dict(color='blue', width=2)
            ))
        fig.update_layout(
            title="Orthographic Projection (XY)",
            xaxis_title="X",
            yaxis_title="Y",
            xaxis=dict(range=[-1, 2], showgrid=True, zeroline=True, gridcolor="lightgray"),
            yaxis=dict(range=[-1, 2], showgrid=True, zeroline=True, gridcolor="lightgray"),
            height=500,
            width=500
        )

    # Ортографическая проекция на плоскость XZ
    elif plane == 'xz':
        for triangle in triangles:
            fig.add_trace(go.Scatter(
                x=[vertices[triangle[0]][0], vertices[triangle[1]][0], vertices[triangle[2]][0],
                   vertices[triangle[0]][0]],  # X координаты
                y=[vertices[triangle[0]][2], vertices[triangle[1]][2], vertices[triangle[2]][2],
                   vertices[triangle[0]][2]],  # Z координаты
                mode='lines',
                line=dict(color='blue', width=2)
            ))
        fig.update_layout(
            title="Orthographic Projection (XZ)",
            xaxis_title="X",
            yaxis_title="Z",
            xaxis=dict(range=[-1, 2], showgrid=True, zeroline=True, gridcolor="lightgray"),
            yaxis=dict(range=[-1, 2], showgrid=True, zeroline=True, gridcolor="lightgray"),
            height=500,
            width=500
        )

    # Ортографическая проекция на плоскость YZ
    elif plane == 'yz':
        for triangle in triangles:
            fig.add_trace(go.Scatter(
                x=[vertices[triangle[0]][1], vertices[triangle[1]][1], vertices[triangle[2]][1],
                   vertices[triangle[0]][1]],  # Y координаты
                y=[vertices[triangle[0]][2], vertices[triangle[1]][2], vertices[triangle[2]][2],
                   vertices[triangle[0]][2]],  # Z координаты
                mode='lines',
                line=dict(color='blue', width=2)
            ))
        fig.update_layout(
            title="Orthographic Projection (YZ)",
            xaxis_title="Y",
            yaxis_title="Z",
            xaxis=dict(range=[-1, 2], showgrid=True, zeroline=True, gridcolor="lightgray"),
            yaxis=dict(range=[-1, 2], showgrid=True, zeroline=True, gridcolor="lightgray"),
            height=500,
            width=500
        )

    return fig



@app.route('/', methods=['GET', 'POST'])
def index():
    # Преобразования по умолчанию
    scale = 1
    rotation = (0, 0, 0)
    translation = (0, 0, 0)

    # Обрабатываем данные из формы
    if request.method == 'POST':
        scale = float(request.form.get('scale', 1))
        rotation = (
            np.radians(float(request.form.get('rx', 0))),
            np.radians(float(request.form.get('ry', 0))),
            np.radians(float(request.form.get('rz', 0)))
        )
        translation = (
            float(request.form.get('tx', 0)),
            float(request.form.get('ty', 0)),
            float(request.form.get('tz', 0))
        )

    # Создаем матрицу преобразования
    matrix = transformation_matrix(scale, rotation, translation)
    transformed_vertices = apply_transformation(vertices, matrix)

    # Создаем графики
    fig_3d = create_3d_plot(transformed_vertices, triangles)
    plot_3d = pio.to_html(fig_3d, full_html=False)

    # Ортографические проекции
    projection_xy = create_projection_plot(transformed_vertices, triangles, 'xy')
    projection_xz = create_projection_plot(transformed_vertices, triangles, 'xz')
    projection_yz = create_projection_plot(transformed_vertices, triangles, 'yz')

    plot_xy = pio.to_html(projection_xy, full_html=False)
    plot_xz = pio.to_html(projection_xz, full_html=False)
    plot_yz = pio.to_html(projection_yz, full_html=False)

    # Выводим матрицу
    matrix_str = f"Scale: {scale}\nRotation (X, Y, Z): {rotation}\nTranslation (X, Y, Z): {translation}"

    return render_template('index.html', plot_3d=plot_3d, plot_xy=plot_xy, plot_xz=plot_xz, plot_yz=plot_yz,
                           matrix=matrix_str)


if __name__ == '__main__':
    app.run(debug=True)
