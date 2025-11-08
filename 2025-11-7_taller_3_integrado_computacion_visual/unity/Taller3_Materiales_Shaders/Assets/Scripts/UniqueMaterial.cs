using UnityEngine;

public class UniqueMaterial : MonoBehaviour
{
    private Material uniqueMaterial;

    void Start()
    {
        // Crear una instancia única del material
        Renderer renderer = GetComponent<Renderer>();
        if (renderer != null)
        {
            uniqueMaterial = Instantiate(renderer.sharedMaterial);
            renderer.material = uniqueMaterial;
        }
    }
}
