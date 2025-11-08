using UnityEngine;

public class ColorPalette : MonoBehaviour
{
    public GameObject[] objects; // Objetos a los que se aplicará la paleta
    public Color[] colors; // Paleta de colores

    void Start()
    {
        // Asignar colores a los objetos
        for (int i = 0; i < objects.Length && i < colors.Length; i++)
        {
            Renderer renderer = objects[i].GetComponent<Renderer>();
            if (renderer != null)
            {
                renderer.material.color = colors[i];
            }
        }
    }
}
