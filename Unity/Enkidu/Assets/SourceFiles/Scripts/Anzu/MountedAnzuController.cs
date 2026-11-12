using UnityEngine;

[RequireComponent(typeof(CharacterController)), RequireComponent(typeof(MountedInputAdapter)), DisallowMultipleComponent]
public sealed class MountedAnzuController : MonoBehaviour
{
    [Header("Speed")]
    public float walkSpeed = 3f, runSpeed = 7f, reverseSpeed = 1.5f, acceleration = 3.5f, deceleration = 4.5f, braking = 7f;
    [Header("Steering")]
    public float movingTurnSpeed = 95f, lowSpeedTurnSpeed = 55f;
    [Header("Grounding")]
    public float groundedForce = -2f, gravity = -20f;
    [Header("State thresholds")]
    public float inputDeadZone = .08f, stopThreshold = .05f, runEnterSpeed = 3.3f, runExitSpeed = 2.8f;
    [SerializeField] MountedInputAdapter input;
    [SerializeField] Transform animatedRoot;

    public MountedLocomotionState LocomotionState => model.State;
    public string State => model.State.ToString();
    public float CurrentSpeed => model.SignedSpeed;
    public Transform AnimatedRoot => animatedRoot;
    public MountedInputAdapter Input => input;

    CharacterController body; readonly MountedLocomotionModel model = new MountedLocomotionModel(); float verticalSpeed;
    void Awake() { body = GetComponent<CharacterController>(); if (!input) input = GetComponent<MountedInputAdapter>(); CopySettings(); }
    void OnValidate() { walkSpeed = Mathf.Max(0, walkSpeed); runSpeed = Mathf.Max(walkSpeed, runSpeed); reverseSpeed = Mathf.Max(0, reverseSpeed); runExitSpeed = Mathf.Min(runExitSpeed, runEnterSpeed); CopySettings(); }
    void Update() { Simulate(input ? input.Move : Vector2.zero, input && input.RunHeld, Time.deltaTime, true); }

    public void Simulate(Vector2 move, bool runHeld, float deltaTime, bool applyMotion)
    {
        CopySettings(); move = Vector2.ClampMagnitude(move, 1); model.Step(move.y, runHeld, deltaTime);
        var turnRate = Mathf.Abs(model.SignedSpeed) > stopThreshold ? movingTurnSpeed : lowSpeedTurnSpeed;
        transform.Rotate(0, move.x * turnRate * deltaTime, 0, Space.World);
        if (!applyMotion || !body) return;
        verticalSpeed = body.isGrounded && verticalSpeed < 0 ? groundedForce : verticalSpeed + gravity * deltaTime;
        body.Move((transform.forward * model.SignedSpeed + Vector3.up * verticalSpeed) * deltaTime);
    }

    void CopySettings()
    {
        model.walkSpeed = walkSpeed; model.runSpeed = runSpeed; model.reverseSpeed = reverseSpeed; model.acceleration = acceleration; model.deceleration = deceleration; model.braking = braking;
        model.inputDeadZone = inputDeadZone; model.stopThreshold = stopThreshold; model.runEnterSpeed = runEnterSpeed; model.runExitSpeed = runExitSpeed;
    }
}
