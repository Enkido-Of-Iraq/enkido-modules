using UnityEngine;
#if ENABLE_INPUT_SYSTEM
using UnityEngine.InputSystem;
#endif
[RequireComponent(typeof(CharacterController))]
public class MountedAnzuController:MonoBehaviour {
 public float walkSpeed=.7f,runSpeed=9f,acceleration=4f,turnSpeed=150f;
 public Transform animatedRoot; public Camera followCamera;
 public string State {get;private set;}="Idle";
 public float CurrentSpeed {get;private set;}
 CharacterController body;Animation[] animations;Vector3 rootRest,cameraOffset;float fall;Vector3 heading;
 public bool testInput; public Vector2 simulatedMove;public bool simulatedRun;
 void Awake(){body=GetComponent<CharacterController>();animations=GetComponentsInChildren<Animation>();if(animatedRoot)rootRest=animatedRoot.localPosition;if(followCamera)cameraOffset=followCamera.transform.position-transform.position;heading=transform.forward;
 foreach(var a in animations){a.playAutomatically=false;foreach(AnimationState st in a){st.wrapMode=WrapMode.Loop;}if(a.clip)a.Play(a.clip.name);}}
 void Update(){
 Vector2 input=Vector2.zero;bool run=false;
 if(testInput){input=simulatedMove;run=simulatedRun;}
 else {
#if ENABLE_INPUT_SYSTEM
 var k=Keyboard.current;if(k!=null){input=new Vector2((k.dKey.isPressed||k.rightArrowKey.isPressed?1:0)-(k.aKey.isPressed||k.leftArrowKey.isPressed?1:0),(k.wKey.isPressed||k.upArrowKey.isPressed?1:0)-(k.sKey.isPressed||k.downArrowKey.isPressed?1:0));run=k.leftShiftKey.isPressed||k.rightShiftKey.isPressed;}
#else
 input=new Vector2(Input.GetAxisRaw("Horizontal"),Input.GetAxisRaw("Vertical"));run=Input.GetKey(KeyCode.LeftShift)||Input.GetKey(KeyCode.RightShift);
#endif
 }
 input=Vector2.ClampMagnitude(input,1);Vector3 forward=followCamera?Vector3.ProjectOnPlane(followCamera.transform.forward,Vector3.up).normalized:Vector3.forward;Vector3 right=Vector3.Cross(Vector3.up,forward);Vector3 move=forward*input.y+right*input.x;
 float target=input.magnitude*(run?runSpeed:walkSpeed);CurrentSpeed=Mathf.MoveTowards(CurrentSpeed,target,acceleration*Time.deltaTime);
 if(move.sqrMagnitude>.001f){heading=move.normalized;transform.rotation=Quaternion.RotateTowards(transform.rotation,Quaternion.LookRotation(heading),turnSpeed*Time.deltaTime);}
 fall=body.isGrounded?-2f:fall+Physics.gravity.y*Time.deltaTime;body.Move((heading*CurrentSpeed+Vector3.up*fall)*Time.deltaTime);
 State=CurrentSpeed<.01f?"Idle":run&&input.sqrMagnitude>.01f?"Run":"Walk";
 foreach(var a in animations)foreach(AnimationState st in a)st.speed=CurrentSpeed/.24f;
 }
 void LateUpdate(){if(animatedRoot)animatedRoot.localPosition=rootRest;if(followCamera){followCamera.transform.position=Vector3.Lerp(followCamera.transform.position,transform.position+cameraOffset,1-Mathf.Exp(-6*Time.deltaTime));followCamera.transform.LookAt(transform.position+Vector3.up*2);}}
 void OnGUI(){GUI.Box(new Rect(16,16,270,60),"WASD / arrows: walk    Shift: run\n"+State);}
}
