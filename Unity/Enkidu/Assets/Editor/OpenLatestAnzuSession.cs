using UnityEditor;
using UnityEditor.SceneManagement;
[InitializeOnLoad]
public static class OpenLatestAnzuSession {
    static OpenLatestAnzuSession() { EditorApplication.delayCall += Open; }
    static void Open() {
        if (SessionState.GetBool("OpenLatestAnzuSession20261110", false)) return;
        if (EditorApplication.isCompiling || EditorApplication.isUpdating) { EditorApplication.delayCall += Open; return; }
        if (EditorApplication.isPlayingOrWillChangePlaymode) return;
        SessionState.SetBool("OpenLatestAnzuSession20261110", true);
        if (EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo())
            EditorSceneManager.OpenScene("Assets/Scenes/AnzuDesert.unity");
    }
}
