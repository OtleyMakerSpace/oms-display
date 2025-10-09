import os
import time
import glfw
from OpenGL.GL import *
from PIL import Image
import numpy as np
import logging


def load_shader_source(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def load_texture(path: str):
    img = Image.open(path).convert("RGB").transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    img_data = np.array(img, np.uint8)
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    return tex


def compile_shader(source: str, shader_type: int):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader))
    return shader


def create_program(vertex_src: str, fragment_src: str):
    vs = compile_shader(vertex_src, GL_VERTEX_SHADER)
    fs = compile_shader(fragment_src, GL_FRAGMENT_SHADER)
    program = glCreateProgram()
    glAttachShader(program, vs)
    glAttachShader(program, fs)
    glLinkProgram(program)
    if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(program))
    glDeleteShader(vs)
    glDeleteShader(fs)
    return program


def draw_transition(window, program, tex1, tex2, progress):
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(program)
    glUniform1f(glGetUniformLocation(program, "progress"), progress)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, tex1)
    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D, tex2)
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
    glfw.swap_buffers(window)
    glfw.poll_events()


class GlHelper:

    def __init__(self, images_paths: list[str]):
        self.logger = logging.getLogger()
        source_folder = "source"
        if not os.path.isdir(source_folder):
            raise ValueError("invalid source folder")
        vertex_path = os.path.join(source_folder, "vertex.glsl")
        self.vertex_src = load_shader_source(vertex_path)
        header_path = os.path.join(source_folder, "fragment-header.glsl")
        self.header_src = load_shader_source(header_path)
        footer_path = os.path.join(source_folder, "fragment-footer.glsl")
        self.footer_src = load_shader_source(footer_path)
        self.static_path = os.path.join(source_folder, "static.glsl")

        if not glfw.init():
            raise Exception("glfw can not be initialized")
        self.monitor = glfw.get_primary_monitor()
        self.mode = glfw.get_video_mode(self.monitor)
        glfw.window_hint(glfw.AUTO_ICONIFY, glfw.FALSE)
        self.window = glfw.create_window(self.mode.size.width, self.mode.size.height, "Slideshow", self.monitor, None)
        if not self.window:
            glfw.terminate()
            raise Exception("glfw window can not be created")
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
        glfw.make_context_current(self.window)
        width, height = glfw.get_framebuffer_size(self.window)
        self.logger.debug(f"window size is {width}x{height}")
        glViewport(0, 0, width, height)

        quad: np.ndarray = np.array([
            [-1, -1],
            [1, -1],
            [-1, 1],
            [1, 1],
        ], dtype=np.float32)

        glBindVertexArray(glGenVertexArrays(1))
        glBindBuffer(GL_ARRAY_BUFFER, glGenBuffers(1))
        glBufferData(GL_ARRAY_BUFFER, quad.nbytes, quad, GL_STATIC_DRAW)

        # preload the textures
        self.textures_dict = dict()
        for p in images_paths:
            self.logger.debug(f'preloading {p}')
            self.textures_dict[p] = load_texture(p)

    def show_image(self, image_path: str) -> None:
        self.logger.debug(f"displaying image: {image_path}")
        self.transition_images(image_path, image_path, self.static_path, 1)

    def transition_images(self, image1_path: str, image2_path: str, transition_path: str, duration: float) -> None:
        self.logger.debug(f"transitioning from {image1_path} to {image2_path} using {transition_path}")
        tex1 = self.textures_dict[image1_path]
        tex2 = self.textures_dict[image2_path]
        fragment_src: str = load_shader_source(transition_path)
        fragment_src = self.header_src + fragment_src + self.footer_src
        program = create_program(self.vertex_src, fragment_src)
        pos_loc = glGetAttribLocation(program, "pos")
        glEnableVertexAttribArray(pos_loc)
        glVertexAttribPointer(pos_loc, 2, GL_FLOAT, GL_FALSE, 0, None)
        glUseProgram(program)
        glUniform1i(glGetUniformLocation(program, "from"), 0)
        glUniform1i(glGetUniformLocation(program, "to"), 1)
        start_time: float = time.time()
        frame_count: int = 0
        while not glfw.window_should_close(self.window):
            elapsed: float = time.time() - start_time
            progress: float = min(elapsed / duration, 1.0)
            draw_transition(self.window, program, tex1, tex2, progress)
            frame_count += 1
            if progress >= 1.0:
                break
        fps = frame_count / duration
        self.logger.debug(f'{fps:.2f} fps')
        glDeleteProgram(program)
