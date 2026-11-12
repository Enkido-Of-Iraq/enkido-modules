using UnityEditor;
public static class TestMountedMovement
{
    [MenuItem("Enkidu/Tests/Enter play mode for traversal fixture")]
    public static void Run() { if (!EditorApplication.isPlaying) EditorApplication.EnterPlaymode(); }
}
