import os
import subprocess
import shutil
from PyQt5.QtWidgets import QMainWindow, QFrame, QVBoxLayout
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk

class VTKApp(QMainWindow):
    def __init__(self, mesh_files_seq=None, parent=None):
        super(VTKApp, self).__init__(parent)
        self.own_mesh_files_seq = mesh_files_seq
        self.initUI()

    def initUI(self):
        self.frame = QFrame()
        self.vl = QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)
        self.show()

    def showEvent(self, event):
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # Convert CGNS to VTK
        self.convert_cgns_to_vtk(self.own_mesh_files_seq)

        # Read VTK files and add to the renderer
        for file_name in self.get_vtk_files():
            reader = vtk.vtkUnstructuredGridReader()
            reader.SetFileName(file_name)
            mapper = vtk.vtkDataSetMapper()
            mapper.SetInputConnection(reader.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            self.ren.AddActor(actor)

        self.ren.SetBackground(0.3647, 0.4431, 0.6196)
        self.iren.Initialize()

        self.delete_subdirectories_in_directory("vtk_output")

    def convert_cgns_to_vtk(self, cgns_files):
        env = os.environ.copy()
        env["PATH"] = "/home/anthony/anaconda3/pkgs/cgns-4.3.0-h97bc1a7_3/bin:" + env["PATH"]
        env["LD_LIBRARY_PATH"] = "/home/anthony/anaconda3/pkgs/hdf5-1.12.2-nompi_h4df4325_101/lib:" + env.get("LD_LIBRARY_PATH", "")
        for cgns_file in cgns_files:
            output_path = os.path.join("vtk_output", os.path.basename(cgns_file) + ".vtk")
            command = f"cgns_to_vtk -a {cgns_file} {output_path}"
            subprocess.run(command, shell=True, env=env)

    def get_vtk_files(self, path='vtk_output'):
        file_names = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.vtk'):
                    full_path = os.path.join(root, file)
                    file_names.append(full_path)
        return file_names

    def delete_subdirectories_in_directory(self, directory):
        """Delete all subdirectories and their contents in the specified directory."""
        for name in os.listdir(directory):
            path = os.path.join(directory, name)
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
            except Exception as e:
                print(f"Failed to delete {path}. Reason: {e}")
