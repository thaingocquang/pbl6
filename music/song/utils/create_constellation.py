import numpy as np
from scipy import signal


def create_constellation(audio, Fs):
    """
    create_constellation ...
    """
    window_length_seconds = 0.5
    window_length_samples = int(window_length_seconds * Fs)
    window_length_samples += window_length_samples % 2
    num_peaks = 15
    amount_to_pad = window_length_samples - audio.size % window_length_samples
    song_input = np.pad(audio, (0, amount_to_pad))
    frequencies, times, stft = signal.stft(
        song_input, Fs, nperseg=window_length_samples, nfft=window_length_samples, return_onesided=True
    )
    constellation_map = []
    for time_idx, window in enumerate(stft.T):
        spectrum = abs(window)
        peaks, props = signal.find_peaks(spectrum, prominence=0, distance=200)
        n_peaks = min(num_peaks, len(peaks))
        largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]
        for peak in peaks[largest_peaks]:
            frequency = frequencies[peak]
            constellation_map.append([time_idx, frequency])
    return constellation_map