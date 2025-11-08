Shader "Custom/ProceduralURPHLSL"
{
    Properties
    {
        _Color("Base Color", Color) = (1, 1, 1, 1)
        _Frequency ("Wave Frequency", Range(0.1, 5)) = 1.0
        _Speed ("Wave Speed", Range(0.1, 5)) = 1.0
    }

    SubShader
    {
        Tags { "RenderType" = "Opaque" "RenderPipeline" = "UniversalPipeline" }
        LOD 100

        Pass
        {
            HLSLPROGRAM

            #pragma vertex vert
            #pragma fragment frag

            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            struct Attributes {
                float4 positionOS : POSITION; 
            };

            struct Varyings {
                float4 positionCS : SV_POSITION; 
                float3 positionWS : TEXCOORD0; // Vertex pos in World Space
            };

            CBUFFER_START(UnityPerMaterial)
                float4 _Color;
                float _Frequency;
                float _Speed;
            CBUFFER_END

            // Vertex Shader
            Varyings vert (Attributes input) {
                Varyings output;
                output.positionCS = TransformObjectToHClip(input.positionOS.xyz);
                output.positionWS = TransformObjectToWorld(input.positionOS.xyz);

                return output;
            }

            // Fragment Shader (Procedural Color Calc.)
            float4 frag (Varyings input) : SV_Target {
                
                float time = _Time.y; 

                // Color given time and pos.
                float r_comp = sin(input.positionWS.x * _Frequency + time * _Speed);
                float g_comp = sin(input.positionWS.z * _Frequency * 1.5 + time * _Speed * 1.5);
                
                // Mapping. Normalization from [-1, 1] -> [0, 1] coords..
                float intensityR = r_comp * 0.5 + 0.5;
                float intensityG = g_comp * 0.5 + 0.5;
                float intensityB = input.positionWS.y * 0.1 + 0.5; // BLUE -. Height
                
                float4 proceduralColor = float4(intensityR, intensityG, intensityB, 1.0);
                
                // Mix Procedural Color and Base Color
                return proceduralColor * _Color;
            }
            ENDHLSL
        }
    }
}
