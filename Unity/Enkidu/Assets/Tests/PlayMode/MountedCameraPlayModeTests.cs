using System.Collections;
using NUnit.Framework;
using Unity.Cinemachine;
using UnityEngine;
using UnityEngine.TestTools;

public sealed class MountedCameraPlayModeTests
{
    [UnityTest] public IEnumerator OrbitIsIndependentAndPitchIsClamped()
    {
        var mountObject = new GameObject("mount"); mountObject.AddComponent<CharacterController>(); var input = mountObject.AddComponent<MountedInputAdapter>(); var mount = mountObject.AddComponent<MountedAnzuController>();
        var cameraObject = new GameObject("camera"); cameraObject.AddComponent<CinemachineCamera>(); var orbit = cameraObject.AddComponent<CinemachineOrbitalFollow>(); var controller = cameraObject.AddComponent<MountedCameraController>(); controller.Configure(input, mount, orbit);
        var mountRotation = mountObject.transform.rotation; controller.Simulate(new Vector2(1, -100), 1);
        Assert.That(orbit.HorizontalAxis.Value, Is.Not.EqualTo(0)); Assert.That(orbit.VerticalAxis.Value, Is.InRange(-12, 42)); Assert.That(mountObject.transform.rotation, Is.EqualTo(mountRotation));
        Object.Destroy(cameraObject); Object.Destroy(mountObject); yield return null;
    }

    [UnityTest] public IEnumerator RecenterWaitsForDelayThenMovesTowardRear()
    {
        var mountObject = new GameObject("mount"); mountObject.AddComponent<CharacterController>(); var input = mountObject.AddComponent<MountedInputAdapter>(); var mount = mountObject.AddComponent<MountedAnzuController>(); mount.Simulate(Vector2.up, false, 1, false);
        var cameraObject = new GameObject("camera"); cameraObject.AddComponent<CinemachineCamera>(); var orbit = cameraObject.AddComponent<CinemachineOrbitalFollow>(); orbit.HorizontalAxis.Value = 90; var controller = cameraObject.AddComponent<MountedCameraController>(); controller.Configure(input, mount, orbit);
        controller.Simulate(Vector2.zero, .5f); Assert.That(orbit.HorizontalAxis.Value, Is.EqualTo(90).Within(.01f));
        controller.Simulate(Vector2.zero, 1f); Assert.That(Mathf.Abs(orbit.HorizontalAxis.Value), Is.LessThan(90));
        Object.Destroy(cameraObject); Object.Destroy(mountObject); yield return null;
    }
}
