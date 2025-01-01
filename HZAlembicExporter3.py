# creation date : 16 Dec, 2024
#
# Author :    Hamed Zandieh
# Contact :   hamed.zandieh@gmail.com
#
# Description :
#    This script Export Materials and Alembic for UnrealEngine
# How To use :
#    copy python file into maya script folder then run these lines:
# 
# import HZAlembicExporter3
# from importlib import reload
# reload(HZAlembicExporter3)
# ui = HZAlembicExporter3.ExporterUI()
# ui.show()
# 

import pymel.core as pm
import os, random
import maya.utils

try:
    from PySide6 import QtWidgets, QtCore # type: ignore
    # print("Using PySide6")
except ImportError:
    try:
        from PySide2 import QtWidgets, QtCore
        # print("Using PySide2")
    except ImportError as e:
       raise ImportError("Neither PySide6 nor PySide2 is available in this Maya environment.")        

class ExporterUI(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setWindowTitle("Export Materials and Alembic")
        self.setMinimumWidth(500)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Export Path Input
        path_layout = QtWidgets.QHBoxLayout()
        basedir = pm.sceneName().parent
        expoDir = os.path.abspath(os.path.join(basedir, "ALEMBICS"))
        self.export_path_label = QtWidgets.QLabel(expoDir)
        self.select_path_button = QtWidgets.QPushButton("Select Export Path")
        self.select_path_button.clicked.connect(self.select_export_path)
        path_layout.addWidget(QtWidgets.QLabel("Export Path:"))
        path_layout.addWidget(self.export_path_label)
        path_layout.addWidget(self.select_path_button)
        layout.addLayout(path_layout)

        # Material Suffix
        # self.material_suffix_input = QtWidgets.QLineEdit("_mt")
        # layout.addWidget(QtWidgets.QLabel("Material Suffix:"))
        # layout.addWidget(self.material_suffix_input)

        # Export Options
        self.batch_export_checkbox = QtWidgets.QCheckBox("Apply Objects Material to their Faces")
        layout.addWidget(self.batch_export_checkbox)

        # Export Buttons
        self.alembic_export_button = QtWidgets.QPushButton("Export Alembic")
        self.alembic_export_button.clicked.connect(self.export_alembic)
        layout.addWidget(self.alembic_export_button)

        self.export_button = QtWidgets.QPushButton("Export Materials to FBX")
        self.export_button.clicked.connect(self.export_materials)
        layout.addWidget(self.export_button)

    def select_export_path(self):
        """
        Opens a folder dialog to select the export directory for both FBX materials and Alembic files.
        """
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Export Directory")
        if directory:
            is_valid, message = validate_directory(directory)
            if not is_valid:
                QtWidgets.QMessageBox.critical(self, "Error", message)
                return
            if not directory.endswith(os.sep): directory += os.sep
            self.export_path_label.setText(directory.replace("\\", "/"))


    def export_materials(self):
        """
        Export materials from selected meshes to FBX in the selected directory.
        """
        export_directory = self.export_path_label.text() 
        try:
            prepare_and_export_materials(export_directory)
            QtWidgets.QMessageBox.information(self, "Success", f"Materials exported to {export_directory}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to export materials: {e}")


    def export_alembic(self):
        """
        Trigger Alembic export for selected meshes in the selected directory.
        """
        export_directory = self.export_path_label.text()
        # if not export_directory:
        #     export_directory = self.make_default_path()        
        applytofaces = self.batch_export_checkbox.isChecked()
        try:
            start_frame = int(pm.playbackOptions(q=True, minTime=True))
            end_frame = int(pm.playbackOptions(q=True, maxTime=True))
            export_alembic(export_directory, start_frame, end_frame, applytofaces)
            QtWidgets.QMessageBox.information(self, "Success", f"Alembic exported to {export_directory}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to export Alembic: {e}")

    def make_default_path(self):
        basedir = pm.sceneName().parent
        expoDir = os.path.join(basedir, "ALEMBICS")
        if not expoDir.exists():
            expoDir.mkdir()
        if not expoDir.endswith(os.sep): directory += os.sep
        self.export_path_label.setText(expoDir.replace("\\", "/"))                 
        return expoDir


def validate_directory(path):
    """
    Validates if the given path is a valid directory and writable.
    
    Parameters:
        path (str): The directory path to validate.
    
    Returns:
        bool: True if the path is valid and writable, False otherwise.
        str: Message providing additional information about the validation result.
    """
    if not path:
        return False, "Path is empty or None."
    if not os.path.exists(path):
        return False, f"Path does not exist: {path}"
    if not os.path.isdir(path):
        return False, f"Path is not a directory: {path}"
    if not os.access(path, os.W_OK):
        return False, f"Directory is not writable: {path}"
    return True, "Path is a valid, writable directory."
    
def get_and_validate_selected_objects():
    selected = pm.selected(type='transform')
    for node in selected:
        pm.lockNode(node, lock=False)    
    # selectedPolygons = pm.filterExpand(selected, sm=12)
    selected_meshes = [obj for obj in selected if obj.getShape() and isinstance(obj.getShape(), pm.nt.Mesh)]
    if not selected_meshes:
        raise RuntimeError("No meshes selected for export.")
    # print(selected_meshes)
    return selected_meshes

def ensure_plugin(plugin_name): #  fbxmaya  AbcExport
    """
    Ensures the FBX plugin is loaded.
    """
    plugin_name = "fbxmaya"
    if not pm.pluginInfo(plugin_name, query=True, loaded=True):
        pm.loadPlugin(plugin_name)
        print(f"{plugin_name} plugin loaded successfully.")

def prepare_and_export_materials(export_directory):
    """
    Prepares and exports materials of selected meshes in FBX format for Unreal.
    Renames shading nodes, removes namespaces, and saves the FBX file in the specified directory.
    
    :param export_directory: Path to save the FBX files.
    :param material_suffix: Suffix to apply to material names.
    """
    ensure_plugin("fbxmaya")

    selected_meshes = get_and_validate_selected_objects()

    copied_meshes = []
    for mesh in selected_meshes:
        copy = mesh.duplicate(name=mesh.name() + "_copy")[0]
        pm.delete(copy, constructionHistory=True)
        copied_meshes.append(copy)

    # Process materials
    # process_materials_for_export(copied_meshes, material_suffix)

    # Generate FBX file name and save materials
    fbx_path = os.path.join(export_directory, f"{selected_meshes[0]}_materials_export.fbx")
    escaped_file_path = fbx_path.replace("\\", "/").replace("|","_")  # Replace backslashes with forward slashes

    pm.select(copied_meshes, r=1)
    export_fbx_materials_only(escaped_file_path)

    # Cleanup
    pm.delete(copied_meshes)
    print(f"Materials exported successfully to {escaped_file_path}.")

def export_fbx_materials_only(output_path):
    """
    Exports selected materials only in FBX ASCII format, ensuring Unreal compatibility.
    """
    pm.mel.eval(f'FBXExportEmbeddedTextures -v true;FBXExportInAscii -v true;FBXExportFileVersion -v FBX201600;FBXExport -f "{output_path}" -s')

def assign_material_to_all_faces(selected_meshes):
    """
    Gets the material of each selected mesh and assigns it to all faces of each mesh.

    :param mesh_objects: List of PyMEL mesh objects to process.
    """
    pm.select(cl=1)
    for obj in selected_meshes:
        # def_shdr, def_sg = pm.createSurfaceShader('lambert')
        # def_shdr.color.set([random.random(),random.random(),random.random()])
        # obj = pm.selected()[0]
        shading_groups = pm.ls(obj.getShape().connections(), type='shadingEngine')
        if not shading_groups:
            pm.warning(f"No material assigned to mesh '{obj}'. Skipping.")
            continue   
        sg = shading_groups[0]
        # sg_sets = pm.sets( sg, q=1) # check members
        # sg_cons = sg.connections() # pm.listConnections(sg)
        sg_mats = pm.ls(sg.connections(), mat=1)
        pm.rename(sg, sg_mats[0].name()+'_SG')
        pm.select(obj, r=1)
        pm.hyperShade(assign="lambert1")
        process_idle_events()
        pm.select(f"{obj}.f[*]", r=1)
        process_idle_events()        
        pm.hyperShade(assign=sg_mats[0])
        pm.select(cl=1)
        print(f"Assigned '{sg.name()}' to all faces of '{obj.name()}'.")


    # Re-select original polygons
    pm.select(selected_meshes, r=True)

def export_alembic(export_directory, start_frame, end_frame, applytofaces = True):
    """
    Exports selected meshes to Alembic format and saves in the specified directory.
    
    :param export_directory: Path to save the Alembic file.
    :param start_frame: Start frame for the export.
    :param end_frame: End frame for the export.
    """
    try:
        # Ensure Alembic plugin is loaded
        ensure_plugin("AbcExport")

        selected_meshes = get_and_validate_selected_objects()

        # Unlock initial shading group and selected nodes
        pm.lockNode('initialShadingGroup', lock=False)
        for node in selected_meshes:
            pm.lockNode(node, lock=False)

        # Generate Alembic file path
        abc_path = os.path.join(export_directory, f"{selected_meshes[0]}_meshes_export.abc")
        escaped_file_path = abc_path.replace("\\", "/").replace("|","_")  # Replace backslashes with forward slashes

        # Escape pipe characters in root paths
        # escaped_roots = [dag.fullPath() for dag in pm.ls(selected_meshes, dag=True)]
        escaped_roots = [obj.longName() for obj in selected_meshes]
        abc_nodes = " ".join(f"-root {root}" for root in escaped_roots)

        # Prepare meshes for Alembic export
        if applytofaces:
            assign_material_to_all_faces(selected_meshes)

        # Alembic export options
        required_options = [
            "-uvWrite",  
            "-stripNamespaces",  
            "-writeFaceSets",  
            "-worldSpace",  
            # "-eulerFilter",  
            "-writeUVSets",
            "-dataFormat ogawa",  
        ]
        export_command = (
            "AbcExport -j \""
            f"-frameRange {start_frame} {end_frame} "
            f"{' '.join(required_options)} "
            f"{abc_nodes} -file \\\"{escaped_file_path}\\\""
            "\""
        )

        # print(export_command)
        # Execute the Alembic export command
        pm.mel.eval(export_command)
        print(f"Alembic exported successfully to {escaped_file_path}.")

    except Exception as e:
        print(f"Failed to export Alembic: {e}")
        raise RuntimeError(f"Failed to export Alembic: {e}")

def process_idle_events(max=15):
    jlist = pm.evalDeferred(list=1)
    pm.timer(startTimer=1)
    while len(jlist) > 1:
        maya.utils.processIdleEvents()
        jlist = pm.evalDeferred(list=1)
        if pm.timer(lap=1) > max:
            break
    pm.timer(endTimer=1)

# Launch the UI
if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication([])
    # mayaWindow = next(w for w in app.topLevelWidgets() if w.objectName()=='MayaWindow')
    # mayaWindow = pm.ui.Window("MayaWindow").asQtObject()
    win = ExporterUI()  # (parent=mayaWindow)
    win.show()
    app.exec()
