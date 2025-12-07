using UnityEngine;

public class CamaraCarreraLateral : MonoBehaviour
{
    public Transform atleta;
    public float altura = 7f;
    public float offsetFrontal = 15f; // Ahora sobre Z para quede “paralela” a la recta de 100m

    void LateUpdate()
    {
        if (atleta == null) return;

        // Posición de cámara: paralela a la línea de meta sobre el eje Z
        Vector3 pos = atleta.position;
        pos.z += offsetFrontal; // Ahora cámara frente al corredor, alineada a la recta principal
        pos.y += altura;
        transform.position = pos;

        // “LookAt” sobre la dirección principal de la pista, manteniendo altura
        Vector3 mirar = atleta.position;
        mirar.y = pos.y;
        transform.LookAt(mirar);
    }
}