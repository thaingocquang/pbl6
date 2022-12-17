def create_hashes(constellation_map, song_id=None):
    hashes = {}
    upper_frequency = 23_000
    frequency_bits = 10
    for idx, (time, freq) in enumerate(constellation_map):
        for other_time, other_freq in constellation_map[idx : idx + 100]:
            diff = other_time - time
            if diff <= 1 or diff > 10:
                continue
            freq_binned = freq / upper_frequency * (2 ** frequency_bits)
            other_freq_binned = other_freq / upper_frequency * (2 ** frequency_bits)
            hash = int(freq_binned) | (int(other_freq_binned) << 10) | (int(diff) << 20)
            hashes[hash] = (time, song_id)
    return hashes