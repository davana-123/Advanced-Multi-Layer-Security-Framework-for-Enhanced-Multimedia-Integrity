import numpy as np
import scipy.io.wavfile as wavfile

def calculate_psnr_mse(original_file, encrypted_file):
    # Read the audio data from the files
    _, original_data = wavfile.read(original_file)
    _, encrypted_data = wavfile.read(encrypted_file)

    # Ensure that both audio files have the same length
    min_length = min(len(original_data), len(encrypted_data))
    original_data = original_data[:min_length]
    encrypted_data = encrypted_data[:min_length]

    # Calculate Mean Square Error (MSE)
    mse = np.mean((original_data - encrypted_data) ** 2)

    # Calculate Peak Signal-to-Noise Ratio (PSNR) in dB
    max_value = np.max(original_data)
    psnr = 20 * np.log10(max_value / np.sqrt(mse))

    return psnr, mse

if __name__ == "__main__":
    original_wav_file = "a.wav"
    encrypted_wav_file = "aa.wav"

    psnr_value, mse_value = calculate_psnr_mse(original_wav_file, encrypted_wav_file)
    print("PSNR:", psnr_value, "dB")
    print("MSE:", mse_value)
