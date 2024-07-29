#version 140
#extension GL_ARB_explicit_attrib_location : enable

vec4 parseRGBA(uint rgba) {
    float r = float((rgba >> 24) & 0xFFU) / 255.0;
    float g = float((rgba >> 16) & 0xFFU) / 255.0;
    float b = float((rgba >> 8) & 0xFFU) / 255.0;
    float a = float(rgba & 0xFFU) / 255.0;
    return vec4(r, g, b, a);
}

layout (location = 0) in vec3 vertexPosition;
layout (location = 1) in uint vertexColor;
layout (location = 2) in vec2 vertexTexCoord;

out vec4 fragmentColor;
out vec2 fragmentTexCoord;

void main() {
    gl_Position = vec4(vertexPosition, 1.0);
    fragmentColor = parseRGBA(vertexColor);
    fragmentTexCoord = vertexTexCoord;
}