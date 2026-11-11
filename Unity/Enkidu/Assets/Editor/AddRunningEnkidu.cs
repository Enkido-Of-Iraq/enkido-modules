using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;
using System;
using System.IO;
using System.Linq;
[InitializeOnLoad] public static class AddRunningEnkidu {
 [Serializable] public class Item { public string name;public Color[] colors; }
 [Serializable] public class Data { public Item[] items; }
 static AddRunningEnkidu(){EditorApplication.delayCall+=Run;}
 static void Run(){
 string dir="Assets/Art/EnkiduRunning",path=dir+"/Enkidu_Running.fbx";
 if(File.Exists(dir+"/installed.done")||!File.Exists(path))return;
 if(EditorApplication.isCompiling||EditorApplication.isUpdating){EditorApplication.delayCall+=Run;return;}
 if(EditorApplication.isPlayingOrWillChangePlaymode)return;
 var imp=AssetImporter.GetAtPath(path) as ModelImporter;if(imp==null)return;
 if(imp.animationType!=ModelImporterAnimationType.Legacy){imp.animationType=ModelImporterAnimationType.Legacy;imp.importAnimation=true;imp.SaveAndReimport();EditorApplication.delayCall+=Run;return;}
 var prefab=AssetDatabase.LoadAssetAtPath<GameObject>(path);if(prefab==null)return;
 if(UnityEngine.SceneManagement.SceneManager.GetActiveScene().name!="AnzuDesert")return;
 var root=GameObject.Find("Enkidu — Ground Running");if(root==null)root=UnityEngine.Object.Instantiate(prefab);
 root.name="Enkidu — Ground Running";
 var mount=GameObject.Find("Mounted Anzu — Walk and Run");
 root.transform.position=(mount?mount.transform.position:Vector3.zero)+new Vector3(2.8f,0,0);
 var anim=root.GetComponent<Animation>();if(!anim)anim=root.AddComponent<Animation>();
 var clip=AssetDatabase.LoadAllAssetsAtPath(path).OfType<AnimationClip>().First(c=>!c.name.StartsWith("__preview"));
 anim.AddClip(clip,"Run");anim.clip=clip;anim.wrapMode=WrapMode.Loop;anim.playAutomatically=true;
 var data=JsonUtility.FromJson<Data>(File.ReadAllText(dir+"/colors.json"));
 foreach(var r in root.GetComponentsInChildren<Renderer>()){
 var it=Array.Find(data.items,i=>i.name==r.name);var mats=r.sharedMaterials;
 for(int i=0;i<mats.Length;i++){var m=new Material(Shader.Find("Universal Render Pipeline/Lit"));m.name=r.name+"_"+i;
 Color c=it!=null&&i<it.colors.Length?it.colors[i]:new Color(.35f,.24f,.14f);
 m.SetColor("_BaseColor",c);m.SetFloat("_Smoothness",.22f);AssetDatabase.CreateAsset(m,AssetDatabase.GenerateUniqueAssetPath(dir+"/Surface.mat"));mats[i]=m;}r.sharedMaterials=mats;}
 anim.Play("Run");anim.Sample();anim.Stop();
 var rs=root.GetComponentsInChildren<Renderer>();var bounds=rs[0].bounds;foreach(var r in rs)bounds.Encapsulate(r.bounds);
 root.transform.position+=Vector3.up*(.025f-bounds.min.y);
 var cam=Camera.main;if(cam){cam.transform.position=new Vector3(7,4,8);cam.transform.LookAt(new Vector3(1.1f,1.5f,0));}
 EditorSceneManager.MarkSceneDirty(root.scene);EditorSceneManager.SaveScene(root.scene);AssetDatabase.SaveAssets();
 if(mount){foreach(var t in mount.GetComponentsInChildren<Transform>(true))if(t.name=="ENKIDU_RIG")t.gameObject.SetActive(false);}
 EditorSceneManager.SaveScene(root.scene);
 var rt=new RenderTexture(1000,1000,24);cam.targetTexture=rt;cam.Render();RenderTexture.active=rt;var tex=new Texture2D(1000,1000,TextureFormat.RGB24,false);tex.ReadPixels(new Rect(0,0,1000,1000),0,0);tex.Apply();File.WriteAllBytes("/private/tmp/enkidu_running_unity.png",tex.EncodeToPNG());cam.targetTexture=null;RenderTexture.active=null;UnityEngine.Object.DestroyImmediate(tex);UnityEngine.Object.DestroyImmediate(rt);
 Selection.activeGameObject=root;
 File.WriteAllText(dir+"/installed.done","clip="+clip.name+" duration="+clip.length+" renderers="+rs.Length+" bounds="+bounds.size);
 }
}

// Refresh after completed FBX export.
