import numpy.linalg
import datetime

class NoteSet(object):
    def __init__(
        self, ar=numpy.array([0,0,0,0,0,0,0,0,0,0,0,0]),
        cl1={'r':0, 'g':0, 'b':0}, cl2={'r':0, 'g':0, 'b':0}, name = ''):
        if len(ar) > 12:
            raise Exception('Too many notes!')
        else:
            self.note_set = ar
            self.color1 = cl1
            self.color2 = cl2
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
        if self.vector is not None:
            return numpy.array(self.vector)
        else:
            ar = numpy.array([0 for i in range(12)])
            for note in self.note_set:
                ar[note] = 1
            return ar

    def intersection(self, target):
        return NoteSet(set(self.note_set) & set(target.note_set))

    def union(self, target):
        return NoteSet(set(self.note_set) | set(target.note_set))

    def difference(self, target):
        return NoteSet(set(self.note_set) - set(target.note_set))

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
        
    def nearest_with_bias(self, sets, prev=None, bias=0.9):
        if prev:
            smallest = prev
            dist = self.distance(prev) * bias
            for i in sets:
                if self.distance(i) < dist:
                    smallest = i
                    dist = self.distance(i)
            return smallest
        else:
            return self.nearest(sets)

class NoteBuffer:
    def __init__(self, b=[]):
        self.buffer = b
    
    def add(self, note, velocity, time):
        self.buffer.append(NoteEvent(note, velocity, time))
    
    def get_last_n(self, number):
        return self.buffer[:number]
    
    def get_last_nsec(self, time):
        return filter(
            lambda x: x.start_time > datetime.datetime.now() - datetime.timedelta(seconds=time),
            self.buffer,)
    
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
            
    def cleanup(self, time):
        notes = filter(
            lambda x: x.start_time < datetime.datetime.now() - datetime.timedelta(seconds=time),
            self.buffer,)
        for n in notes:
            n.end_time = datetime.datetime.now()

    def get_heights(self):
        counts = [{'chroma': i, 'height': 0} for i in range(12)]
        for note in self.buffer:
            if note.height > counts[chroma]['height']:
                counts[chroma]['height'] = note.height
        sorted(counts, key=lambda n:n['height'])
        return [i['chroma'] for i in counts]

class NoteEvent:
    def __init__(self, note, velocity, start_time):
        self.note = note
        self.velocity = velocity
        self.start_time = start_time
        self.end_time = None
        self.chroma = note % 12
        self.height = note / 12
    
    @property
    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        else:
            return -1

    @property
    def active(self):
        return not self.end_time            

    def __unicode__(self):
        return "chroma: {0}, height: {1}, start: {2}, end: {3}".format(
            self.chroma, self.height, self.start_time, self.end_time)
            
    def __str__(self):
        return self.__unicode__()
     
def simple_vector_calc(buffer):
    active_notes = buffer.get_active()
    return NoteSet(set([i.chroma for i in active_notes]))

def fixed_duration_calc(buffer):
    last_5_secs = buffer.get_last_nsec(5)
    return NoteSet(set([i.chroma for i in last_5_secs]))
    
def fixed_notes_calc(buffer):
    last_20_notes = buffer.get_last_n(20)
    return NoteSet(set([i.chroma for i in last_20_notes]))

def complex_vector_calc(
    buffer, halflife = 0.5):
    current_time = datetime.datetime.now()
    window_length = halflife * 10

    window_time = current_time - datetime.timedelta(seconds = window_length)
    ns = NoteSet()
    vector = [0.0 for i in range(12)]
    ns.vector = vector
    for i in buffer.buffer:
        value = round(0.5 ** (
            (float((current_time - i.start_time).seconds) / halflife)), 3)
        if value > vector[i.chroma]:
            vector[i.chroma] = value
    ns.vector = vector
    return ns
    
M0T0 = NoteSet({0,1,2,3,4,5,6,7,8,9,10,11},
    {'r': 255, 'g': 255, 'b': 255, 'w': 255, 'i':255},
    {'r': 255, 'g': 255, 'b': 255, 'w': 255, 'i':255},
    name='M0T0') # all white
M0T0.vector = [1.25 for i in range(12)]
M0T1 = NoteSet({},
    {'r': 0, 'g': 0, 'b': 0, 'w': 0, 'i': 0},
    {'r': 0, 'g': 0, 'b': 0, 'w': 0, 'i': 0},
    name='M0T1') # no notes at all...black
M0T1.vector = [-0.5 for i in range(12)]
M1T1 = NoteSet({0,2,4,6,8,10}, name='M1T1')
M1T2 = NoteSet({1,3,5,7,9,11}, name='M1T2')
M2T1 = NoteSet({0,1,3,4,6,7,9,10},
    {'r': 127, 'g': 0, 'b': 191, 'w': 0, 'i': 255},
    {'r': 84, 'g': 0, 'b': 168, 'w': 0, 'i': 255},
    name='M2T1')       # violet purple
M2T2 = NoteSet({1,2,4,5,7,8,10,11},
    {'r': 204, 'g': 204, 'b': 0, 'w': 0, 'i': 255},
    {'r': 89, 'g': 38, 'b': 0, 'w': 0, 'i': 255},
    name='M2T2')      # gold/brown
M2T3 = NoteSet({2,3,5,6,8,9,11,0},
    {'r': 0, 'g': 255, 'b': 0, 'w': 0, 'i': 255},
    {'r': 0, 'g': 204, 'b': 51, 'w': 0, 'i': 255},
    name='M2T3')        # green
