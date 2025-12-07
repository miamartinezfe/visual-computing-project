using UnityEngine;

public class WalkCycle : MonoBehaviour
{
    [Header("Referencia al controlador FK")]
    public LegFKController legController;

    [Header("Frecuencia del paso (Hz)")]
    public float stepFrequency = 1.5f;

    [Header("Amplitud de movimiento (grados)")]
    public float musloAmplitude = 30f;
    public float gemeloAmplitude = 25f;
    public float pieAmplitude = 15f;

    [Header("Desfase entre articulaciones (radianes)")]
    public float gemeloPhase = Mathf.PI / 2;
    public float piePhase = Mathf.PI;

    private float timeCounter = 0f;

    
    void Update()
    {
        timeCounter += Time.deltaTime * stepFrequency * 2 * Mathf.PI;

        float musloZ = Mathf.Sin(timeCounter) * musloAmplitude;
    float rawGemelo = Mathf.Sin(timeCounter + gemeloPhase);
    float pieZ = Mathf.Sin(timeCounter + piePhase) * pieAmplitude;

    // --- nuevo control de rodilla ---
    float gemeloZ;
    if (rawGemelo < 0)
    {
        // Flexión (atrás)
        gemeloZ = rawGemelo * gemeloAmplitude;
    }
    else
    {
        // Extensión (adelante) → limitar a 0
        gemeloZ = 0;
    }

    legController.SetPose(musloZ, gemeloZ, pieZ);

    }
}
