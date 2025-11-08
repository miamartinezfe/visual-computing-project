using UnityEngine;

public class CameraSwitch : MonoBehaviour
{
    private Camera mainCamera;
    void Start()
    {
        mainCamera = GetComponent<Camera>();
        mainCamera.orthographic = false; // DEFAULT = PERSPECTIVE

        // Initial Camera pos.
        transform.position = new Vector3(25, 20, -30);
        transform.rotation = Quaternion.Euler(30, -45, 0);

        mainCamera.fieldOfView = 80;
    }

    
    void Update()
    {
        // Camera Switch trigger = SpaceBar.
        if (Input.GetKeyDown(KeyCode.Space))
        {
            // Switch Projection
            mainCamera.orthographic = !mainCamera.orthographic;

            if (mainCamera.orthographic)
            {
                // Ortho adjustment. Size.
                mainCamera.orthographicSize = 18;
                Debug.Log("ORTHOGRAPHIC: (Sec. 11).");
            }
            else
            {
                Debug.Log("PERSPECTIVE:(Sec. 11).");
            }
        }
    }
}
