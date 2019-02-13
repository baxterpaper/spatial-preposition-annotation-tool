### Handles with textual displays and input as well as output

import sys

# So we can find the bgui module
sys.path.append('../..')

import csv
import os

from os.path import expanduser

import random

import bgui
import bgui.bge_utils
import bge

preposition_list = ['in','inside','on', 'on top of', 'against', 'over', 'under', 'above','below']


main_scene = bge.logic.getCurrentScene()

co = bge.logic.getCurrentController()

empty = co.owner

keyboard = co.sensors["textinputkeyboard"]

deselect = co.sensors["deselect"]

end_game = co.actuators['END_GAME']

def quit_game():
    co.activate(end_game)

### This allows users to reset choices and replaces the old cancel button

for key,status in keyboard.events:
    if status == bge.logic.KX_INPUT_JUST_ACTIVATED:
        if key == bge.events.DELKEY:
            bge.logic.sendMessage("deselect") #Sends a deselect message to sensors in any active scene.
            bge.logic.sendMessage("change")

# the confirm property is necessary to force the script to have to run a second time
if 'confirm' in empty.getPropertyNames():
    if deselect.positive:
        empty['confirm'] = False
        co.owner['sys'].layout.confirmlbl.visible = False



selectable_objects = []

for obj in main_scene.objects:
    if 'selectedfigure' in obj.getPropertyNames():
        selectable_objects.append(obj)



def output(selection):
    output_path = expanduser("~")
    bge.logic.sendMessage("deselect") #Sends a deselect message to sensors in any active scene.
    bge.logic.sendMessage("change")

    print(str(selection))
    selection.append("currentscene")

    cam_loc = main_scene.objects["Camera"].position
    cam_rot = main_scene.objects["Camera"].orientation
    selection.append(cam_loc)
    selection.append(cam_rot)

    time = empty['game_time']
    selection.append(time)

    with open(output_path + '/output.csv', "a") as csvfile:
        outputwriter = csv.writer(csvfile)
        outputwriter.writerow(selection)




