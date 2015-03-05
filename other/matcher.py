import numpy.linalg
import datetime
import pickle

class NoteSet(object):
    def __init__(self):
        self.note_set = numpy.array([0,0,0,0,0,0,0,0,0,0,0,0])

    def __init__(self, ar, cl = {'r':0, 'g':0, 'b':0}, name = ''):
        self.note_set = ar
        self.color = cl
        self.name = name
        self.vector = None

    def __unicode__(self):
        return self.note_set

    @property
    def note_names(self):
        return [self.__translate_num_to_note(i) for i in self.note_set]

    def __translate_num_to_note(self, input):
        if input == 0:
            return 'C'
        elif input == 1:
            return 'C#'
        elif input == 2:
            return 'D'
        elif input == 3:
            return 'D#'
        elif input == 4:
            return 'E'
        elif input == 5:
            return 'F'
        elif input == 6:
            return 'F#'
        elif input == 7:
            return 'G'
        elif input == 8:
            return 'G#'
        elif input == 9:
            return 'A'
        elif input == 10:
            return 'A#'
        elif input == 11:
            return 'B'
        else:
            return None

    @property
    def note_vector(self):
        if self.vector:
            return self.vector
        else:
            ar = numpy.array([0 for i in range(12)])
            for note in self.note_set:
                ar[note] = 1
            return ar

    def intersection(self, target):
        return NoteSet(self.note_set & target.note_set)

    def union(self, target):
        return NoteSet(self.note_set | target.note_set)

    def difference(self, target):
        return NoteSet(self.note_set - target.note_set)

    def distance(self, target):
        return numpy.linalg.norm(self.note_vector - target.note_vector)

    def nearest(self, sets):
        smallest = None
        dist = 100000
        for i in sets:
            if self.distance(i) < dist:
                smallest = i
                dist = self.distance(i)
        return smallest


class NoteBuffer:
    def __init__(self, b=[]):
        self.buffer = b
    
    def add(self, note, velocity, time):
        self.buffer.append(NoteEvent(note, velocity, time))
    
    def get_last(self):
        return self.buffer[:]
    
    def get_last_n(self, number):
        return self.buffer[:number]
    
    def get_last_nsec(self, time):
        return NoteBuffer(filter(
            lambda x: x.start_time > datetime.datetime.now() - datetime.timedelta(seconds=time),
            self.buffer,))
    
    def get_last_note(self, note):
        try:
            return filter(
                lambda x: x.note == note,
                self.buffer,)[-1]
        except:
            return None
    
    def get_active(self):
        return filter(
            lambda x: x.end_time == None,
            self.buffer,)

    def get_inactive(self):
        return filter(
            lambda x: x.end_time != None,
            self.buffer,)

    def get_all(self):
        return self.buffer

    def close_last(self, note):
        notes = filter(
            lambda x: x.note == note and x.end_time == None,
            self.buffer,)
        for n in notes:
            n.end_time = datetime.datetime.now()


class NoteEvent:
    def __init__(self, note, velocity, start_time):
        self.note = note
        self.velocity = velocity
        self.start_time = start_time
        self.end_time = None
    
    @property
    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        else:
            return -1


