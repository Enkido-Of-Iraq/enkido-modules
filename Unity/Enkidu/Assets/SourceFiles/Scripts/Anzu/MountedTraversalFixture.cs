using System.Collections;
using System.Text;
using UnityEngine;

[DisallowMultipleComponent]
public sealed class MountedTraversalFixture : MonoBehaviour
{
    [SerializeField] MountedAnzuController controller; [SerializeField] MountedInputAdapter input; [SerializeField] bool runOnStart;
    public string LastReport { get; private set; }
    void Start() { if (runOnStart) StartCoroutine(RunSequence()); }
    public IEnumerator RunSequence()
    {
        var report = new StringBuilder("Mounted traversal fixture\n");
        yield return Phase("forward", new Vector2(0, 1), false, 2, report); yield return Phase("steer", new Vector2(.6f, 1), false, 1.5f, report); yield return Phase("run", new Vector2(0, 1), true, 2, report);
        yield return Phase("release", Vector2.zero, false, 2, report); yield return Phase("brake", new Vector2(0, -1), false, 1, report); yield return Phase("reverse", new Vector2(0, -1), false, 2, report);
        input.ReleaseInjection(); LastReport = report.ToString(); Debug.Log(LastReport, this);
    }
    IEnumerator Phase(string name, Vector2 move, bool run, float duration, StringBuilder report)
    {
        input.Inject(move, Vector2.zero, run); var elapsed = 0f; while (elapsed < duration) { elapsed += Time.deltaTime; yield return null; }
        report.Append(name).Append(": t=").Append(elapsed.ToString("F2")).Append(" position=").Append(controller.transform.position.ToString("F2")).Append(" speed=").Append(controller.CurrentSpeed.ToString("F2")).Append(" state=").Append(controller.LocomotionState).Append('\n');
    }
}
