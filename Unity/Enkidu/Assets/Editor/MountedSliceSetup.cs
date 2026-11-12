using System.IO;
using Unity.Cinemachine;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.OnScreen;
using UnityEngine.InputSystem.UI;
using UnityEngine.UI;

public static class MountedSliceSetup
{
    const string ScenePath = "Assets/Scenes/AnzuDesert.unity";
    const string InputPath = "Assets/SourceFiles/InputSystem/StarterAssets.inputactions";
    const string PrefabPath = "Assets/Prefabs/MountedAnzuPlayer.prefab";

    [MenuItem("Enkidu/Configure Mounted Slice")]
    public static void Configure()
    {
        var scene = EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Single);
        var controller = Object.FindFirstObjectByType<MountedAnzuController>();
        if (!controller) throw new System.InvalidOperationException("AnzuDesert has no MountedAnzuController.");
        var root = controller.gameObject;
        var playerInput = GetOrAdd<PlayerInput>(root); playerInput.actions = AssetDatabase.LoadAssetAtPath<InputActionAsset>(InputPath); playerInput.defaultActionMap = "Player"; playerInput.notificationBehavior = PlayerNotifications.InvokeCSharpEvents;
        var adapter = GetOrAdd<MountedInputAdapter>(root); SetReference(adapter, "playerInput", playerInput); SetReference(controller, "input", adapter);
        controller.walkSpeed = 3; controller.runSpeed = 7; controller.reverseSpeed = 1.5f; controller.acceleration = 3.5f; controller.deceleration = 4.5f; controller.braking = 7; controller.movingTurnSpeed = 95; controller.lowSpeedTurnSpeed = 55;
        var presenter = GetOrAdd<MountedAnimationPresenter>(root); SetReference(presenter, "controller", controller); SetReference(presenter, "animatedRoot", controller.AnimatedRoot);
        var fixture = GetOrAdd<MountedTraversalFixture>(root); SetReference(fixture, "controller", controller); SetReference(fixture, "input", adapter);
        var target = FindOrCreateChild(root.transform, "Mounted Camera Target"); target.localPosition = new Vector3(0, 2.25f, 0); target.localRotation = Quaternion.identity;
        ConfigureCamera(target, controller, adapter); ConfigureMobileUi();
        Directory.CreateDirectory("Assets/Prefabs"); PrefabUtility.SaveAsPrefabAssetAndConnect(root, PrefabPath, InteractionMode.AutomatedAction);
        EditorSceneManager.MarkSceneDirty(scene); EditorSceneManager.SaveScene(scene); AssetDatabase.SaveAssets(); Debug.Log("MOUNTED_SLICE_CONFIGURED");
    }

    static void ConfigureCamera(Transform target, MountedAnzuController controller, MountedInputAdapter adapter)
    {
        var main = Camera.main; if (!main) throw new System.InvalidOperationException("AnzuDesert has no Main Camera."); GetOrAdd<CinemachineBrain>(main.gameObject);
        var go = GameObject.Find("Mounted Cinemachine Camera") ?? new GameObject("Mounted Cinemachine Camera");
        var camera = GetOrAdd<CinemachineCamera>(go); camera.Follow = target; camera.LookAt = target; camera.Lens.FieldOfView = 48;
        var orbit = GetOrAdd<CinemachineOrbitalFollow>(go); orbit.Radius = 8.5f; orbit.TargetOffset = new Vector3(0, .6f, 0); orbit.HorizontalAxis.Value = 0; orbit.VerticalAxis.Range = new Vector2(-12, 42); orbit.VerticalAxis.Value = 12; orbit.TrackerSettings.PositionDamping = new Vector3(.45f, .55f, .45f);
        GetOrAdd<CinemachineRotationComposer>(go).Damping = new Vector2(.35f, .35f);
        var cameraInput = GetOrAdd<MountedCameraController>(go); SetReference(cameraInput, "input", adapter); SetReference(cameraInput, "mount", controller); SetReference(cameraInput, "orbit", orbit);
    }

    static void ConfigureMobileUi()
    {
        var go = GameObject.Find("Mounted Mobile Controls") ?? new GameObject("Mounted Mobile Controls", typeof(RectTransform), typeof(Canvas), typeof(CanvasScaler), typeof(GraphicRaycaster));
        var canvas = go.GetComponent<Canvas>(); canvas.renderMode = RenderMode.ScreenSpaceOverlay; canvas.sortingOrder = 20; go.GetComponent<CanvasScaler>().uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
        CreateStick(go.transform, "Move Stick", new Vector2(150, 150), "<Gamepad>/leftStick", false); CreateStick(go.transform, "Look Stick", new Vector2(-150, 150), "<Gamepad>/rightStick", true); CreateRunButton(go.transform);
        if (!Object.FindFirstObjectByType<EventSystem>()) { var eventSystem = new GameObject("EventSystem", typeof(EventSystem)); eventSystem.AddComponent<InputSystemUIInputModule>(); }
    }
    static void CreateStick(Transform parent, string name, Vector2 position, string path, bool right)
    {
        var go = FindOrCreateUi(parent, name); var rect = go.GetComponent<RectTransform>(); rect.sizeDelta = new Vector2(220, 220); rect.anchorMin = rect.anchorMax = right ? new Vector2(1, 0) : Vector2.zero; rect.anchoredPosition = position;
        var image = GetOrAdd<Image>(go); image.color = new Color(1, 1, 1, .18f); image.raycastTarget = true; var stick = GetOrAdd<OnScreenStick>(go); stick.controlPath = path; stick.movementRange = 90;
    }
    static void CreateRunButton(Transform parent)
    {
        var go = FindOrCreateUi(parent, "Hold To Run"); var rect = go.GetComponent<RectTransform>(); rect.sizeDelta = new Vector2(150, 150); rect.anchorMin = rect.anchorMax = new Vector2(1, 0); rect.anchoredPosition = new Vector2(-300, 150);
        var image = GetOrAdd<Image>(go); image.color = new Color(.85f, .55f, .1f, .55f); image.raycastTarget = true; GetOrAdd<OnScreenButton>(go).controlPath = "<Gamepad>/leftTrigger";
        var label = FindOrCreateUi(go.transform, "Label"); var lr = label.GetComponent<RectTransform>(); lr.anchorMin = Vector2.zero; lr.anchorMax = Vector2.one; lr.offsetMin = lr.offsetMax = Vector2.zero;
        var text = GetOrAdd<Text>(label); text.text = "RUN"; text.alignment = TextAnchor.MiddleCenter; text.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf"); text.fontSize = 28; text.color = Color.white; text.raycastTarget = false;
    }
    static GameObject FindOrCreateUi(Transform parent, string name) { var child = parent.Find(name); if (child) return child.gameObject; var go = new GameObject(name, typeof(RectTransform)); go.transform.SetParent(parent, false); return go; }
    static Transform FindOrCreateChild(Transform parent, string name) { var child = parent.Find(name); if (child) return child; var go = new GameObject(name); go.transform.SetParent(parent, false); return go.transform; }
    static T GetOrAdd<T>(GameObject go) where T : Component { var value = go.GetComponent<T>(); return value ? value : go.AddComponent<T>(); }
    static void SetReference(Object target, string property, Object value) { var serialized = new SerializedObject(target); serialized.FindProperty(property).objectReferenceValue = value; serialized.ApplyModifiedPropertiesWithoutUndo(); }
}
