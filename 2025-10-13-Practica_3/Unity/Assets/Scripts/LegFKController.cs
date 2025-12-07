using UnityEngine;


/// <summary>
/// Controlador FK simple para una pierna con rotación en eje Z.
/// Muslo -> Gemelo -> Pie
/// </summary>
public class LegFKController : MonoBehaviour
{
    [Header("Asigna los huesos en orden")]
    public Transform muslo;    // root
    public Transform gemelo;   // mid
    public Transform pie;      // end
    public Transform punta;    // opcional

    [Header("Ángulos locales en Z (grados)")]
    public float musloZ = 0f;
    public float gemeloZ = 0f;
    public float pieZ = 0f;
    public float puntaZ = 0f;

    [Header("Runtime")]
    public bool aplicarCadaFrame = true;

    void Start()
    {
        if (!aplicarCadaFrame) AplicarFK();
    }

    void LateUpdate()
    {
        if (aplicarCadaFrame) AplicarFK();
    }

    public void AplicarFK()
    {
        if (muslo != null) muslo.localRotation = Quaternion.Euler(0f, 0f, musloZ);
        if (gemelo != null) gemelo.localRotation = Quaternion.Euler(0f, 0f, gemeloZ);
        if (pie != null) pie.localRotation = Quaternion.Euler(0f, 0f, pieZ);
        if (punta != null) punta.localRotation = Quaternion.Euler(0f, 0f, puntaZ);
    }

    public void SetPose(float mZ, float gZ, float pZ, float puZ = 0f)
    {
        musloZ = mZ; gemeloZ = gZ; pieZ = pZ; puntaZ = puZ;
        AplicarFK();
    }
}
