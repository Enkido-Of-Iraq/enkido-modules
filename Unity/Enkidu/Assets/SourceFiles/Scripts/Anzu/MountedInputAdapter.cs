using UnityEngine;
using UnityEngine.InputSystem;

[DisallowMultipleComponent]
public sealed class MountedInputAdapter : MonoBehaviour
{
    [SerializeField] PlayerInput playerInput;
    [SerializeField] string moveAction = "Move", lookAction = "Look", runAction = "Sprint";
    public Vector2 Move { get; private set; }
    public Vector2 Look { get; private set; }
    public bool RunHeld { get; private set; }
    public bool UsesInjectedInput { get; private set; }
    void Awake() { if (!playerInput) playerInput = GetComponent<PlayerInput>(); }
    void Update()
    {
        if (UsesInjectedInput || !playerInput || playerInput.actions == null) return;
        var move = playerInput.actions.FindAction(moveAction, false); var look = playerInput.actions.FindAction(lookAction, false); var run = playerInput.actions.FindAction(runAction, false);
        Move = move == null ? Vector2.zero : Vector2.ClampMagnitude(move.ReadValue<Vector2>(), 1); Look = look == null ? Vector2.zero : look.ReadValue<Vector2>(); RunHeld = run != null && run.ReadValue<float>() > .5f;
    }
    public void Inject(Vector2 move, Vector2 look, bool run) { UsesInjectedInput = true; Move = Vector2.ClampMagnitude(move, 1); Look = look; RunHeld = run; }
    public void ReleaseInjection() { UsesInjectedInput = false; Move = Look = Vector2.zero; RunHeld = false; }
}
