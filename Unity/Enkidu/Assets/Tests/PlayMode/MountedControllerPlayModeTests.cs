using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

public sealed class MountedControllerPlayModeTests
{
    [UnityTest] public IEnumerator SteeringRotatesWithoutLateralStrafeAtRest()
    {
        var go = new GameObject("mount test"); go.AddComponent<CharacterController>(); go.AddComponent<MountedInputAdapter>(); var controller = go.AddComponent<MountedAnzuController>();
        var start = go.transform.position; controller.Simulate(new Vector2(1, 0), false, 1, false);
        Assert.That(Quaternion.Angle(Quaternion.identity, go.transform.rotation), Is.GreaterThan(1)); Assert.That(Vector3.Distance(start, go.transform.position), Is.LessThan(.001f));
        Object.Destroy(go); yield return null;
    }

    [UnityTest] public IEnumerator GroundingDoesNotChangeSignedHorizontalState()
    {
        var ground = GameObject.CreatePrimitive(PrimitiveType.Plane); var go = new GameObject("mount test"); go.transform.position = new Vector3(0, .1f, 0);
        go.AddComponent<CharacterController>(); var input = go.AddComponent<MountedInputAdapter>(); var controller = go.AddComponent<MountedAnzuController>(); input.Inject(Vector2.up, Vector2.zero, false);
        yield return new WaitForSeconds(.25f); Assert.That(controller.CurrentSpeed, Is.GreaterThan(0)); Assert.That(controller.LocomotionState, Is.EqualTo(MountedLocomotionState.Walking));
        Object.Destroy(go); Object.Destroy(ground); yield return null;
    }
}
