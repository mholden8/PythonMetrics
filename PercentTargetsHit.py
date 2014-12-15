import math
import vtk
import slicer

class PerkEvaluatorMetric:

  # A structure is "in" the imaging plane if it is within some small threshold of the plane
  IMAGE_PLANE_THRESHOLD = 5 #mm (since scaling should be uniform)
  # And is within the depth
  IMAGE_X_MIN = 173 #pixels
  IMAGE_X_MAX = 793 #pixels
  IMAGE_Y_MIN = 153 #pixels
  IMAGE_Y_MAX = 625 #pixels

  def __init__( self ):
    pass
  
  def GetMetricName( self ):
    return "Targets Hit"
    
  def GetMetricUnit( self ):
    return "%"
    
  def RequiresTissueNode( self ):
    return False
    
  def RequiresNeedle( self ):
    return False
    
  def GetAcceptedTransformRoles( self ):
    return [ "Ultrasound" ]
    
  def GetRequiredAnatomyRoles( self ):
    return [ "POIs" ]
    
  def AddAnatomyRole( self, role, node ):
    if ( role == "POIs" and node != None ):
      self.targets = node  
      self.hitTargets = [ 0 ] * self.targets.GetNumberOfFiducials()
    
  def Initialize( self ):   
    self.percentHit = 0
    
    
  def AddTimestamp( self, time, matrix, point ):
  
    for i in range( self.targets.GetNumberOfFiducials() ):
    
      # Find the centre of the fiducial
      centerPoint = [ 0, 0, 0 ]
      self.targets.GetNthFiducialPosition( i, centerPoint )
      centerPoint_RAS = [ centerPoint[ 0 ], centerPoint[ 1 ], centerPoint[ 2 ], 1 ]
      
      # Assume the matrix is ImageToRAS
      # We know the center of mass of the structure in the RAS coordinate system
      # Transform the center of mass into the image coordinate system
      RASToImageMatrix = vtk.vtkMatrix4x4()
      RASToImageMatrix.DeepCopy( matrix )
      RASToImageMatrix.Invert()
    
      centerPoint_Image = [ 0, 0, 0, 1 ]
      RASToImageMatrix.MultiplyPoint( centerPoint_RAS, centerPoint_Image )
    
      # Assumption is the imaging plane is in the Image coordinate system's XY plane    
      if ( centerPoint_Image[0] < PerkEvaluatorMetric.IMAGE_X_MIN or centerPoint_Image[0] > PerkEvaluatorMetric.IMAGE_X_MAX ):
        return
      
      if ( centerPoint_Image[1] < PerkEvaluatorMetric.IMAGE_Y_MIN or centerPoint_Image[1] > PerkEvaluatorMetric.IMAGE_Y_MAX ):
        return
    
      # Note: This only works for similarity matrix (i.e. uniform scale factor)
      scaleFactor = math.pow( vtk.vtkMatrix4x4().Determinant( matrix ), 1.0 / 3.0 )
    
      # Now check if the z-coordinate of the point in the image coordinate system is below some threshold value (i.e. 2mm)
      if ( abs( centerPoint_Image[2] ) < PerkEvaluatorMetric.IMAGE_PLANE_THRESHOLD / scaleFactor ):
        self.hitTargets[ i ] = 1

    
  def Finalize( self ):
    self.percentHit = 100 * float( sum( self.hitTargets ) ) / len( self.hitTargets )
    
  def GetMetric( self ):
    return self.percentHit