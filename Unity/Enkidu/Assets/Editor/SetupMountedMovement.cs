using UnityEngine;using UnityEditor;using UnityEditor.SceneManagement;using System.IO;
[InitializeOnLoad] public static class SetupMountedMovement {
 static SetupMountedMovement(){EditorApplication.delayCall+=Install;}
 static void Install(){if(File.Exists("Assets/Art/AnzuMountedV05/movement.done")||EditorApplication.isPlayingOrWillChangePlaymode)return;
 if(UnityEngine.SceneManagement.SceneManager.GetActiveScene().name!="AnzuDesert")return;
 var model=GameObject.Find("Enkidu riding Anzu — V05");if(!model)return;
 var player=new GameObject("Mounted Anzu — Walk and Run");player.transform.position=model.transform.position;model.transform.SetParent(player.transform,true);
 var cc=player.AddComponent<CharacterController>();cc.height=2.6f;cc.radius=.55f;cc.center=new Vector3(0,1.35f,0);cc.stepOffset=.25f;
 var control=player.AddComponent<MountedAnzuController>();control.followCamera=Camera.main;
 foreach(var t in model.GetComponentsInChildren<Transform>())if(t.name=="ANZU_V05_RIG")control.animatedRoot=t;
 var anim=model.GetComponent<Animation>();if(!anim)anim=model.AddComponent<Animation>();
 foreach(var asset in AssetDatabase.LoadAllAssetsAtPath("Assets/Art/AnzuMountedV05/Enkidu_Anzu_v05.fbx"))if(asset is AnimationClip clip&&!clip.name.StartsWith("__")){anim.AddClip(clip,clip.name);if(!anim.clip)anim.clip=clip;}
 anim.playAutomatically=false;
 EditorSceneManager.SaveScene(UnityEngine.SceneManagement.SceneManager.GetActiveScene());
 File.WriteAllText("Assets/Art/AnzuMountedV05/movement.done","root="+(control.animatedRoot?control.animatedRoot.name:"MISSING")+" clip="+(anim.clip?anim.clip.name:"MISSING"));Debug.Log("ANZU_MOVEMENT_INSTALLED");
 }
}
