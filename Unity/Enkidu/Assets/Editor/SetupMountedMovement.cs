using UnityEditor;
public static class SetupMountedMovement
{
    [MenuItem("Enkidu/Legacy/Run old mounted setup")]
    public static void Install() => UnityEngine.Debug.LogWarning("Legacy load-time setup is retired. Use Enkidu/Configure Mounted Slice.");
}
