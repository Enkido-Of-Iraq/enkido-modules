using UnityEngine;

public enum MountedLocomotionState { Idle, Walking, Running, Stopping, Reversing }

[System.Serializable]
public sealed class MountedLocomotionModel
{
    public float walkSpeed = 3f, runSpeed = 7f, reverseSpeed = 1.5f;
    public float acceleration = 3.5f, deceleration = 4.5f, braking = 7f;
    public float inputDeadZone = .08f, stopThreshold = .05f, runEnterSpeed = 3.3f, runExitSpeed = 2.8f;
    public float SignedSpeed { get; private set; }
    public MountedLocomotionState State { get; private set; } = MountedLocomotionState.Idle;

    public void Reset(float speed = 0f) { SignedSpeed = speed; State = Mathf.Abs(speed) <= stopThreshold ? MountedLocomotionState.Idle : speed < 0 ? MountedLocomotionState.Reversing : MountedLocomotionState.Walking; }
    public void Step(float forward, bool runHeld, float dt)
    {
        forward = Mathf.Clamp(forward, -1f, 1f); float target = 0f, rate = deceleration;
        if (forward > inputDeadZone) { target = forward * (runHeld ? runSpeed : walkSpeed); rate = SignedSpeed < -stopThreshold ? braking : Mathf.Abs(target) >= Mathf.Abs(SignedSpeed) ? acceleration : deceleration; }
        else if (forward < -inputDeadZone) { if (SignedSpeed > stopThreshold) { target = 0; rate = braking; } else { target = forward * reverseSpeed; rate = SignedSpeed > 0 ? braking : acceleration; } }
        SignedSpeed = Mathf.MoveTowards(SignedSpeed, target, Mathf.Max(0, rate) * Mathf.Max(0, dt));
        if (Mathf.Abs(forward) <= inputDeadZone && Mathf.Abs(SignedSpeed) <= stopThreshold) SignedSpeed = 0;
        State = Resolve(forward, runHeld);
    }
    MountedLocomotionState Resolve(float forward, bool runHeld)
    {
        if (SignedSpeed < -stopThreshold || (forward < -inputDeadZone && SignedSpeed <= stopThreshold)) return MountedLocomotionState.Reversing;
        if (Mathf.Abs(forward) <= inputDeadZone) return SignedSpeed > stopThreshold ? MountedLocomotionState.Stopping : MountedLocomotionState.Idle;
        if (forward < -inputDeadZone && SignedSpeed > stopThreshold) return MountedLocomotionState.Stopping;
        if (!runHeld) return MountedLocomotionState.Walking;
        return (State == MountedLocomotionState.Running ? SignedSpeed >= runExitSpeed : SignedSpeed >= runEnterSpeed) ? MountedLocomotionState.Running : MountedLocomotionState.Walking;
    }
}
