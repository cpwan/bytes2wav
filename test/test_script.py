import pytest
from bytes2wavbytes import convert
import wave

@pytest.fixture
def input_path():
    return "./test/example_input.mp4"

@pytest.fixture
def output_path():
    return "./test/example_output.wav"

def test_conversion_basic(input_path, output_path):
    """Test basic conversion from MP4 to WAV"""
    with open(input_path, "rb") as fin:
        input_bytes = fin.read()
        
    wav_bytes = convert(input_bytes)
    
    with open(output_path, "wb") as fout:
        fout.write(wav_bytes)
    
    # Validate output is a valid WAV file
    with open(output_path, "rb") as f:
        wf = wave.open(f)
        assert wf.getnchannels() > 0
        assert wf.getsampwidth() > 0
        assert wf.getframerate() > 0

def test_conversion_empty_input(output_path):
    """Test conversion with empty input"""
    input_bytes = b""
    
    try:
        wav_bytes = convert(input_bytes)
    except ValueError as e:
        assert "Input byte stream cannot be empty" in str(e)

def test_conversion_silent_input(output_path):
    """Test conversion with silent input"""
    # Create silent bytes (2 seconds of silence at 44.1kHz, 16-bit)
    silent_bytes = b'\x00' * 44100 * 2 * 2
    
    wav_bytes = convert(silent_bytes)
    
    with open(output_path, "wb") as fout:
        fout.write(wav_bytes)
    
    # Validate output
    with open(output_path, "rb") as f:
        wf = wave.open(f)
        assert wf.getnframes() == 44100 * 2
        assert wf.getframerate() == 44100
