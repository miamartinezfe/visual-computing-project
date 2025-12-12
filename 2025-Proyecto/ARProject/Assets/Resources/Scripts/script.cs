// 12/11/2025 AI-Tag
// This was created with the help of Assistant, a Unity Artificial Intelligence product.

using UnityEngine;
using UnityEngine.UI;

public class OrganDescriptionUI : MonoBehaviour
{
    public Text descriptionText; // Reference to the UI Text element

    public void UpdateDescription(string newDescription)
    {
        descriptionText.text = newDescription;
    }

    public void ClearDescription()
    {
        descriptionText.text = ""; // Clear the text
    }
}