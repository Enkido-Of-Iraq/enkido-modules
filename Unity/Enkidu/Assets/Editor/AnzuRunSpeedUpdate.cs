using UnityEditor;using UnityEngine;using UnityEditor.SceneManagement;using System.IO;
[InitializeOnLoad] public static class AnzuRunSpeedUpdate {
 static AnzuRunSpeedUpdate(){EditorApplication.delayCall+=Apply;EditorApplication.playModeStateChanged+=s=>{if(s==PlayModeStateChange.EnteredEditMode)EditorApplication.delayCall+=Apply;};}
 static void Apply(){const string path="Assets/Art/AnzuMountedV05/run-speed-9.done";if(File.Exists(path))return;var c=Object.FindFirstObjectByType<MountedAnzuController>();if(!c)return;c.runSpeed=9f;EditorUtility.SetDirty(c);if(EditorApplication.isPlaying)return;EditorSceneManager.MarkSceneDirty(c.gameObject.scene);EditorSceneManager.SaveScene(c.gameObject.scene);File.WriteAllText(path,"runSpeed=9 walkSpeed="+c.walkSpeed);Debug.Log("ANZU_RUN_SPEED_9_SAVED");}
}
