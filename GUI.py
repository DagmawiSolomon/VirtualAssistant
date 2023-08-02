import pygame
import pyaudio
import numpy as np
import user_speech_recognition as Usr
import threading

class SoundVisualization:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 120, 215)
        self.LIGHT_BLUE = (13, 67, 110)
        self.RADIUS = 130
        self.MAX_RADIUS = 100
        self.MAX_GROWTH_FACTOR = 1.2
        self.INNER_RADIUS_1 = 90
        self.INNER_RADIUS_2 = 70
        self.FADE_OUT_RATE = 2500
        self.usr = Usr.SpeechRecognition()
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sound Visualization")
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                                  frames_per_buffer=self.CHUNK)

    def draw_circles(self, outer_radius, inner_radius_1, inner_radius_2, opacity):
        self.screen.fill(self.BLACK)
        pygame.draw.circle(self.screen, self.BLUE, (self.WIDTH // 2, self.HEIGHT // 2), outer_radius)
        inner_color = (self.LIGHT_BLUE[0], self.LIGHT_BLUE[1], self.LIGHT_BLUE[2], opacity)
        pygame.draw.circle(self.screen, inner_color, (self.WIDTH // 2, self.HEIGHT // 2), inner_radius_1)
        pygame.draw.circle(self.screen, inner_color, (self.WIDTH // 2, self.HEIGHT // 2), inner_radius_2)

    def map_sound_to_radius(self, sound_amplitude):
        outer_circle_radius = self.RADIUS + int(sound_amplitude * self.MAX_GROWTH_FACTOR)
        inner_circle_radius_1 = self.INNER_RADIUS_1
        inner_circle_radius_2 = self.INNER_RADIUS_2
        return outer_circle_radius, inner_circle_radius_1, inner_circle_radius_2

    
    def get_sound_amplitude(self, audio_data):
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        rms = np.sqrt(np.clip(np.mean(np.square(audio_array)), 0.0, None))
        return rms

    def run_visualization(self):
        running = True
        opacity = 255  
        speech_thread = threading.Thread(target=self.usr.recognize_speech)  
        speech_thread.start()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            data = self.stream.read(self.CHUNK)
            sound_amplitude = self.get_sound_amplitude(data)
            outer_circle_radius, inner_circle_radius_1, inner_circle_radius_2 = self.map_sound_to_radius(sound_amplitude)
            opacity = max(0, opacity - self.FADE_OUT_RATE)
            pygame.time.wait(60)
            self.draw_circles(outer_circle_radius, inner_circle_radius_1, inner_circle_radius_2, opacity)
            pygame.display.flip()
            pygame.time.wait(30)
        self.usr.is_listening = False  
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        pygame.quit()

if __name__ == "__main__":
    visualizer = SoundVisualization()
    visualizer.run_visualization()
