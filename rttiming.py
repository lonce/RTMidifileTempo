import mido
import time
import keyboard
import argparse
import threading
import rtmidi

# Global variables to manage tempo
current_tempo_factor = 1.0  # Start with no tempo change
stop_tempo_thread = False

def adjust_tempo(adjustment_factor):
    """Adjusts the tempo factor based on the adjustment factor."""
    global current_tempo_factor
    current_tempo_factor *= adjustment_factor

def set_tempo_to_normal():
    """Resets the tempo factor to 1.0 (normal speed)."""
    global current_tempo_factor
    current_tempo_factor = 1.0

def monitor_tempo_keys():
    """Continuously checks for tempo adjustment keys."""
    while True:
        if keyboard.is_pressed('1'):
            adjust_tempo(1.02)  # Increase tempo by 2%
            time.sleep(0.05)
        elif keyboard.is_pressed('9'):
            adjust_tempo(0.98)  # Decrease tempo by 2%
            time.sleep(0.05)
        elif keyboard.is_pressed('2'):
            adjust_tempo(1.015)  # Increase tempo by 1.5%
            time.sleep(0.05)
        elif keyboard.is_pressed('8'):
            adjust_tempo(0.985)  # Decrease tempo by 1.5%
            time.sleep(0.05)
        elif keyboard.is_pressed('3'):
            adjust_tempo(1.01)  # Increase tempo by 1%
            time.sleep(0.05)
        elif keyboard.is_pressed('7'):
            adjust_tempo(0.99)  # Decrease tempo by 1%
            time.sleep(0.05)
        elif keyboard.is_pressed('4'):
            adjust_tempo(1.005)  # Increase tempo by 0.5%
            time.sleep(0.05)
        elif keyboard.is_pressed('6'):
            adjust_tempo(0.995)  # Decrease tempo by 0.5%
            time.sleep(0.05)
        elif keyboard.is_pressed('5'):
            set_tempo_to_normal()  # Reset tempo to normal
            time.sleep(0.05)
        time.sleep(0.01)  # Small delay to avoid busy-waiting

def play_midi(midi_file, midi_out):
    global current_tempo_factor

    # Load the MIDI file
    mid = mido.MidiFile(midi_file)
    
    paused = True
    current_time = 0
    print("Press 'p' to start playing the MIDI stream.")

    # Start a thread to monitor tempo adjustment keys
    threading.Thread(target=monitor_tempo_keys, daemon=True).start()

    while True:
        # Wait until the user presses 'p' to start playback
        if paused:
            if keyboard.is_pressed('p'):
                paused = not paused
                if not paused:
                    print("Playing")
                    start_time = time.time() - current_time  # Adjust start time
                time.sleep(0.3)  # Debounce delay
            time.sleep(0.01)
            continue

        # Iterate over MIDI messages
        for msg in mid:
            # Handle the play/pause toggle
            if keyboard.is_pressed('p'):
                paused = not paused
                if paused:
                    print("Paused")
                else:
                    print("Playing")
                    start_time = time.time() - current_time  # Adjust start time
                time.sleep(0.3)  # Debounce delay

            # If paused, wait until unpaused
            while paused:
                if keyboard.is_pressed('p'):
                    paused = not paused
                    if not paused:
                        start_time = time.time() - current_time  # Adjust start time
                        print("Playing")
                    else:
                        print("Paused")
                    time.sleep(0.3)  # Debounce delay
                time.sleep(0.01)
            
            # Calculate elapsed time since start
            current_time = time.time() - start_time
            
            # Adjust the time to wait for the message based on the tempo factor
            time.sleep(msg.time * current_tempo_factor)
            
            # Send the message to the output port if it's not a meta message
            if not msg.is_meta:
                midi_out.send_message(msg.bytes())

        # Allow notes to ring out before final termination
        print("Allowing notes to decay...")
        time.sleep(2)  # Adjust this value as needed to allow sufficient decay time
        
        # Send all notes off or sustain off (if necessary)
        midi_out.send_message([0xB0, 0x7B, 0x00])  # All Notes Off (Control Change)
        midi_out.send_message([0xB0, 0x40, 0x00])  # Sustain Off (Control Change)

        # Stop after playing all messages
        break

def main():
    parser = argparse.ArgumentParser(description="Stream a MIDI file to FluidSynth with play/pause functionality.")
    parser.add_argument('midi_file', type=str, help="Path to the MIDI file")
    args = parser.parse_args()

    # Initialize rtmidi and list available output ports
    midi_out = rtmidi.MidiOut()
    available_ports = midi_out.get_ports()

    if not available_ports:
        print("No MIDI output ports available.")
        return

    print("Available MIDI output ports:")
    for i, port in enumerate(available_ports):
        print(f"{i}: {port}")

    port_index = int(input("Select the MIDI output port number: "))
    midi_out.open_port(port_index)

    try:
        play_midi(args.midi_file, midi_out)
    finally:
        midi_out.close_port()

if __name__ == "__main__":
    main()
