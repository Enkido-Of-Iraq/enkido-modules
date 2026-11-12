using Unity.Cinemachine;
using UnityEngine;

[DisallowMultipleComponent]
public sealed class MountedCameraController : MonoBehaviour
{
    [SerializeField] MountedInputAdapter input; [SerializeField] MountedAnzuController mount; [SerializeField] CinemachineOrbitalFollow orbit;
    [SerializeField] float horizontalSensitivity = 100f, verticalSensitivity = 70f, minimumPitch = -12f, maximumPitch = 42f, recenterDelay = 1.25f, recenterSpeed = 90f, lookDeadZone = .02f;
    float timeSinceLook;
    void Update() => Simulate(input ? input.Look : Vector2.zero, Time.deltaTime);
    public void Configure(MountedInputAdapter inputSource, MountedAnzuController mountedController, CinemachineOrbitalFollow orbitalFollow)
    { input = inputSource; mount = mountedController; orbit = orbitalFollow; }
    public void Simulate(Vector2 look, float deltaTime)
    {
        if (!orbit) return;
        if (look.sqrMagnitude > lookDeadZone * lookDeadZone) { timeSinceLook = 0; orbit.HorizontalAxis.Value += look.x * horizontalSensitivity * deltaTime; orbit.VerticalAxis.Value -= look.y * verticalSensitivity * deltaTime; }
        else { timeSinceLook += deltaTime; if (timeSinceLook >= recenterDelay && mount && Mathf.Abs(mount.CurrentSpeed) > mount.stopThreshold) orbit.HorizontalAxis.Value = Mathf.MoveTowardsAngle(orbit.HorizontalAxis.Value, 0, recenterSpeed * deltaTime); }
        orbit.VerticalAxis.Range = new Vector2(minimumPitch, maximumPitch); orbit.VerticalAxis.Value = Mathf.Clamp(orbit.VerticalAxis.Value, minimumPitch, maximumPitch);
    }
}
