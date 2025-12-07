using UnityEngine;

public class Carrera200m_FinalExtra_Ajustado : MonoBehaviour
{
    public Transform objetoSalida;
    public Transform objetoPicoCurva;
    public Transform objetoLlegadaCurva;
    public Transform objetoMeta;
    public float velocidad = 0.25f;
    [Range(20, 80)] public int puntosCurva = 50;

    private Vector3[] ruta = null;
    private int puntoActual = 0;
    private bool recorriendoRecta = false;
    private bool corriendoExtra = false;
    private float timerExtra = 0f;
    private Vector3 direccionExtra = Vector3.zero;

    void Start()
    {
        // Toma las posiciones de cada objeto
        ruta = GenerarRutaMediaCircunferencia(
                   objetoSalida.position,
                   objetoPicoCurva.position,
                   objetoLlegadaCurva.position,
                   puntosCurva);
        transform.position = objetoSalida.position;
    }

    void Update()
    {
        if (ruta == null) return;
        float umbral = Mathf.Max(0.03f, velocidad * 1.5f);

        if (!recorriendoRecta)
        {
            if (puntoActual < ruta.Length)
            {
                MoverYRotar(ruta[puntoActual], umbral);
                if (Vector3.Distance(transform.position, ruta[puntoActual]) < umbral)
                    puntoActual++;
            }
            else
            {
                recorriendoRecta = true;
            }
        }
        else if (!corriendoExtra)
        {
            MoverYRotar(objetoMeta.position, umbral);
            if (Vector3.Distance(transform.position, objetoMeta.position) < umbral)
            {
                direccionExtra = (objetoMeta.position - ruta[ruta.Length - 1]).normalized;
                corriendoExtra = true;
                timerExtra = 0f;
            }
        }
        else
        {
            timerExtra += Time.deltaTime;
            if (timerExtra <= 2f)
            {
                transform.position += direccionExtra * velocidad * Time.deltaTime;
                if (direccionExtra.sqrMagnitude > 0.001f)
                {
                    Quaternion rot = Quaternion.LookRotation(direccionExtra);
                    transform.rotation = Quaternion.Slerp(transform.rotation, rot, 6f * Time.deltaTime);
                }
            }
            else
            {
                enabled = false; // Detiene el script por completo
            }
        }
    }

    void MoverYRotar(Vector3 destino, float umbral)
    {
        Vector3 direccion = destino - transform.position;
        direccion.y = 0;
        if (direccion.sqrMagnitude > umbral * umbral)
        {
            Quaternion rotacion = Quaternion.LookRotation(direccion);
            transform.rotation = Quaternion.Slerp(transform.rotation, rotacion, 6f * Time.deltaTime);
        }
        transform.position = Vector3.MoveTowards(transform.position, destino, velocidad * Time.deltaTime);
    }

    // Ahora acepta las posiciones de los objetos en vez de coordenadas fijas
    Vector3[] GenerarRutaMediaCircunferencia(Vector3 inicio, Vector3 medio, Vector3 fin, int cantidadPuntos)
    {
        Vector2 a = new Vector2(inicio.x, inicio.z);
        Vector2 b = new Vector2(medio.x, medio.z);
        Vector2 c = new Vector2(fin.x, fin.z);
        float d = 2 * (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y));
        Vector2 centro2D = new Vector2(
            (a.sqrMagnitude * (b.y - c.y) + b.sqrMagnitude * (c.y - a.y) + c.sqrMagnitude * (a.y - b.y)) / d,
            (a.sqrMagnitude * (c.x - b.x) + b.sqrMagnitude * (a.x - c.x) + c.sqrMagnitude * (b.x - a.x)) / d
        );
        float radio = Vector2.Distance(a, centro2D);

        float ang0 = Mathf.Atan2(a.y - centro2D.y, a.x - centro2D.x);
        float ang1 = Mathf.Atan2(c.y - centro2D.y, c.x - centro2D.x);

        Vector3[] puntos = new Vector3[cantidadPuntos + 1];
        for (int i = 0; i <= cantidadPuntos; i++)
        {
            float t = i / (float)cantidadPuntos;
            float ang = Mathf.Lerp(ang0, ang1, t);
            Vector2 pos = centro2D + (new Vector2(Mathf.Cos(ang), Mathf.Sin(ang)) * radio);
            puntos[i] = new Vector3(pos.x, 0f, pos.y);
        }
        return puntos;
    }
}
