#version 140
#extension GL_ARB_explicit_attrib_location : enable

in vec4 fragmentColor;

out vec4 screenColor;

void main() {
    screenColor = fragmentColor;
}