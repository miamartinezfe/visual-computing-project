using UnityEngine;

public class ControlInfo : MonoBehaviour
{
    public GameObject infoCanvas; // Aquí guardaremos tu Canvas

    void OnMouseDown()
    {
        // Si el Canvas existe, invertimos su estado (si está on, se apaga; si está off, se prende)
        if (infoCanvas != null)
        {
            bool estado = infoCanvas.activeSelf;
            infoCanvas.SetActive(!estado);
        }
    }
}