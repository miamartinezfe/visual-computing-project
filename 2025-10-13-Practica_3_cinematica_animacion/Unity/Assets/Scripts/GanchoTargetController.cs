using UnityEngine;

public class GanchoTargetController : MonoBehaviour
{
    [Header("Límites de Movimiento")]
    [SerializeField] private float minX = -12f;
    [SerializeField] private float maxX = -8f;
    [SerializeField] private float minY = 4f;
    [SerializeField] private float maxY = 9f;
    
    [Header("Configuración de Velocidad")]
    [SerializeField] private float speed = 2f;
    
    private Vector3 targetPosition;
    private float constantZ;

    void Start()
    {
        // Guardar la posición Z inicial como constante
        constantZ = transform.position.z;
        targetPosition = transform.position;
    }

    void Update()
    {
        // Control con teclado (opcional)
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        
        // Calcular nueva posición objetivo
        targetPosition.x += horizontal * speed * Time.deltaTime;
        targetPosition.y += vertical * speed * Time.deltaTime;
        
        // Aplicar límites con Mathf.Clamp
        targetPosition.x = Mathf.Clamp(targetPosition.x, minX, maxX);
        targetPosition.y = Mathf.Clamp(targetPosition.y, minY, maxY);
        targetPosition.z = constantZ; // Z permanece constante
        
        // Aplicar la posición
        transform.position = targetPosition;
    }
    
    // Método público para mover a una posición específica
    public void MoverA(float x, float y)
    {
        targetPosition.x = Mathf.Clamp(x, minX, maxX);
        targetPosition.y = Mathf.Clamp(y, minY, maxY);
        targetPosition.z = constantZ;
        transform.position = targetPosition;
    }
    
    // Método para movimiento suave a una posición
    public void MoverSuaveA(float x, float y, float velocidad)
    {
        Vector3 destino = new Vector3(
            Mathf.Clamp(x, minX, maxX),
            Mathf.Clamp(y, minY, maxY),
            constantZ
        );
        StartCoroutine(MovimientoSuave(destino, velocidad));
    }
    
    private System.Collections.IEnumerator MovimientoSuave(Vector3 destino, float velocidad)
    {
        while (Vector3.Distance(transform.position, destino) > 0.01f)
        {
            transform.position = Vector3.Lerp(
                transform.position, 
                destino, 
                velocidad * Time.deltaTime
            );
            yield return null;
        }
        transform.position = destino;
    }
}
