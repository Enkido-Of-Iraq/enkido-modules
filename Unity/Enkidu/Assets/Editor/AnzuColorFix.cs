using UnityEngine;using UnityEditor;using UnityEditor.SceneManagement;using System;using System.IO;
[InitializeOnLoad] public static class AnzuColorFix {
 [Serializable] public class Item {public string name;public Color[] colors;}
 [Serializable] public class Data {public Item[] items;}
 static AnzuColorFix(){EditorApplication.delayCall+=Fix;}
 static void Fix(){string done="Assets/Art/AnzuMountedV05/colorfix.done";if(File.Exists(done))return;
 if(UnityEngine.SceneManagement.SceneManager.GetActiveScene().name!="AnzuDesert")EditorSceneManager.OpenScene("Assets/Scenes/AnzuDesert.unity");
 var data=JsonUtility.FromJson<Data>(File.ReadAllText("Assets/Art/AnzuMountedV05/colors.json"));
 var root=GameObject.Find("Enkidu riding Anzu — V05");if(!root)return;
 foreach(var r in root.GetComponentsInChildren<Renderer>()){var item=Array.Find(data.items,i=>i.name==r.name);if(item==null)continue;var mats=r.sharedMaterials;for(int i=0;i<mats.Length&&i<item.colors.Length;i++){if(!mats[i])continue;var m=new Material(mats[i]);m.color=item.colors[i];m.SetColor("_BaseColor",item.colors[i]);AssetDatabase.CreateAsset(m,AssetDatabase.GenerateUniqueAssetPath("Assets/Art/AnzuMountedV05/Color.mat"));mats[i]=m;}r.sharedMaterials=mats;}
 var c=Camera.main;c.transform.position=new Vector3(6,4.5f,8);c.transform.LookAt(new Vector3(0,2,0));
 EditorSceneManager.SaveScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene());AssetDatabase.SaveAssets();File.WriteAllText(done,"Applied Blender base colors");SetupAnzuDesert.Open();
 }
}
