using UnityEngine;using UnityEditor;using UnityEditor.SceneManagement;using System.IO;
[InitializeOnLoad]public static class EnkiduSkinFill{
static EnkiduSkinFill(){EditorApplication.delayCall+=Run;}
static void Run(){if(EditorApplication.isCompiling||EditorApplication.isUpdating){EditorApplication.delayCall+=Run;return;}if(EditorApplication.isPlayingOrWillChangePlaymode||File.Exists("Assets/Art/EnkiduRunning/skin_fill.done"))return;
var root=GameObject.Find("Enkidu — Ground Running");if(!root)return;
var go=GameObject.Find("Soft front fill")??new GameObject("Soft front fill");var l=go.GetComponent<Light>();if(!l)l=go.AddComponent<Light>();l.type=LightType.Directional;l.color=new Color(1,.95f,.88f);l.intensity=.7f;l.shadows=LightShadows.None;go.transform.rotation=Quaternion.Euler(35,180,0);
EditorSceneManager.MarkSceneDirty(root.scene);EditorSceneManager.SaveScene(root.scene);
var c=Camera.main;var pos=c.transform.position;var rot=c.transform.rotation;c.transform.position=new Vector3(3.7f,1.2f,2.6f);c.transform.LookAt(new Vector3(2.8f,.75f,0));
var rt=new RenderTexture(900,900,24);c.targetTexture=rt;c.Render();RenderTexture.active=rt;var t=new Texture2D(900,900,TextureFormat.RGB24,false);t.ReadPixels(new Rect(0,0,900,900),0,0);t.Apply();File.WriteAllBytes("/private/tmp/enkidu_skin_final.png",t.EncodeToPNG());c.targetTexture=null;RenderTexture.active=null;Object.DestroyImmediate(t);Object.DestroyImmediate(rt);c.transform.SetPositionAndRotation(pos,rot);File.WriteAllText("Assets/Art/EnkiduRunning/skin_fill.done","Corrected linear color conversion; soft front fill 0.7; original rig geometry retained.");}}
