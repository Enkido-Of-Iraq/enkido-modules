using UnityEditor;using UnityEngine;using System.IO;
[InitializeOnLoad] public static class TestMountedMovement {
 static double start;static Vector3 last;static float walk,run;static bool initialized;
 static TestMountedMovement(){EditorApplication.update+=Tick;}
 static void Tick(){if(File.Exists("Assets/Art/AnzuMountedV05/movement-test.txt"))return;if(EditorApplication.isCompiling)return;
 var c=Object.FindFirstObjectByType<MountedAnzuController>();if(!c)return;
 if(!EditorApplication.isPlaying){if(!SessionState.GetBool("anzu-test-started",false)){SessionState.SetBool("anzu-test-started",true);EditorApplication.isPlaying=true;}return;}
 if(!initialized){initialized=true;start=EditorApplication.timeSinceStartup;last=c.transform.position;c.testInput=true;}
 double t=EditorApplication.timeSinceStartup-start;
 c.simulatedMove=t<.5||t>5?Vector2.zero:Vector2.up;c.simulatedRun=t>2.5;
 float delta=Vector3.ProjectOnPlane(c.transform.position-last,Vector3.up).magnitude;last=c.transform.position;
 if(t>1&&t<2.5)walk+=delta;if(t>3&&t<4.5)run+=delta;
 if(t>6){File.WriteAllText("Assets/Art/AnzuMountedV05/movement-test.txt","walkDistance="+walk+" runDistance="+run+" stoppedSpeed="+c.CurrentSpeed+" grounded="+c.GetComponent<CharacterController>().isGrounded+" animations="+c.GetComponentsInChildren<Animation>().Length+" result="+(walk>.3f&&run>walk*1.5f&&c.CurrentSpeed<.01f?"PASS":"FAIL"));EditorApplication.isPlaying=false;}
 }
}
