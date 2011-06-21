#import sip
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = "qt4"

from traits.api import *
from traitsui.api import *
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene

from traitsui.key_bindings import KeyBinding, KeyBindings

bindings = KeyBindings(*[
        KeyBinding(
            binding1 = str(i),
            description = "first binding",
            method_name = "func%i"%i)
        for i in [1,2,3]])


        

class MlabGui(HasTraits):    
    x = Bool
    scene = Instance(MlabSceneModel,  ())
    funcs = []

    def __init__(self,funcs):
        HasTraits.__init__(self)
        self.funcs = funcs        
    
    def func1(self,info):
        self.funcs[0]()
    def func2(self,info):
        self.funcs[1]()
    def func3(self,info):
        self.funcs[2]()
        
    
    view = View(
        Item("scene",editor = SceneEditor(scene_class=MayaviScene),
                 height=250, width=300, show_label=False),
        Item("x"),
        resizable = True,
        key_bindings = bindings,

    )
    
if __name__ == "__main__":
    def hi1(): print "hi1"
    def hi2(): print "hi2"
    def hi3(): print "hi3"
    m = Mlab([hi1,hi2,hi3])
    m.configure_traits()
