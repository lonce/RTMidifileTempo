## Python MIDI File Player with Interactive Tempo

### Summary

The python script takes a MIDI file as a command line argument and "plays" it by sending out events at the proper time to a MIDI port. You will be given a choice of the MIDI port (from a list of those available on your system) to use when the program starts.

As the program plays, you can adjust its tempo by hitting or holding keys '1' through '9', which slows down playback for '1' through '4' and speeds up playback for '6' through '9'. The further from 5, the greater the effect.

### Note

On Windows, you'll probably see a synth port listed for the provided general MIDI synth. You can create other ports with [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) and by running a synthesizer such as FluidSynth that monitors the port you create. On Linux, you may not have ports available by default.

### Todo

On my 'todo' list is to write a midi file with the time modifications to that it can be played (or used for score following experiments ;-))