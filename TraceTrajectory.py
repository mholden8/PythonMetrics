import math
import vtk
import slicer

class PerkEvaluatorMetric:

  # Static methods
  @staticmethod
  def GetMetricName():
    return "Display Trajectory"
  
  @staticmethod  
  def GetMetricUnit():
    return "display"
  
  @staticmethod  
  def GetAcceptedTransformRoles():
    return [ "Any" ]
  
  @staticmethod
  def GetRequiredAnatomyRoles():
    return {}
    
    
  # Instance methods
  def __init__( self ):    
    self.curvePoints = vtk.vtkPoints()
    self.curveLines = vtk.vtkCellArray()
    self.curvePolyData = vtk.vtkPolyData()
    self.counter = 0
    
    self.curvePolyData.SetPoints( self.curvePoints )
    self.curvePolyData.SetLines( self.curveLines )
    
    # Turn the polydata into a model    
    curveModel = slicer.mrmlScene.CreateNodeByClass( "vtkMRMLModelNode" )
    curveModel.SetAndObservePolyData( self.curvePolyData )
    curveModel.SetName( "TrajectoryTrace" )
    curveModel.SetScene( slicer.mrmlScene )
  
    curveModelDisplay = slicer.mrmlScene.CreateNodeByClass( "vtkMRMLModelDisplayNode" )
    curveModelDisplay.SetScene( slicer.mrmlScene )
    curveModelDisplay.SetInputPolyDataConnection( curveModel.GetPolyDataConnection() )
  
    slicer.mrmlScene.AddNode( curveModelDisplay )
    slicer.mrmlScene.AddNode( curveModel )
  
    curveModel.SetAndObserveDisplayNodeID( curveModelDisplay.GetID() )
    
  def AddAnatomyRole( self, role, node ):
    pass
       
  def AddTimestamp( self, time, matrix, point ):
  
    # Some initialization for the first point
    if ( self.curveLines.GetNumberOfCells() == 0 ):
      self.curvePoints.InsertNextPoint( point[ 0 ], point[ 1 ], point[ 2 ] )
      self.curveLines.InsertNextCell( 1 )
      self.curveLines.InsertCellPoint( 0 )
  
    self.curvePoints.InsertPoint( self.counter + 1, point[ 0 ], point[ 1 ], point[ 2 ] )
    
    self.curveLines.InsertNextCell( 2 ) # Because there are two points in the cell
    self.curveLines.InsertCellPoint( self.counter )
    self.curveLines.InsertCellPoint( self.counter + 1 )
    self.counter += 1

    
  def GetMetric( self ):
    return 0