#version 330 core
out vec4 FragColor;

in vec2 TexCoord;
in vec3 Normal;
in vec3 FragPos;

uniform sampler2D ourTexture;

uniform vec3 lightDirection; // Direction from fragment TO light source (normalized)
uniform vec3 lightColor;     // Color of the light
uniform vec3 viewPos;        // Camera position (for specular)

uniform float ambientStrength;
uniform float diffuseStrength;
uniform float specularStrength;
uniform float shininess;

void main()
{
    // Texture sampling
    vec4 texColor = texture(ourTexture, TexCoord);

    // Normalize interpolated normal
    vec3 norm = normalize(Normal);
    
    // Light direction (from fragment to light source)
    vec3 lightDir = normalize(lightDirection); 

    // 1. Ambient lighting
    vec3 ambient = ambientStrength * lightColor * texColor.rgb;

    // 2. Diffuse lighting
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor * texColor.rgb;

    // 3. Specular lighting
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm); // Reflect light direction
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    vec3 specular = specularStrength * spec * lightColor * texColor.rgb;

    // Final result
    FragColor = vec4(ambient + diffuse + specular, texColor.a);
}