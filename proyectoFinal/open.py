import pygame
import numpy
from obj import *
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import glm

pygame.init()
screen = pygame.display.set_mode((1200, 720), pygame.OPENGL | pygame.DOUBLEBUF)
glClearColor(0.1, 0.2, 0.5, 1.0)
glEnable(GL_DEPTH_TEST)
clock = pygame.time.Clock()

vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 ccolor;

uniform mat4 theMatrix;
uniform int clock;
uniform int shade;
uniform vec3 light;

out vec3 mycolor;

void main() 
{
  gl_Position = theMatrix * vec4(position, 1);
  float intensity = dot(ccolor, normalize(light - position));
  
  if (shade == 1)
  {
    if (mod(clock/10, 11) == 0) 
    {
      mycolor = ccolor.xyz;
    }
    else if (mod(clock/10, 7) == 0) 
    {
      mycolor = ccolor.xzy;
    }
    else if (mod(clock/10, 5) == 0) 
    {
      mycolor = ccolor.yxz;
    }
    else if (mod(clock/10, 3) == 0) 
    {
      mycolor = ccolor.yzx;
    }
    else if (mod(clock/10, 2) == 0) 
    {
      mycolor = ccolor.zxy;
    }
    else 
    {
      mycolor = ccolor.ztx;
    }
  }
  else if (shade == 2)
  {
    vec3 poscolor = vec3(abs(position.x), abs(position.y), abs(position.z));
    if (mod(clock/10, 2) == 0) 
    {
      mycolor = poscolor * intensity;
    }
    else
    {
      mycolor = poscolor;
    }
  }
  else
  {
    vec3 tempcolor = vec3(0.8f, 0.8f, 0.8f);
    float intent = intensity;
    if (mod(clock/10, 2) == 0) 
    {
      intent = 1.0f - intensity;
    }
    mycolor = tempcolor * intent;
  }
}
"""

fragment_shader = """
#version 460
layout(location = 0) out vec4 fragColor;
in vec3 mycolor;

void main()
{
  fragColor = vec4(mycolor, 1.0f);
}
"""

cvs = compileShader(vertex_shader, GL_VERTEX_SHADER)
cfs = compileShader(fragment_shader, GL_FRAGMENT_SHADER)

shader = compileProgram(cvs, cfs)

mesh = Obj('./box.obj')

vertex_data = numpy.hstack((
  numpy.array(mesh.vertices, dtype=numpy.float32),
  numpy.array(mesh.normals, dtype=numpy.float32),
)).flatten()

index_data = numpy.array([[vertex[0] - 1 for vertex in face] for face in mesh.faces], dtype=numpy.uint32).flatten()

vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)
glVertexAttribPointer(
  0, # location
  3, # size
  GL_FLOAT, # tipo
  GL_FALSE, # normalizados
  4 * 6, # stride
  ctypes.c_void_p(0)
)
glEnableVertexAttribArray(0)

element_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

glVertexAttribPointer(
  1, # location
  3, # size
  GL_FLOAT, # tipo
  GL_FALSE, # normalizados
  4 * 6, # stride
  ctypes.c_void_p(4 * 3)
)
glEnableVertexAttribArray(1)

glUseProgram(shader)

def render(rotate=(0, 0, 0), translate=0):
  i = glm.mat4(1)

  translate = glm.translate(i, glm.vec3(0, 0, translate))
  rotatex = glm.rotate(i, glm.radians(rotate[0]), glm.vec3(1, 0, 0))
  rotatey = glm.rotate(i, glm.radians(rotate[1]), glm.vec3(0, 1, 0))
  rotatez = glm.rotate(i, glm.radians(rotate[2]), glm.vec3(0, 0, 1))
  rotate = rotatex * rotatey * rotatez
  scale = glm.scale(i, glm.vec3(1, 1, 1))

  model = translate * rotate * scale
  view = glm.lookAt(glm.vec3(0, 0, 10), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
  projection = glm.perspective(glm.radians(45), 1200/720, 0.1, 1000.0)

  theMatrix = projection * view * model

  glUniformMatrix4fv(
    glGetUniformLocation(shader, 'theMatrix'),
    1,
    GL_FALSE,
    glm.value_ptr(theMatrix)
  )

glViewport(0, 0, 1200, 720)
glUniform3f(
  glGetUniformLocation(shader, 'light'),
  0, 0, 10
)

clocki=0
shade=1
rotate=[0, 0, 0] 
translate=0
running = True
while running:
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

  render(rotate, translate)
  clocki += 1
  glUniform1i(
    glGetUniformLocation(shader, 'clock'),
    clocki
  )
  glUniform1i(
    glGetUniformLocation(shader, 'shade'),
    shade,
  )

  glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, None)

  pygame.display.flip()
  clock.tick(15)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_e:
        if (translate < 5): translate += 1
      if event.key == pygame.K_d:
        translate -= 1

      if event.key == pygame.K_q:
        rotate[0] -= 45
      if event.key == pygame.K_w:
        rotate[0] += 45
      if event.key == pygame.K_a:
        rotate[1] -= 45
      if event.key == pygame.K_s:
        rotate[1] += 45
      if event.key == pygame.K_z:
        rotate[2] -= 45
      if event.key == pygame.K_x:
        rotate[2] += 45

      if event.key == pygame.K_1:
        shade = 1
      if event.key == pygame.K_2:
        shade = 2
      if event.key == pygame.K_3:
        shade = 3