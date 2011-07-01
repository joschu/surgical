import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
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
    
    
class fb:
    i = 0
    def __init__(self,xyzs,xyz_goal=None):
        self.xyzs = xyzs
        self.gui = MlabGui([self.back,self.fwd])
        self.mlab = self.gui.scene.mlab
        opts = dict(tube_radius=.5)
        xyz_start = xyzs[0]
        if xyz_goal is None: xyz_goal = xyzs[-1]
        self.mlab.plot3d(
            xyz_start[0],xyz_start[1],xyz_start[2],color=(1,0,0),**opts)
        self.plot_cur = self.mlab.plot3d(
            xyz_start[0],xyz_start[1],xyz_start[2],color=(0,1,0),**opts)
        self.mlab.plot3d(
            xyz_goal[0],xyz_goal[1],xyz_goal[2],color=(0,0,1),**opts)
        
    def fwd(self):
        self.i = min(self.i+1,len(self.xyzs)-1)
        self.update()
    def back(self):
        self.i = max(self.i-1,0)
        self.update()
    def update(self):
        x,y,z = self.xyzs[self.i]            
        self.plot_cur.mlab_source.set(x=x,y=y,z=z)
        print "updated to %i"%self.i
    def start(self):
        self.gui.configure_traits()        
    
if __name__ == "__main__":
    def hi1(): print "hi1"
    def hi2(): print "hi2"
    def hi3(): print "hi3"
    m = MlabGui([hi1,hi2,hi3])
    m.configure_traits()
