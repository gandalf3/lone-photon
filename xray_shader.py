import bge

cont = bge.logic.getCurrentController()

VertexShader = """
        varying vec4 texCoords; 
           // this is a varying variable in the vertex shader
         
        void main()
        {
            texCoords = gl_MultiTexCoord0;
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
         }

"""

FragmentShader = """
         varying vec4 texCoords; 
         uniform sampler2D textureUnit;
         
         void main()
         {
            vec2 longitudeLatitude = vec2(
                (atan(texCoords.y, texCoords.x) / 3.1415926 + 1.0) * 0.5,
                1.0 - acos(texCoords.z) / 3.1415926);


            gl_FragColor = texture2D(textureUnit, texCoords);
            gl_FragDepth = 0.0;
               // Here the fragment shader reads intput(!) from the 
               // varying variable. The red, gree, blue, and alpha 
               // component of the fragment color are set to the 
               // values in the varying variable. (The alpha 
               // component of the fragment doesn't matter here.) 
         }

"""

mesh = cont.owner.meshes[0]
for mat in mesh.materials:
    shader = mat.getShader()
    if shader != None:
        if not shader.isValid():
            shader.setSource(VertexShader, FragmentShader, 1)
            shader.setSampler('textureUnit', 0)
            