using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;
using System.IO;
[InitializeOnLoad] public static class AnzuOverheadSun {
 static AnzuOverheadSun(){EditorApplication.delayCall+=Apply;EditorApplication.playModeStateChanged+=state=>{if(state==PlayModeStateChange.EnteredEditMode)EditorApplication.delayCall+=Apply;};}
 static void Apply(){
 const string marker="Assets/Art/AnzuMountedV05/overhead-sun.done";
 if(File.Exists(marker)||EditorApplication.isPlayingOrWillChangePlaymode)return;
 if(UnityEngine.SceneManagement.SceneManager.GetActiveScene().name!="AnzuDesert")return;
 var sunObject=GameObject.Find("Desert sun");if(!sunObject)sunObject=new GameObject("Desert sun");
 var sun=sunObject.GetComponent<Light>();if(!sun)sun=sunObject.AddComponent<Light>();
 sun.type=LightType.Directional;sun.transform.position=new Vector3(0,12,0);sun.transform.rotation=Quaternion.Euler(68,-30,0);
 sun.color=new Color(1f,.92f,.78f);sun.intensity=2.2f;sun.shadows=LightShadows.Soft;sun.shadowStrength=.8f;sun.shadowBias=.04f;sun.shadowNormalBias=.3f;
 RenderSettings.sun=sun;RenderSettings.ambientMode=UnityEngine.Rendering.AmbientMode.Trilight;
 RenderSettings.ambientSkyColor=new Color(.52f,.62f,.72f);RenderSettings.ambientEquatorColor=new Color(.55f,.48f,.36f);RenderSettings.ambientGroundColor=new Color(.27f,.20f,.12f);
 EditorSceneManager.MarkSceneDirty(UnityEngine.SceneManagement.SceneManager.GetActiveScene());EditorSceneManager.SaveScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene());
 File.WriteAllText(marker,"Warm overhead sun applied");SetupAnzuDesert.Open();Debug.Log("ANZU_OVERHEAD_SUN_APPLIED");
 }
}
