using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class SetupIraqMarshlandScene
{
    private const string AssetPath = "Assets/Art/Environment/IraqMarshland/IraqMarshlandAssetKit.fbx";
    private const string ScenePath = "Assets/Scenes/IraqMarshland.unity";

    public static void Build()
    {
        AssetDatabase.ImportAsset(AssetPath, ImportAssetOptions.ForceUpdate);
        var kit = AssetDatabase.LoadAssetAtPath<GameObject>(AssetPath);
        if (kit == null)
            throw new System.InvalidOperationException("Marshland FBX could not be imported.");

        var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
        var environment = PrefabUtility.InstantiatePrefab(kit) as GameObject;
        environment.name = "Iraq Marshland Environment";

        var sunObject = new GameObject("Sun");
        var sun = sunObject.AddComponent<Light>();
        sun.type = LightType.Directional;
        sun.color = new Color(1f, 0.79f, 0.56f);
        sun.intensity = 1.15f;
        sunObject.transform.rotation = Quaternion.Euler(38f, -28f, 0f);

        var cameraObject = new GameObject("Main Camera");
        cameraObject.tag = "MainCamera";
        var camera = cameraObject.AddComponent<Camera>();
        cameraObject.AddComponent<AudioListener>();
        camera.transform.position = new Vector3(0f, -12f, 5.2f);
        camera.transform.LookAt(new Vector3(0f, 0.7f, 1.45f));
        camera.clearFlags = CameraClearFlags.SolidColor;
        camera.backgroundColor = new Color(0.42f, 0.58f, 0.56f);

        RenderSettings.ambientMode = UnityEngine.Rendering.AmbientMode.Flat;
        RenderSettings.ambientLight = new Color(0.55f, 0.52f, 0.43f);
        EditorSceneManager.SaveScene(scene, ScenePath);

        var remaining = EditorBuildSettings.scenes
            .Where(s => s.path != ScenePath)
            .ToList();
        remaining.Insert(0, new EditorBuildSettingsScene(ScenePath, true));
        EditorBuildSettings.scenes = remaining.ToArray();
        AssetDatabase.SaveAssets();
    }
}
