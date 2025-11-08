using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
public class ProceduralWaveGen : MonoBehaviour
{
    public int resolution = 100; // 100x100 vertices
    public float size = 10f; // Mesh Width & Height
    public float amplitude = 1.0f; // Max Wave Height (Amp)
    public float frequency = 0.5f; // Freq. Wave behaviour
    public float speed = 1.5f; // Prop. Speed.

    private Mesh mesh;
    private Vector3[] baseVertices;
    private Vector3[] currentVertices;

    void Start()
    {
        mesh = new Mesh();
        GetComponent<MeshFilter>().mesh = mesh;
        CreateProceduralMesh();

        baseVertices = mesh.vertices;
    }

    void CreateProceduralMesh()
    {
        // Vertex and UV gen
        List<Vector3> vertices = new List<Vector3>();
        List<Vector2> uvs = new List<Vector2>();

        for (int i = 0; i <= resolution; i++)
        {
            for (int j = 0; j <= resolution; j++)
            {
                // Vertex pos. Center at (0, 0, 0)
                float x = (float)i / resolution * size - size / 2f;
                float z = (float)j / resolution * size - size / 2f;
                vertices.Add(new Vector3(x, 0, z));
                uvs.Add(new Vector2((float)i / resolution, (float)j / resolution));
            }
        }
        mesh.vertices = vertices.ToArray();
        mesh.uv = uvs.ToArray();

        // Triangle gen -> Quad gen.
        List<int> triangles = new List<int>();
        for (int i = 0; i < resolution; i++)
        {
            for (int j = 0; j < resolution; j++)
            {
                int a = i * (resolution + 1) + j;
                int b = a + 1;
                int c = (i + 1) * (resolution + 1) + j;
                int d = c + 1;

                // Quad triangulation
                triangles.Add(a); triangles.Add(c); triangles.Add(b);
                triangles.Add(b); triangles.Add(c); triangles.Add(d);
            }
        }
        mesh.triangles = triangles.ToArray();
        mesh.RecalculateNormals();
    }

    void Update()
    {
        if (baseVertices == null || baseVertices.Length == 0) return;

        currentVertices = mesh.vertices;

        for (int i = 0; i < currentVertices.Length; i++)
        {
            Vector3 basePos = baseVertices[i];

            // Wave behaviour. (Sine function used)
            float waveY = amplitude * Mathf.Sin(
                (basePos.x * frequency) + (Time.time * speed)
            );

            // New Height recalc.
            currentVertices[i] = new Vector3(basePos.x, waveY, basePos.z);
        }

        mesh.vertices = currentVertices;
        mesh.RecalculateNormals();
        mesh.RecalculateBounds();

    }
}
