using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;
public static class SetupAnzuDesert {
 public static void Open(){
 EditorSceneManager.OpenScene("Assets/Scenes/AnzuDesert.unity");
 var c=Camera.main;var rt=new RenderTexture(1000,1000,24);c.targetTexture=rt;c.Render();RenderTexture.active=rt;
 var t=new Texture2D(1000,1000,TextureFormat.RGB24,false);t.ReadPixels(new Rect(0,0,1000,1000),0,0);t.Apply();System.IO.File.WriteAllBytes("/private/tmp/anzu_unity_preview.png",t.EncodeToPNG());c.targetTexture=null;RenderTexture.active=null;
 if(SceneView.lastActiveSceneView!=null)SceneView.lastActiveSceneView.LookAt(new Vector3(0,2,0),Quaternion.Euler(20,-35,0),8);
 Debug.Log("ANZU_SCENE_OPENED");
 }
 public static void Build(){
 string folder="Assets/Art/AnzuMountedV05";
 AssetDatabase.Refresh();
 var importer=AssetImporter.GetAtPath(folder+"/Enkidu_Anzu_v05.fbx") as ModelImporter;
 importer.animationType=ModelImporterAnimationType.Legacy;importer.importAnimation=true;importer.SaveAndReimport();
 var scene=EditorSceneManager.NewScene(NewSceneSetup.EmptyScene,NewSceneMode.Single);
 var model=AssetDatabase.LoadAssetAtPath<GameObject>(folder+"/Enkidu_Anzu_v05.fbx");
 var instance=Object.Instantiate(model);instance.name="Enkidu riding Anzu — V05";
 var shader=Shader.Find("Universal Render Pipeline/Lit");if(!shader)shader=Shader.Find("Standard");
 var map=new System.Collections.Generic.Dictionary<Material,Material>();
 foreach(var rend in instance.GetComponentsInChildren<Renderer>()){
 var mats=rend.sharedMaterials;
 for(int i=0;i<mats.Length;i++){var original=mats[i];if(original==null)continue;if(!map.ContainsKey(original)){var m=new Material(shader);m.name=original.name;Color c=original.HasProperty("_Color")?original.color:new Color(.45f,.25f,.1f);m.SetColor("_BaseColor",c);m.color=c;m.SetFloat("_Smoothness",.25f);string path=AssetDatabase.GenerateUniqueAssetPath(folder+"/Material.mat");AssetDatabase.CreateAsset(m,path);map.Add(original,m);}mats[i]=map[original];}rend.sharedMaterials=mats;}
 var sand=new Material(shader);sand.name="Warm desert sand";sand.color=new Color(.68f,.49f,.26f);sand.SetColor("_BaseColor",sand.color);sand.SetFloat("_Smoothness",.05f);AssetDatabase.CreateAsset(sand,folder+"/DesertSand.mat");
 var ground=GameObject.CreatePrimitive(PrimitiveType.Plane);ground.name="Desert floor";ground.transform.localScale=new Vector3(30,1,30);ground.transform.position=new Vector3(0,-.03f,0);ground.GetComponent<Renderer>().sharedMaterial=sand;
 Random.InitState(27);
 for(int i=0;i<18;i++){var dune=GameObject.CreatePrimitive(PrimitiveType.Sphere);dune.name="Distant sand dune";float angle=i*Mathf.PI*2/18;dune.transform.position=new Vector3(Mathf.Cos(angle)*45,-2,Mathf.Sin(angle)*45);dune.transform.localScale=new Vector3(Random.Range(18,30),Random.Range(5,9),Random.Range(12,22));dune.GetComponent<Renderer>().sharedMaterial=sand;}
 var sun=new GameObject("Desert sun").AddComponent<Light>();sun.type=LightType.Directional;sun.intensity=1.4f;sun.color=new Color(1,.85f,.64f);sun.transform.rotation=Quaternion.Euler(45,-35,0);sun.shadows=LightShadows.Soft;
 RenderSettings.ambientMode=UnityEngine.Rendering.AmbientMode.Flat;RenderSettings.ambientLight=new Color(.55f,.52f,.45f);RenderSettings.fog=true;RenderSettings.fogColor=new Color(.77f,.69f,.54f);RenderSettings.fogMode=FogMode.ExponentialSquared;RenderSettings.fogDensity=.008f;
 var camera=new GameObject("Main Camera").AddComponent<Camera>();camera.tag="MainCamera";camera.transform.position=new Vector3(8,5,-9);camera.transform.LookAt(new Vector3(0,2,0));camera.clearFlags=CameraClearFlags.SolidColor;camera.backgroundColor=new Color(.65f,.77f,.86f);camera.gameObject.AddComponent<AudioListener>();
 foreach(var anim in instance.GetComponentsInChildren<Animation>()){anim.playAutomatically=true;anim.wrapMode=WrapMode.Loop;}
 EditorSceneManager.SaveScene(scene,"Assets/Scenes/AnzuDesert.unity");
 PrefabUtility.SaveAsPrefabAsset(instance,folder+"/EnkiduRidingAnzu.prefab");

 AssetDatabase.SaveAssets();Debug.Log("ANZU_DESERT_READY renderers="+instance.GetComponentsInChildren<Renderer>().Length);
 }
}