M1T1 = NoteSet({0,2,4,6,8,10}, {'r': 0, 'g': 0, 'b': 0}, name='M1T1')
M1T2 = NoteSet({1,3,5,7,9,11}, {'r': 0, 'g': 0, 'b': 0}, name='M1T2')
M2T1 = NoteSet({0,1,3,4,6,7,9,10}, {'r': 120, 'g': 0, 'b': 255}, name='M2T1')       # violet purple
M2T2 = NoteSet({1,2,4,5,7,8,10,11}, {'r': 147, 'g': 108, 'b': 0}, name='M2T2')      # gold/brown
M2T3 = NoteSet({2,3,5,6,8,9,11,0}, {'r': 24, 'g': 126, 'b': 0}, name='M2T3')        # green
M3T1 = NoteSet({0,2,3,4,6,7,8,10,11}, {'r': 256, 'g': 149, 'b': 0}, name='M3T1')    # orange
M3T2 = NoteSet({1,3,4,5,7,8,9,11,0}, {'r': 145, 'g': 100, 'b': 145}, name='M3T2')   # grey/mauve
M3T3 = NoteSet({2,4,5,6,8,9,10,0,1}, {'r': 0, 'g': 0, 'b': 0}, name='M3T3')# blue-orange
M3T4 = NoteSet({3,5,6,7,9,10,11,1,2}, {'r': 0, 'g': 0, 'b': 0}, name='M3T4')# green-orange
M4T1 = NoteSet({0,1,2,5,6,7,8,11}, {'r': 0, 'g': 0, 'b': 0}, name='M4T1')
M4T2 = NoteSet({1,2,3,6,7,8,9,0}, {'r': 0, 'g': 0, 'b': 0}, name='M4T2')
M4T3 = NoteSet({2,3,4,7,8,9,10,1}, {'r': 0, 'g': 0, 'b': 0}, name='M4T3')# yellow & violet
M4T4 = NoteSet({3,4,5,8,9,10,11,2}, {'r': 0, 'g': 0, 'b': 0}, name='M4T4')# deep violet with white
M4T5 = NoteSet({4,5,6,9,10,11,0,3}, {'r': 0, 'g': 0, 'b': 0}, name='M4T5')# deep violet
M4T6 = NoteSet({5,6,7,10,11,0,1,4}, {'r': 215, 'g': 0, 'b': 64}, name='M4T6')# carmine red
M5T1 = NoteSet({0,1,5,6,7,11}, {'r': 0, 'g': 0, 'b': 0}, name='M5T1')
M5T2 = NoteSet({1,2,6,7,8,0}, {'r': 0, 'g': 0, 'b': 0}, name='M5T2')
M5T3 = NoteSet({2,3,7,8,9,1}, {'r': 0, 'g': 0, 'b': 0}, name='M5T3')
M5T4 = NoteSet({3,4,8,9,10,2}, {'r': 0, 'g': 0, 'b': 0}, name='M5T4')
M5T5 = NoteSet({4,5,9,10,11,3}, {'r': 0, 'g': 0, 'b': 0}, name='M5T5')
M5T6 = NoteSet({5,6,10,11,0,4}, {'r': 0, 'g': 0, 'b': 0}, name='M5T6')
M6T1 = NoteSet({0,2,4,5,6,8,10,11}, {'r': 0, 'g': 0, 'b': 0}, name='M6T1')# golden
M6T2 = NoteSet({1,3,5,6,7,9,11,0}, {'r': 0, 'g': 0, 'b': 0}, name='M6T2')# brown, russet
M6T3 = NoteSet({2,4,6,7,8,10,0,1}, {'r': 0, 'g': 0, 'b': 0}, name='M6T3')# yellow
M6T4 = NoteSet({3,5,7,8,9,11,1,2}, {'r': 0, 'g': 0, 'b': 0}, name='M6T4')# yellow violet black
M6T5 = NoteSet({4,6,8,9,10,0,2,3}, {'r': 0, 'g': 0, 'b': 0}, name='M6T5')
M6T6 = NoteSet({5,7,9,10,11,1,3,4}, {'r': 0, 'g': 0, 'b': 0}, name='M6T6')
M7T1 = NoteSet({0,1,2,3,5,6,7,8,9,11}, {'r': 0, 'g': 0, 'b': 0}, name='M7T1')
M7T2 = NoteSet({1,2,3,4,6,7,8,9,10,0}, {'r': 0, 'g': 0, 'b': 0}, name='M7T2')
M7T3 = NoteSet({2,3,4,5,7,8,9,10,11,1}, {'r': 0, 'g': 0, 'b': 0}, name='M7T3')
M7T4 = NoteSet({3,4,5,6,8,9,10,11,0,2}, {'r': 0, 'g': 0, 'b': 0}, name='M7T4')
M7T5 = NoteSet({4,5,6,7,9,10,11,0,1,3}, {'r': 0, 'g': 0, 'b': 0}, name='M7T5')
M7T6 = NoteSet({5,6,7,8,10,11,0,1,2,4}, {'r': 0, 'g': 0, 'b': 0}, name='M7T6')

all_modes = [
    M1T1, M1T2,
    M2T1, M2T2, M2T3,
    M3T1, M3T2, M3T3, M3T4,
    M4T1, M4T2, M4T3, M4T4, M4T5, M4T6,
    M5T1, M5T2, M5T3, M5T4, M5T5, M5T6,
    M6T1, M6T2, M6T3, M6T4, M6T5, M6T6,
    M7T1, M7T2, M7T3, M7T4, M7T5, M7T6,
]

color_modes = [
]

current_buffer = NoteBuffer()

def simple_vector_calc(buffer):
    active_notes = buffer.get_active()
    return NoteSet(set([i.note % 12 for i in active_notes]))

def fixed_duration_calc(buffer):
    last_5_secs = buffer.get_last_nsec(5)
    return NoteSet(set([i.note % 12 for i in last_5_secs]))
    
def fixed_notes_calc(buffer):
    last_20_notes = buffer.get_last_n(20)
    return NoteSet(set([i.note % 12 for i in last_5_secs]))

def complex_vector_calc(buffer):
    power = 2
    current_time = datetime.datetime.now()
    window_length = 5
    window_time = current_time - datetime.timedelta(seconds = window_length)
    active = simple_vector_calc(buffer)
    vector = active.note_vector
    for i in vector:
        if i is not 1:
            window = buffer.get_last_nsec(window_length) - active
            for i in window.note_set:
                value = -1 * ((current_time - i.note_end)/(current_time - i.window_time))^power + 1
                if value > vector[i.note % 12]:
                    vector[i.note % 12] = value
    buffer.vector = vector
    return buffer


def list(note, velocity):
    if velocity:
        # seeing a new note
        current_buffer.add(note, velocity, datetime.datetime.now())
    else:
        # ending a note
        current_buffer.close_last(note)
    current_mode = simple_vector_calc(current_buffer)
    #current_mode = complex_vector_calc(current_buffer)
    closest_mode = current_mode.nearest(all_modes)
    return (
        closest_mode.color['r'],
        closest_mode.color['g'],
        closest_mode.color['b'],
        closest_mode.name)
        
def bang():
    file = open('/Users/n91p817/sample_buffer.pickle', 'w+')
    pickle.dump(current_buffer, file)