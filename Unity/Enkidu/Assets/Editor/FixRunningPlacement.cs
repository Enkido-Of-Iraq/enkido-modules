using UnityEngine;using UnityEditor;using UnityEditor.SceneManagement;using System.IO;using System.Linq;
[InitializeOnLoad] public static class FixRunningPlacement {
static FixRunningPlacement(){EditorApplication.delayCall+=Run;}
static void Run(){
if(EditorApplication.isCompiling||EditorApplication.isUpdating){EditorApplication.delayCall+=Run;return;}
if(EditorApplication.isPlayingOrWillChangePlaymode||File.Exists("Assets/Art/EnkiduRunning/grounded_v2.done"))return;
var root=GameObject.Find("Enkidu — Ground Running");if(!root)return;
var a=root.GetComponent<Animation>();var clip=a.clip;
clip.SampleAnimation(root,.2f);
float min=float.PositiveInfinity,max=float.NegativeInfinity;
foreach(var r in root.GetComponentsInChildren<Renderer>()){
Mesh m=null;bool temp=false;
if(r is SkinnedMeshRenderer sk){m=new Mesh();sk.BakeMesh(m);temp=true;}else{var mf=r.GetComponent<MeshFilter>();if(mf)m=mf.sharedMesh;}
if(m){foreach(var v in m.vertices){float y=r.transform.TransformPoint(v).y;min=Mathf.Min(min,y);max=Mathf.Max(max,y);}if(temp)Object.DestroyImmediate(m);}}
root.transform.position=new Vector3(2.8f,.02f,0);
var mount=GameObject.Find("Mounted Anzu — Walk and Run");
var names=mount.GetComponentsInChildren<Renderer>(true).Select(r=>r.name).ToArray();File.WriteAllLines("/private/tmp/mounted_names.txt",names);
foreach(var r in mount.GetComponentsInChildren<Renderer>(true))if(r.name.StartsWith("ANIM"))r.enabled=false;
EditorSceneManager.SaveScene(root.scene);
var cam=Camera.main;var rt=new RenderTexture(1000,1000,24);cam.targetTexture=rt;cam.Render();RenderTexture.active=rt;var tx=new Texture2D(1000,1000,TextureFormat.RGB24,false);tx.ReadPixels(new Rect(0,0,1000,1000),0,0);tx.Apply();File.WriteAllBytes("/private/tmp/enkidu_running_grounded_v2.png",tx.EncodeToPNG());cam.targetTexture=null;RenderTexture.active=null;Object.DestroyImmediate(tx);Object.DestroyImmediate(rt);
File.WriteAllText("Assets/Art/EnkiduRunning/grounded_v2.done","min="+min+" max="+max+" root="+root.transform.position+" scale="+root.transform.localScale);
}
}

// Retry compilation after disk availability recovered.
