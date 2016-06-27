from __future__ import print_function
import os
import vtk

# Read the data
os.chdir(os.path.dirname(__file__))
pl3d = vtk.vtkMultiBlockPLOT3DReader()
xyx_file = "volume/combxyz.bin"
q_file = "volume/combq.bin"
pl3d.SetXYZFileName(xyx_file)
pl3d.SetQFileName(q_file)
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

blocks = pl3d.GetOutput()
b0 = blocks.GetBlock(0)

# Setup VTK environment
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
render_window.SetInteractor(interactor)
renderer.SetBackground(0.2,0.2,0.2)
interactor.Initialize()

# Draw Outline
outline = vtk.vtkStructuredGridOutlineFilter()
outline.SetInputData(b0)
outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())
outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(1,1,1)
renderer.AddActor(outline_actor)
renderer.ResetCamera()


# Threshold points
threshold = vtk.vtkThresholdPoints()
threshold.SetInputData(b0)
threshold.ThresholdByUpper(0.5)

# Draw arrows
arrow = vtk.vtkArrowSource()
glyphs = vtk.vtkGlyph3D()
glyphs.SetInputData(b0)
glyphs.SetSourceConnection(arrow.GetOutputPort())
glyphs.SetInputConnection(threshold.GetOutputPort())

glyphs.SetVectorModeToUseVector()
glyphs.SetScaleModeToScaleByVector()
glyphs.SetScaleFactor(0.005)
glyphs.SetColorModeToColorByVector()

# Mapper
glyph_mapper =  vtk.vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyphs.GetOutputPort())
glyph_actor = vtk.vtkActor()
glyph_actor.SetMapper(glyph_mapper)

glyph_mapper.UseLookupTableScalarRangeOn()
renderer.AddActor(glyph_actor)

# Set color lookuptable
glyphs.Update()
s0,sf = glyphs.GetOutput().GetScalarRange()
lut = vtk.vtkColorTransferFunction()
lut.AddRGBPoint(s0, 1,0,0)
lut.AddRGBPoint(sf, 0,1,0)
glyph_mapper.SetLookupTable(lut)

interactor.Start()