from __future__ import unicode_literals, division

from unittest import TestCase
import optivis.scene
import optivis.bench.components as components
import optivis.bench.links as links

class TestSceneInstantiation(TestCase):
  def test_invalid_titles(self):
    self.assertRaises(Exception, optivis.scene.Scene, title=int(1))
    self.assertRaises(Exception, optivis.scene.Scene, title=float(1))
    self.assertRaises(Exception, optivis.scene.Scene, title=dict(one=1, two=2, three=3))
    self.assertRaises(Exception, optivis.scene.Scene, title=list('abc'))
    self.assertRaises(Exception, optivis.scene.Scene, title=set('abc'))
    self.assertRaises(Exception, optivis.scene.Scene, title=frozenset('abc'))
    self.assertRaises(Exception, optivis.scene.Scene, title=tuple('abc'))
    
  def test_valid_titles(self):
    self.assertTrue(isinstance(optivis.scene.Scene(title=None), optivis.scene.Scene))
    self.assertTrue(isinstance(optivis.scene.Scene(title=unicode('Title')), optivis.scene.Scene))
    self.assertTrue(isinstance(optivis.scene.Scene(title=str('Title')), optivis.scene.Scene))
    
  def test_invalid_azimuth(self):
    self.assertRaises(ValueError, optivis.scene.Scene, azimuth=str('invalid'))
    self.assertRaises(ValueError, optivis.scene.Scene, azimuth=unicode('invalid'))
    self.assertRaises(TypeError, optivis.scene.Scene, azimuth=None)
    self.assertRaises(TypeError, optivis.scene.Scene, azimuth=dict(one=1, two=2, three=3))
    self.assertRaises(TypeError, optivis.scene.Scene, azimuth=list('abc'))
    self.assertRaises(TypeError, optivis.scene.Scene, azimuth=set('abc'))
    self.assertRaises(TypeError, optivis.scene.Scene, azimuth=frozenset('abc'))
    self.assertRaises(TypeError, optivis.scene.Scene, azimuth=tuple('abc'))

  def test_valid_azimuth(self):
    self.assertTrue(isinstance(optivis.scene.Scene(azimuth=0), optivis.scene.Scene))
    self.assertTrue(isinstance(optivis.scene.Scene(azimuth=int('45')), optivis.scene.Scene))
    self.assertTrue(isinstance(optivis.scene.Scene(azimuth=float('720')), optivis.scene.Scene))
    self.assertTrue(isinstance(optivis.scene.Scene(azimuth=float('inf')), optivis.scene.Scene))

  def test_valid_init(self):
    self.assertTrue(isinstance(optivis.scene.Scene(), optivis.scene.Scene))
    self.assertTrue(isinstance(optivis.scene.Scene(title=None, azimuth=0), optivis.scene.Scene))

class TestSceneAddComponent(TestCase):
  def setUp(self):
    self.scene = optivis.scene.Scene()
    
  def test_add_valid_component(self):
    component = components.Laser()
    
    # can add a component of type laser
    self.assertTrue(self.scene.addComponent(component) is None)
  
  def test_add_invalid_component(self):
    componentA = components.Laser()
    componentB = components.CavityMirror()

    link = links.Link(componentA.getOutputNode('out'), componentB.getInputNode('fr'), 10)
    
    # can't add a component of type link
    self.assertRaises(Exception, self.scene.addComponent, link)
    
class TestSceneAddLink(TestCase):
  def setUp(self):
    self.scene = optivis.scene.Scene()
    self.componentA = components.Laser()
    self.componentB = components.CavityMirror()
    
  def test_add_valid_link(self):
    # add components to scene
    self.scene.addComponent(self.componentA)
    self.scene.addComponent(self.componentB)
    
    link = links.Link(self.componentA.getOutputNode('out'), self.componentB.getInputNode('fr'), 10)
    
    # can add a link of type Link
    self.assertTrue(self.scene.addLink(link) is None)
  
  def test_add_invalid_link(self):    
    # can't add a link of type Laser
    self.assertRaises(Exception, self.scene.addLink, self.componentA)