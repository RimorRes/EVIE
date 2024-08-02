#version 140
#extension GL_ARB_explicit_attrib_location : enable

layout (location = 0) in vec3 vertexPosition;
layout (location = 1) in vec2 vertexTexCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 fragmentTexCoord;

void main() {
    gl_Position = projection * view * model * vec4(vertexPosition, 1.0);
    fragmentTexCoord = vertexTexCoord;
}