class SimpleLayout(bgui.bge_utils.Layout):

    def __init__(self, sys, data):
        super().__init__(sys, data)
        
        #Use a frame to store all of our widgets
        self.frame = bgui.Frame(self, border=0,options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
        self.frame.colors = [(0, 0, 0, 0) for i in range(4)]


        

        # Add a label for the title
        self.titlelbl = bgui.Label(self.frame, text=empty.getPropertyNames()[0], pos=[0.4, .95],
            sub_theme='Large', pt_size = 50,options = bgui.BGUI_DEFAULT)

        self.timerlbl = bgui.Label(self.frame,text="0:00", pos=[0.1, .95],
            sub_theme='Large', pt_size = 50,options = bgui.BGUI_DEFAULT)

        if 'pragmatic' not in empty.getPropertyNames():
            # Add a label for the figure
            self.figurelbl = bgui.Label(self.frame,text='Figure: ',pos=[.1, .9],
                sub_theme='Large',pt_size = 50, options = bgui.BGUI_DEFAULT)
            # Add a label for the ground
            self.groundlbl = bgui.Label(self.frame,text='Ground: ', pos=[.7, .9],
                sub_theme='Large',pt_size = 50, options = bgui.BGUI_DEFAULT)

            self.confirmlbl = bgui.Label(self.frame,text='Press Enter to Confirm this selection', pos=[0.3, .5],
                sub_theme='Large', color = (0,1,0,1),outline_color=(1,0,0,1), outline_size = 2, pt_size = 50, options = bgui.BGUI_DEFAULT)
            self.confirmlbl.visible = False

            if 'sfg' in empty.getPropertyNames():
                self.allselectedlbl = bgui.Label(self.frame,text='Press Enter to Confirm that you have selected all pairs in the scene', pos=[0.1, .5],
                    sub_theme='Large', color = (0,1,0,1),outline_color=(1,0,0,1), outline_size = 2, pt_size = 50, options = bgui.BGUI_DEFAULT)
                self.allselectedlbl.visible = False

            if "p" not in empty.getPropertyNames():
                # A label for the given preposition
                self.prepositionlbl = bgui.Label(self.frame,text= 'Preposition: '+random.choice(preposition_list), pos=[0, 0.9],
                    sub_theme='Large',pt_size = 50, options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
        
            if "p" in empty.getPropertyNames():
                # A themed frame to store text input widget
                self.win = bgui.Frame(self.frame, size=[.6, .1],pos=[0, 0.1],border=0.2,
                    options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)

                self.prepositionlbl = bgui.Label(self.frame,text="", pos=[0, 0.9],
                    sub_theme='Large',pt_size = 50, options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)

                # A TextInput widget
                self.input = bgui.TextInput(self.win, text="",
                    input_options = bgui.BGUI_INPUT_NONE,pt_size = 50, options = bgui.BGUI_DEFAULT)
                self.input.activate()
                self.input.on_enter_key = self.on_input_enter
        
        if 'pragmatic' in empty.getPropertyNames():
            # Add a label for the title
            self.instructionlbl0 = bgui.Label(self.frame, text='Imagine you want the robot to bring you the highlighted object.', pos=[0.18, .9],
                sub_theme='Large', pt_size = 50,options = bgui.BGUI_DEFAULT)
            self.instructionlbl1 = bgui.Label(self.frame, text='Provide the robot with a description of its location', pos=[0.21, .85],
                sub_theme='Large', pt_size = 50,options = bgui.BGUI_DEFAULT)
            # A TextInput widget
            # A themed frame to store text input widget
            self.win = bgui.Frame(self.frame, size=[.6, .1],pos=[0, 0.1],border=0.2,
                options=bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX)
            self.input = bgui.TextInput(self.win, text="",
                input_options = bgui.BGUI_INPUT_NONE,pt_size = 50, options = bgui.BGUI_DEFAULT)
            self.input.activate()
            self.input.on_enter_key = self.on_input_enter

            if 'f' in empty.getPropertyNames():
                # Add a label for the figure
                self.figurelbl = bgui.Label(self.frame, text='Object: ',pos=[0, .8],
                    sub_theme='Large',pt_size = 50, options = bgui.BGUI_DEFAULT| bgui.BGUI_CENTERX)

        


        



    def on_input_enter(self, widget):
        # in pragmatic tasks just output immediately
        if "pragmatic" in empty.getPropertyNames():
            triple=[0,1,2]
            triple[1] = widget.text
            if 'f' in empty.getPropertyNames():
                for obj in selectable_objects:
                    
                    if obj.get('selectedfigure')==True:
                        triple[0]=obj
                
                triple[2] = 'N/A'

            output(triple)
            
        elif empty.get('confirm') == False:
            self.prepositionlbl.text = "You've entered: " + widget.text
        widget.text = ""


        

        
        #widget.deactivate()
        #widget.frozen = 1
        
    # def on_img_click(self, widget):
    #     self.counter += 1
    #     self.lbl.text = "You've clicked me %d times" % self.counter
    #     self.progress.percent += .1
    #     if self.counter % 2 == 1:
    #         self.win.img.texco = [(1,0), (0,0), (0,1), (1,1)]
    #     else:
    #         self.win.img.texco = [(0,0), (1,0), (1,1), (0,1)]


def main(cont):
    own = cont.owner
    mouse = bge.logic.mouse

    if 'sys' not in own:
        # Create our system and show the mouse
        own['sys'] = bgui.bge_utils.System('../../themes/default')
        own['sys'].load_layout(SimpleLayout, None)
        mouse.visible = True

    else:
        own['sys'].run()



main(bge.logic.getCurrentController())

#Update Timer
seconds = empty['game_time']
m, s = divmod(seconds, 60)
co.owner['sys'].layout.timerlbl.text = "%d:%02d" % (m, s)

### Quit game at 10mins
if round(seconds,0) == 600.0:
    quit_game()

if 'pragmatic' not in empty.getPropertyNames():
    for obj in selectable_objects:
        if obj.get('selectedfigure')==True:
            co.owner['sys'].layout.figurelbl.text = 'Figure: '+ obj.name

        if obj.get('selectedground')==True: 
            co.owner['sys'].layout.groundlbl.text = 'Ground: '+ obj.name



    if all(obj['selectedfigure']==False for obj in selectable_objects):
        co.owner['sys'].layout.figurelbl.text = ''

    if all(obj['selectedground']==False for obj in selectable_objects):
        co.owner['sys'].layout.groundlbl.text = ''

    if "p" in empty.getPropertyNames():
        ###Keep text input focused
        co.owner['sys'].layout.input.system.focused_widget = co.owner['sys'].layout.input

        triple=[0,1,2]
        triple[1] = co.owner['sys'].layout.prepositionlbl.text.replace("You've entered: ",'')
        for obj in selectable_objects:
            
            if obj.get('selectedfigure')==True:
                triple[0]=obj

            if obj.get('selectedground')==True: 
                triple[2] = obj

        if triple[0] != 0 and triple[2] != 2 and triple[1] != '':
            co.owner['sys'].layout.confirmlbl.visible = True

            # the confirm property is necessary to force the script to have to run a second time
            if empty.get('confirm') == True:
                for key,status in keyboard.events:
                    # key[0] == bge.events.keycode, key[1] = status
                    if status == bge.logic.KX_INPUT_JUST_ACTIVATED:
                        if key == bge.events.ENTERKEY:
                            output(triple)


                            co.owner['sys'].layout.prepositionlbl.text = ''

                            co.owner['sys'].layout.confirmlbl.visible = False

            empty['confirm'] = True
        # if triple[1] == '':
        #     co.owner['sys'].layout.input.on_enter_key = co.owner['sys'].layout.on_input_enter(co.owner['sys'].layout.input)
    if "p" not in empty.getPropertyNames():
        #### Output annotations
        triple=[0,1,2]
        triple[1] = co.owner['sys'].layout.prepositionlbl.text.replace('Preposition: ','')
        for obj in main_scene.objects:
            
            if obj.get('selectedfigure')==True:
                triple[0]=obj

            if obj.get('selectedground')==True: 
                triple[2] = obj

        if triple[0] != 0 and triple[2] != 2:
            co.owner['sys'].layout.confirmlbl.visible = True
            for key,status in keyboard.events:
                
                if status == bge.logic.KX_INPUT_JUST_ACTIVATED:
                    if key == bge.events.ENTERKEY:
                        output(triple)
                        

                        co.owner['sys'].layout.confirmlbl.visible = False
                            
            

        if 'sfg' not in empty.getPropertyNames():
            #### Change preposition
            changeprep = co.sensors["changepreposition"]

            for key,status in keyboard.events:
                # key[0] == bge.events.keycode, key[1] = status
                if status == bge.logic.KX_INPUT_JUST_ACTIVATED:
                    if key == bge.events.SPACEKEY:
                        bge.logic.sendMessage("changepreposition")

            if changeprep.positive:
                co.owner['sys'].layout.prepositionlbl.text = 'Preposition: ' + random.choice(preposition_list)
                # new_index = preposition_list.index(co.owner['sys'].layout.lbl2.text) + 1

                # if new_index < len(preposition_list):

                #     co.owner['sys'].layout.lbl2.text = preposition_list[new_index]
                # else:
                #     co.owner['sys'].layout.lbl2.text = preposition_list[0]

if 'sfg' in empty.getPropertyNames():
    if deselect.positive:
        co.owner['sys'].layout.allselectedlbl.visible = False
    for key,status in keyboard.events:
        # key[0] == bge.events.keycode, key[1] = status
        if status == bge.logic.KX_INPUT_JUST_ACTIVATED:
            if key == bge.events.SPACEKEY:
                co.owner['sys'].layout.allselectedlbl.visible = True
    for key,status in keyboard.events:
        # key[0] == bge.events.keycode, key[1] = status
        if status == bge.logic.KX_INPUT_JUST_ACTIVATED:
            if key == bge.events.ENTERKEY:
                if co.owner['sys'].layout.allselectedlbl.visible == True:
                    output(['ALL INSTANCES SELECTED',co.owner['sys'].layout.prepositionlbl.text.replace('Preposition: ',''),''])
                    co.owner['sys'].layout.allselectedlbl.visible = False
                    co.owner['sys'].layout.prepositionlbl.text = 'Preposition: ' + random.choice(preposition_list)

if "pragmatic" in empty.getPropertyNames():
    ###Keep text input focused
    co.owner['sys'].layout.input.system.focused_widget = co.owner['sys'].layout.input

    if 'f' in empty.getPropertyNames():
        for obj in selectable_objects:
            if obj['selectedfigure']==True:
                co.owner['sys'].layout.figurelbl.text = 'Object: '+ obj.name










