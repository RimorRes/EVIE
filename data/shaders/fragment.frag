#version 140
#extension GL_ARB_explicit_attrib_location : enable

in vec4 fragmentColor;
in vec2 fragmentTexCoord;

out vec4 screenColor;

uniform sampler2D imageTexture;
uniform vec4 baseColor;

void main() {
    screenColor = baseColor * texture(imageTexture, fragmentTexCoord );
}