M3T1 = NoteSet({0,2,3,4,6,7,8,10,11},
    {'r': 255, 'g': 153, 'b': 0, 'w': 0, 'i': 255},
    {'r': 255, 'g': 153, 'b': 0, 'w': 0, 'i': 255},
    name='M3T1')    # orange
M3T2 = NoteSet({1,3,4,5,7,8,9,11,0},
    {'r': 0, 'g': 64, 'b': 64, 'w': 192, 'i': 255},
    {'r': 230, 'g': 192, 'b': 255, 'w': 84, 'i': 255},
    name='M3T2')   # grey/mauve
M3T3 = NoteSet({2,4,5,6,8,9,10,0,1},
    {'r': 0, 'g': 0, 'b': 255, 'w': 0, 'i': 255},
    {'r': 255, 'g': 192, 'b': 0, 'w': 0, 'i': 255},
    name='M3T3')# blue-orange
    
M3T4 = NoteSet({3,5,6,7,9,10,11,1,2},
    {'r': 0, 'g': 255, 'b': 0, 'w': 0, 'i': 255},
    {'r': 255, 'g': 175, 'b': 0, 'w': 0, 'i': 255},
    name='M3T4')# green-orange
M4T1 = NoteSet({0,1,2,5,6,7,8,11},
    name='M4T1')
M4T2 = NoteSet({1,2,3,6,7,8,9,0},
    name='M4T2')
    
M4T3 = NoteSet({2,3,4,7,8,9,10,1},
    {'r': 255, 'g': 255, 'b': 0, 'w': 51, 'i': 255},
    {'r': 128, 'g': 0, 'b': 192, 'w': 0, 'i': 255},
    name='M4T3')# yellow & violet
M4T4 = NoteSet({3,4,5,8,9,10,11,2},
    {'r': 141, 'g': 0, 'b': 217, 'w': 0, 'i': 255},
    {'r': 0, 'g': 0, 'b': 153, 'w': 255, 'i': 255},
    name='M4T4')# deep violet with white
M4T5 = NoteSet({4,5,6,9,10,11,0,3},
    {'r': 141, 'g': 0, 'b': 217, 'w': 0, 'i': 255},
    {'r': 141, 'g': 0, 'b': 217, 'w': 0, 'i': 255},
    name='M4T5')# deep violet
M4T6 = NoteSet({5,6,7,10,11,0,1,4},
    {'r': 255, 'g': 0, 'b': 0, 'w': 0, 'i': 255},
    {'r': 255, 'g': 0, 'b': 0, 'w': 128, 'i': 255},
    name='M4T6')# carmine red
M5T1 = NoteSet({0,1,5,6,7,11}, name='M5T1')
M5T2 = NoteSet({1,2,6,7,8,0}, name='M5T2')
M5T3 = NoteSet({2,3,7,8,9,1}, name='M5T3')
M5T4 = NoteSet({3,4,8,9,10,2}, name='M5T4')
M5T5 = NoteSet({4,5,9,10,11,3}, name='M5T5')
M5T6 = NoteSet({5,6,10,11,0,4}, name='M5T6')
M6T1 = NoteSet({0,2,4,5,6,8,10,11},
    {'r': 230, 'g': 218, 'b': 0, 'w': 0, 'i': 255},
    {'r': 192, 'g': 166, 'b': 0, 'w': 0, 'i': 255},
    name='M6T1')# golden
M6T2 = NoteSet({1,3,5,6,7,9,11,0},
    {'r': 77, 'g': 45, 'b': 0, 'w': 0, 'i': 255},
    {'r': 115, 'g': 64, 'b': 0, 'w': 0, 'i': 255},
    name='M6T2')# brown, russet
M6T3 = NoteSet({2,4,6,7,8,10,0,1},
    {'r': 255, 'g': 255, 'b': 0, 'w': 0, 'i': 255},
    {'r': 255, 'g': 255, 'b': 0, 'w': 0, 'i': 255},
    name='M6T3')# yellow
M6T4 = NoteSet({3,5,7,8,9,11,1,2},
    {'r': 255, 'g': 255, 'b': 0, 'w': 51, 'i': 255},
    {'r': 128, 'g': 0, 'b': 192, 'w': 0, 'i': 255},
    name='M6T4')# yellow violet black
M6T5 = NoteSet({4,6,8,9,10,0,2,3}, name='M6T5')
M6T6 = NoteSet({5,7,9,10,11,1,3,4}, name='M6T6')
M7T1 = NoteSet({0,1,2,3,5,6,7,8,9,11}, name='M7T1')
M7T2 = NoteSet({1,2,3,4,6,7,8,9,10,0}, name='M7T2')
M7T3 = NoteSet({2,3,4,5,7,8,9,10,11,1}, name='M7T3')
M7T4 = NoteSet({3,4,5,6,8,9,10,11,0,2}, name='M7T4')
M7T5 = NoteSet({4,5,6,7,9,10,11,0,1,3}, name='M7T5')
M7T6 = NoteSet({5,6,7,8,10,11,0,1,2,4}, name='M7T6')

all_modes = [
    M0T0, M0T1,
    M1T1, M1T2,
    M2T1, M2T2, M2T3,
    M3T1, M3T2, M3T3, M3T4,
    M4T1, M4T2, M4T3, M4T4, M4T5, M4T6,
    M5T1, M5T2, M5T3, M5T4, M5T5, M5T6,
    M6T1, M6T2, M6T3, M6T4, M6T5, M6T6,
    M7T1, M7T2, M7T3, M7T4, M7T5, M7T6,
]
color_modes = [
    M0T0, M0T1,
    M2T1, M2T2, M2T3,
    M3T1, M3T2, M3T3, M3T4,
    M4T3, M4T4, M4T5, M4T6,
    M6T1, M6T2, M6T3, M6T4,
]