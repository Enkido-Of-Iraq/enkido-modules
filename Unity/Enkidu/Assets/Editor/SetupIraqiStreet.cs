using System;
using System.Collections.Generic;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

public static class SetupIraqiStreet
{
    private const string SourceScene = "Assets/Scenes/AnzuDesert.unity";
    private const string StreetScene = "Assets/Scenes/IraqiStreet.unity";
    private const string StreetModel = "Assets/Art/IraqiStreet/IraqiStreet_Environment_v09.fbx";
    private const string PaintedTexture = "Assets/Art/IraqiStreet/IraqiWindow_plaster_painted_v08.png";
    private const string PaintedMaterial = "Assets/Art/IraqiStreet/PaintedWindowPlaster.mat";

    [MenuItem("Enkidu/Build Iraqi Street Scene")]
    public static void Build()
    {
        AssetDatabase.ImportAsset(StreetModel, ImportAssetOptions.ForceSynchronousImport);
        AssetDatabase.ImportAsset(PaintedTexture, ImportAssetOptions.ForceSynchronousImport);

        var scene = EditorSceneManager.OpenScene(SourceScene, OpenSceneMode.Single);
        foreach (var item in scene.GetRootGameObjects())
        {
            if (item.name == "Desert floor" || item.name == "Distant sand dune" ||
                item.name == "Enkidu — Ground Running")
                UnityEngine.Object.DestroyImmediate(item);
        }

        var existingStreet = GameObject.Find("Iraqi Street Environment");
        if (existingStreet != null)
            UnityEngine.Object.DestroyImmediate(existingStreet);

        var streetPrefab = AssetDatabase.LoadAssetAtPath<GameObject>(StreetModel);
        if (streetPrefab == null)
            throw new InvalidOperationException("The Iraqi street FBX has not imported.");

        var root = new GameObject("Iraqi Street Environment");
        var street = (GameObject)PrefabUtility.InstantiatePrefab(streetPrefab, scene);
        street.name = "Iraqi street, houses and details";
        street.transform.SetParent(root.transform, false);
        street.transform.localPosition = Vector3.zero;
        street.transform.localRotation = Quaternion.identity;
        street.transform.localScale = Vector3.one;

        var roadColliders = 0;
        foreach (var mesh in street.GetComponentsInChildren<MeshFilter>(true))
        {
            if (mesh.name != "Street asphalt" || mesh.sharedMesh == null)
                continue;
            var collider = mesh.GetComponent<BoxCollider>();
            if (collider == null)
                collider = mesh.gameObject.AddComponent<BoxCollider>();
            collider.center = mesh.sharedMesh.bounds.center;
            collider.size = mesh.sharedMesh.bounds.size;
            roadColliders++;
        }
        if (roadColliders == 0)
            throw new InvalidOperationException("The exported street road mesh is missing.");

        var texture = AssetDatabase.LoadAssetAtPath<Texture2D>(PaintedTexture);
        if (texture == null)
            throw new InvalidOperationException("The painted window texture has not imported.");

        var material = AssetDatabase.LoadAssetAtPath<Material>(PaintedMaterial);
        if (material == null)
        {
            var shader = Shader.Find("Universal Render Pipeline/Lit") ?? Shader.Find("Standard");
            if (shader == null)
                throw new InvalidOperationException("No compatible lit shader was found.");
            material = new Material(shader) { name = "Painted Window Plaster" };
            AssetDatabase.CreateAsset(material, PaintedMaterial);
        }
        material.mainTexture = texture;
        material.color = Color.white;
        EditorUtility.SetDirty(material);

        var paintedParts = 0;
        foreach (var renderer in street.GetComponentsInChildren<Renderer>(true))
        {
            var slots = renderer.sharedMaterials;
            var changed = false;
            for (var i = 0; i < slots.Length; i++)
            {
                if (slots[i] != null && slots[i].name.Contains("painted plaster"))
                {
                    slots[i] = material;
                    changed = true;
                }
            }
            if (!changed && (renderer.name == "Chipped plaster vertical jamb" ||
                             renderer.name == "Chipped plaster vertical jamb.001" ||
                             renderer.name == "Uneven plaster lintel"))
            {
                for (var i = 0; i < slots.Length; i++)
                    slots[i] = material;
                changed = slots.Length > 0;
            }
            if (changed)
            {
                renderer.sharedMaterials = slots;
                paintedParts++;
            }
        }

        var mounted = UnityEngine.Object.FindAnyObjectByType<MountedAnzuController>();
        if (mounted == null)
            throw new InvalidOperationException("The mounted Enkidu and Anzu character is missing from the source scene.");

        var rider = Array.Find(mounted.GetComponentsInChildren<Transform>(true),
            part => part.name == "ENKIDU_RIG");
        if (rider == null)
            throw new InvalidOperationException("The Enkidu rider rig is missing from the mounted character.");
        rider.gameObject.SetActive(true);

        var mobileControls = GameObject.Find("Mounted Mobile Controls");
        if (mobileControls != null && mobileControls.GetComponent<MobileControlsVisibility>() == null)
            mobileControls.AddComponent<MobileControlsVisibility>();

        EditorSceneManager.MarkSceneDirty(scene);
        if (!EditorSceneManager.SaveScene(scene, StreetScene))
            throw new InvalidOperationException("Unity could not save the Iraqi street scene.");

        var scenes = new List<EditorBuildSettingsScene>
        {
            new EditorBuildSettingsScene(StreetScene, true)
        };
        foreach (var item in EditorBuildSettings.scenes)
            if (item.path != StreetScene)
                scenes.Add(item);
        EditorBuildSettings.scenes = scenes.ToArray();

        AssetDatabase.SaveAssets();
        Debug.Log($"Iraqi Street scene saved with mounted character, {paintedParts} painted window parts, and {roadColliders} road collider.");
    }
}
