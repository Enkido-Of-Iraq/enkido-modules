using UnityEngine;

[DisallowMultipleComponent]
public sealed class MountedAnimationPresenter : MonoBehaviour
{
    [SerializeField] MountedAnzuController controller; [SerializeField] Transform animatedRoot;
    [SerializeField] float walkReferenceSpeed = 3f, minimumCadence = .35f, maximumCadence = 1.65f, cadenceDamping = 6f;
    Animation[] animations; Vector3 restPosition; Quaternion restRotation; float cadence;
    void Awake()
    {
        if (!controller) controller = GetComponent<MountedAnzuController>(); if (!animatedRoot && controller) animatedRoot = controller.AnimatedRoot;
        if (animatedRoot) { restPosition = animatedRoot.localPosition; restRotation = animatedRoot.localRotation; }
        animations = GetComponentsInChildren<Animation>(true);
        foreach (var source in animations) { source.playAutomatically = false; foreach (AnimationState clip in source) clip.wrapMode = WrapMode.Loop; if (source.clip) source.Play(source.clip.name); }
    }
    void LateUpdate()
    {
        if (!controller) return; var moving = controller.LocomotionState != MountedLocomotionState.Idle;
        var desired = moving ? Mathf.Clamp(Mathf.Abs(controller.CurrentSpeed) / Mathf.Max(.01f, walkReferenceSpeed), minimumCadence, maximumCadence) : 0;
        cadence = Mathf.MoveTowards(cadence, desired, cadenceDamping * Time.deltaTime);
        foreach (var source in animations) foreach (AnimationState clip in source) clip.speed = controller.LocomotionState == MountedLocomotionState.Reversing ? -cadence : cadence;
        if (animatedRoot) { animatedRoot.localPosition = restPosition; animatedRoot.localRotation = restRotation; }
    }
}
