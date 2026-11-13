using UnityEngine;

public sealed class MobileControlsVisibility : MonoBehaviour
{
    private void Awake()
    {
        if (!Application.isMobilePlatform)
            gameObject.SetActive(false);
    }
}
