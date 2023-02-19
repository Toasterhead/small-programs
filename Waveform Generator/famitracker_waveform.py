#For use with Famitracker.

#Use the functions below to generate a waveform where amplitude is represented
#as a sequence of integers ranging from 0 - 15.

#Print the resulting waveform as a string with waveform_as_string(), then copy
#and paste the result into the sequence editor in the instrument editor window.

import copy, random

def waveform_as_string(waveform):

    """Converts the waveform as a list to a string that can be
    copied-and-pasted to the sequence editor."""

    s = ""
    
    for i in waveform: s += str(i) + " "

    s = s[:len(s) - 1]

    return s

def sustain(duration, volume):

    """Create a waveform that sustains at a consistent volume."""

    waveform = []

    for i in range(duration): waveform.append(volume)

    return waveform

def linear_fade(duration, start = 15, end = 0):

    """Create a waveform that decreases at a constant rate."""

    waveform = []

    for i in range(start, end, -1):
        for j in range(duration): waveform.append(i)

    return waveform

def logarithmic_fade(rate, start = 15, end = 0):

    """Create a waveform that decreases in volume at an increasingly slower
    rate. That is, a brief, sharp attack and a long sustained tail."""

    waveform = [start,]

    num = rate

    for i in range(start - 1, end, -1):
        num += rate
        for j in range(int(round(num))): waveform.append(i)

    return waveform

def linear_swell(duration, start = 1, end = 15):

    """Create a waveform that increases in volume at a constant rate."""

    waveform = []

    for i in range(start, end):
        for j in range(duration): waveform.append(i)

    return waveform

def attack(duration, decay, start = 15, end = 0):

    """Create a waveform with an attack that can be attached to the beginning
    of another waveform."""

    interval = start - end

    waveform = []

    for i in range(duration):
        waveform.append(int(end + (interval *(pow(decay, i)))))

    return waveform

def pre_attack(duration, swell, start = 1, end = 15):

    """Create a waveform with an increase in volume that can be attached to the
    beginning of an attack waveform."""

    interval = end - start

    waveform = []

    for i in range(duration):
        waveform.append(int(start + (interval - (interval * pow(rate, i)))))

    return waveform

def swell(duration, rate, start = 1, end = 15):

    """Create a waveform that begins with a swift, then gradual increase in
    volumne."""

    interval = end - start

    waveform = []

    for i in range(duration):
        waveform.append(int(start + (interval - (interval * pow(rate, i)))))

    return waveform

def apply_terminal(waveform):

    """Append a mute to the end of a waveform to ensure silence."""

    newWaveform = copy.deepcopy(waveform)
    newWaveform.append(0)

    return newWaveform
        
def apply_noise(waveform, variability):

    """Give the waveforme a gritty, unstable quality by rapidly and randomly
    alternating the volume."""

    newWaveform = []

    for i in range(len(waveform)):
        
        displacement = random.random() * variability
        displacement = -displacement if random.random() >= 0.5 else displacement
        
        value = int(waveform[i] + displacement + 0.5)
        value = 15  if value > 15   else value
        value = 0   if value < 0    else value
        
        newWaveform.append(value)

    return newWaveform
    
def apply_noise_proportionally(waveform, ratio):

    """Apply noise to a waveform proportionally to the current volume."""

    newWaveform = []

    for i in range(len(waveform)):

        variability = ratio * waveform[i]
        displacement = random.random() * variability
        displacement = -displacement if random.random() >= 0.5 else displacement
        
        value = int(waveform[i] + displacement + 0.5)
        value = 15  if value > 15   else value
        value = 0   if value < 0    else value
        
        newWaveform.append(value)

    return newWaveform

def apply_volume_pattern(waveform, pattern):

    """Alternate the volume of a waveform in the pattern provided as a list."""

    newWaveform = []

    for i in range(len(waveform)):
        newWaveform.append(int(waveform[i] + pattern[i % len(pattern)]))

    return newWaveform

def apply_volume_pattern_proportionally(waveform, pattern):

    """Alternate the volume of a waveform proportionally to the current
    volume."""

    newWaveform = []

    for i in range(len(waveform)):
        newWaveform.append(int(pattern[i % len(pattern)] * waveform[i]))

    return newWaveform
