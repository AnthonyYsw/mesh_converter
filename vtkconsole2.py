import h5py
import numpy as np
import vtk
from vtk.util import numpy_support

def create_vtk_data(coord_x_data, coord_y_data, coord_z_data, pyramid_data, tetra_data, triangle_data, quad_data):
    points = vtk.vtkPoints()
    for x, y, z in zip(coord_x_data, coord_y_data, coord_z_data):
        points.InsertNextPoint(x, y, z)

    cells = vtk.vtkCellArray()

    # add pyramid
    for i in range(0, len(pyramid_data), 5):
        pyramid = vtk.vtkPyramid()
        for j in range(5):
            pyramid.GetPointIds().SetId(j, pyramid_data[i+j]-1)
        cells.InsertNextCell(pyramid)

    # add tetrahedral
    for i in range(0, len(tetra_data), 4):
        tetra = vtk.vtkTetra()
        for j in range(4):
            tetra.GetPointIds().SetId(j, tetra_data[i+j]-1)
        cells.InsertNextCell(tetra)

    # add triangle
    for i in range(0, len(triangle_data), 3):
        triangle = vtk.vtkTriangle()
        for j in range(3):
            triangle.GetPointIds().SetId(j, triangle_data[i+j]-1)
        cells.InsertNextCell(triangle)

    # add quadrilateral
    for i in range(0, len(quad_data), 4):
        quad = vtk.vtkQuad()
        for j in range(4):
            quad.GetPointIds().SetId(j, quad_data[i+j]-1)
        cells.InsertNextCell(quad)

    poly_data = vtk.vtkPolyData()
    poly_data.SetPoints(points)
    poly_data.SetPolys(cells)

    return poly_data

def separate_face_elements(face_data):
    triangles = []
    quads = []
    i = 0
    while i < len(face_data):
        node_count = face_data[i]
        if node_count == 3:
            triangles.extend(face_data[i+1:i+node_count+1])
        elif node_count == 4:
            quads.extend(face_data[i+1:i+node_count+1])
        i += node_count + 1
    return np.array(triangles), np.array(quads)


with h5py.File('zone1.cgns', 'r') as f:
    coord_x_path = '/Base/blk-1/GridCoordinates/CoordinateX/ data'
    coord_y_path = '/Base/blk-1/GridCoordinates/CoordinateY/ data'
    coord_z_path = '/Base/blk-1/GridCoordinates/CoordinateZ/ data'

    pyramid_element_path = '/Base/blk-1/PyramidElements/ElementConnectivity/ data'
    tet_elements_path = '/Base/blk-1/TetElements/ElementConnectivity/ data'
    
    face_data_paths = [
        '/Base/blk-1/wall/ElementConnectivity/ data',
        '/Base/blk-1/inlet/ElementConnectivity/ data',
        '/Base/blk-1/outlet/ElementConnectivity/ data',
        '/Base/blk-1/periodic_hi/ElementConnectivity/ data',
        '/Base/blk-1/periodic_lo/ElementConnectivity/ data'
    ]

    face_data = np.concatenate([np.array(f[path]) for path in face_data_paths])
    triangle_data, quad_data = separate_face_elements(face_data)

    pyramid_elements_data = np.array(f[pyramid_element_path])
    tet_elements_data = np.array(f[tet_elements_path])
    coord_x_data = np.array(f[coord_x_path])
    coord_y_data = np.array(f[coord_y_path])
    coord_z_data = np.array(f[coord_z_path])
    
# 将这些数据传递给函数
vtk_data = create_vtk_data(coord_x_data, coord_y_data, coord_z_data, pyramid_elements_data, tet_elements_data, triangle_data, quad_data)
print(vtk_data)

# 创建一个Mapper和Actor
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(vtk_data)

actor = vtk.vtkActor()
actor.SetMapper(mapper)

# 创建一个渲染器，渲染窗口和渲染窗口交互器
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# 添加到渲染器
renderer.AddActor(actor)
renderer.SetBackground(0.5, 0.5, 1) # 设置背景颜色为白色

# 开始渲染和交互
renderWindow.Render()
renderWindowInteractor.Start()
