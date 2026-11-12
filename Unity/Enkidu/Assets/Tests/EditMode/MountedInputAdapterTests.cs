using NUnit.Framework;
using UnityEngine;

public sealed class MountedInputAdapterTests
{
    [Test] public void DesktopAndMobileEquivalentValuesProduceIdenticalIntent()
    {
        var go = new GameObject("input test");
        try
        {
            var adapter = go.AddComponent<MountedInputAdapter>();
            var desktopMove = new Vector2(.3f, .9f); adapter.Inject(desktopMove, new Vector2(2, -1), true);
            var firstMove = adapter.Move; var firstLook = adapter.Look; var firstRun = adapter.RunHeld;
            adapter.ReleaseInjection(); adapter.Inject(desktopMove, new Vector2(2, -1), true);
            Assert.That(adapter.Move, Is.EqualTo(firstMove)); Assert.That(adapter.Look, Is.EqualTo(firstLook)); Assert.That(adapter.RunHeld, Is.EqualTo(firstRun));
            adapter.Inject(desktopMove, Vector2.zero, false); Assert.That(adapter.RunHeld, Is.False);
        }
        finally { Object.DestroyImmediate(go); }
    }
}
