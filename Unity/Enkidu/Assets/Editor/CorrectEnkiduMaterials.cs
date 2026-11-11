using UnityEngine;using UnityEditor;using UnityEditor.SceneManagement;using System;using System.IO;using System.Linq;
[InitializeOnLoad] public static class CorrectEnkiduMaterials {
[Serializable] public class Item {public string name;public Color[] colors;}
[Serializable] public class Data {public Item[] items;}
static CorrectEnkiduMaterials(){EditorApplication.delayCall+=Run;}
static void Run(){
if(EditorApplication.isCompiling||EditorApplication.isUpdating){EditorApplication.delayCall+=Run;return;}
if(EditorApplication.isPlayingOrWillChangePlaymode||File.Exists("Assets/Art/EnkiduRunning/material_fix_v3.done"))return;
var root=GameObject.Find("Enkidu — Ground Running");if(!root)return;
var old=root;old.name="Enkidu — previous import (disabled)";old.SetActive(false);
root=UnityEngine.Object.Instantiate(AssetDatabase.LoadAssetAtPath<GameObject>("Assets/Art/EnkiduRunning/Enkidu_Running.fbx"));root.name="Enkidu — Ground Running";
var originalMats=old.GetComponentsInChildren<Renderer>(true).ToDictionary(r=>r.name,r=>r.sharedMaterials);
foreach(var r in root.GetComponentsInChildren<Renderer>())if(originalMats.ContainsKey(r.name))r.sharedMaterials=originalMats[r.name];
var anim=root.GetComponent<Animation>();anim.clip=old.GetComponent<Animation>().clip;anim.wrapMode=WrapMode.Loop;anim.playAutomatically=true;
var data=JsonUtility.FromJson<Data>(File.ReadAllText("Assets/Art/EnkiduRunning/colors.json"));int fixedCount=0,missing=0;
foreach(var r in root.GetComponentsInChildren<Renderer>(true)){
var item=Array.Find(data.items,i=>i.name==r.name);if(item==null){missing++;continue;}
var ms=r.sharedMaterials;
for(int i=0;i<ms.Length&&i<item.colors.Length;i++){
var m=ms[i];if(!m)continue;
// Blender base-color components are linear. Unity color properties are authored in sRGB.
var c=item.colors[i].gamma;c.a=1;m.SetColor("_BaseColor",c);m.SetFloat("_Metallic",0);
var n=r.name.ToLowerInvariant();bool skin=n.Contains("face")||n.Contains("arm")||n.Contains("palm")||n.Contains("finger")||n.Contains("thumb")||n.Contains("ear");
m.SetFloat("_Smoothness",skin?.35f:.22f);EditorUtility.SetDirty(m);fixedCount++;}
}
root.transform.localScale=Vector3.one;root.transform.position=new Vector3(2.8f,.02f,0);
var clip=root.GetComponent<Animation>().clip;clip.SampleAnimation(root,.2f);
EditorSceneManager.MarkSceneDirty(root.scene);EditorSceneManager.SaveScene(root.scene);AssetDatabase.SaveAssets();
var cam=Camera.main;var pos=cam.transform.position;var rot=cam.transform.rotation;
cam.transform.position=new Vector3(4.5f,2f,5f);cam.transform.LookAt(new Vector3(2.8f,1.1f,0));
var rt=new RenderTexture(900,900,24);cam.targetTexture=rt;cam.Render();RenderTexture.active=rt;var tx=new Texture2D(900,900,TextureFormat.RGB24,false);tx.ReadPixels(new Rect(0,0,900,900),0,0);tx.Apply();File.WriteAllBytes("/private/tmp/enkidu_material_fixed_v3.png",tx.EncodeToPNG());cam.targetTexture=null;RenderTexture.active=null;UnityEngine.Object.DestroyImmediate(tx);UnityEngine.Object.DestroyImmediate(rt);cam.transform.SetPositionAndRotation(pos,rot);
if(SceneView.lastActiveSceneView)SceneView.lastActiveSceneView.LookAt(new Vector3(2.8f,1.3f,0),Quaternion.Euler(8,200,0),3.8f);
Selection.activeGameObject=root;
File.WriteAllText("Assets/Art/EnkiduRunning/material_fix_v3.done","materials="+fixedCount+" unmatchedRenderers="+missing+" colorSpace="+QualitySettings.activeColorSpace);
}
}
