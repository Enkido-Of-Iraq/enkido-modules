using NUnit.Framework;

public sealed class MountedLocomotionModelTests
{
    MountedLocomotionModel model;
    [SetUp] public void SetUp() => model = new MountedLocomotionModel();

    [Test] public void ForwardAcceleratesWithoutJumping()
    {
        model.Step(1, false, .1f);
        Assert.That(model.SignedSpeed, Is.GreaterThan(0).And.LessThan(model.walkSpeed));
        Assert.That(model.State, Is.EqualTo(MountedLocomotionState.Walking));
    }

    [Test] public void PartialInputUsesProportionalWalkTarget()
    {
        StepFor(.5f, false, 4);
        Assert.That(model.SignedSpeed, Is.EqualTo(model.walkSpeed * .5f).Within(.02f));
    }

    [Test] public void RunReleaseImmediatelyReturnsTargetStateToWalking()
    {
        StepFor(1, true, 3); Assert.That(model.State, Is.EqualTo(MountedLocomotionState.Running));
        model.Step(1, false, .02f); Assert.That(model.State, Is.EqualTo(MountedLocomotionState.Walking));
    }

    [Test] public void ReleaseStopsWithoutCrossingZero()
    {
        StepFor(1, false, 2); model.Step(0, false, .02f); Assert.That(model.State, Is.EqualTo(MountedLocomotionState.Stopping));
        StepFor(0, false, 2); Assert.That(model.SignedSpeed, Is.Zero); Assert.That(model.State, Is.EqualTo(MountedLocomotionState.Idle));
    }

    [Test] public void BackwardBrakesBeforeReverseAndHonorsLimit()
    {
        StepFor(1, false, 2); model.Step(-1, false, .1f); Assert.That(model.SignedSpeed, Is.GreaterThanOrEqualTo(0)); Assert.That(model.State, Is.EqualTo(MountedLocomotionState.Stopping));
        StepFor(-1, false, 3); Assert.That(model.SignedSpeed, Is.EqualTo(-model.reverseSpeed).Within(.02f)); Assert.That(model.State, Is.EqualTo(MountedLocomotionState.Reversing));
    }

    [Test] public void RunThresholdHysteresisPreventsFlicker()
    {
        StepFor(1, true, 3); Assert.That(model.State, Is.EqualTo(MountedLocomotionState.Running));
        model.Step(.42f, true, .05f); Assert.That(model.State, Is.EqualTo(MountedLocomotionState.Running));
    }

    void StepFor(float input, bool run, float seconds) { for (var t = 0f; t < seconds; t += .02f) model.Step(input, run, .02f); }
}
