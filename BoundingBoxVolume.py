import math

class PerkEvaluatorMetric:

  def __init__( self ):
    self.Initialize( None )
  
  def GetMetricName( self ):
    return "Bounding Box Volume"
    
  def GetMetricUnit( self ):
    return "mm^3"
    
  def RequiresTissueNode( self ):
    return False
    
  def RequiresNeedle( self ):
    return False
    
  def Initialize( self, tissueNode ):
    self.minX = None
    self.minY = None
    self.minZ = None
    self.maxX = None
    self.maxY = None
    self.maxZ = None
    
    self.volume = None
    
  def AddTimestamp( self, time, matrix, point ):

    if ( self.minX == None or self.minY == None or self.minZ == None or self.maxX == None or self.maxY == None or self.maxZ == None ):
      self.minX = point[ 0 ]
      self.minY = point[ 1 ]
      self.minZ = point[ 2 ]
      self.maxX = point[ 0 ]
      self.maxY = point[ 1 ]
      self.maxZ = point[ 2 ]
      
    if ( point[ 0 ] < self.minX ):
      self.minX = point[ 0 ]
    if ( point[ 1 ] < self.minY ):
      self.minY = point[ 1 ]
    if ( point[ 2 ] < self.minZ ):
      self.minZ = point[ 2 ]
    if ( point[ 0 ] > self.maxX ):
      self.maxX = point[ 0 ]
    if ( point[ 1 ] > self.maxY ):
      self.maxY = point[ 1 ]
    if ( point[ 2 ] > self.maxZ ):
      self.maxZ = point[ 2 ]
    
    
  def Finalize( self ):
    self.volume = ( self.maxX - self.minX ) * ( self.maxY - self.minY ) * ( self.maxZ - self.minZ )
    
  def GetMetric( self ):
    return self.volume