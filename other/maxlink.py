import pyext
import pickle
from matcher import *

class Decider(pyext._class):
    _inlets = 2
    _outlets = 3
    
    def __init__(self, *args):
        self.current_buffer = NoteBuffer()
        self.prev_mode = None
        self.bias = None
        self.halflife = None
        self.inspect = False


    def list_1(self, note, velocity):
        if velocity > 0:
            # seeing a new note
            self.current_buffer.add(note, velocity, datetime.datetime.now())
        else:
            # ending a note
            self.current_buffer.close_last(note)
        self.current_buffer.cleanup(2.5)


    def bang_1(self):
        current_mode = complex_vector_calc(self.current_buffer, self.halflife)

        closest_mode = current_mode.nearest_with_bias(
            color_modes, self.prev_mode)

        self.prev_mode = closest_mode    

        self._outlet(1,
            [closest_mode.color1['r'],
            closest_mode.color1['g'],
            closest_mode.color1['b'],])
        self._outlet(2,
            [closest_mode.color2['r'],
            closest_mode.color2['g'],
            closest_mode.color2['b'],])
        self._outlet(3,
            closest_mode.name)
        if self.inspect:
            print current_mode.note_vector


  
    def clear_2(self):
        self.current_buffer = NoteBuffer()
        
  
    def dump_2(self):
        file = open('/Users/n91p817/sample_buffer.pickle', 'w+')
        pickle.dump(current_buffer, file)
        

    def inspect_2(self):
        if self.inspect:
            self.inspect = False
        else:
            self.inspect = True
        
        self._outlet(3,
            str(len(self.current_buffer.get_active())))

    def set_2(self, *args):
        if args:
            if str(args[0]) == "halflife":
                self.halflife = args[1]
                print "Setting halflife to {0} seconds.".format(args[1])
            elif str(args[0]) == "bias":
                self.bias = args[1]
                print "Setting bias to {0}.".format(args[1])