# iOS UI Automation Skill

## Metadata

- Type: Workflow
- Use when: an agent needs to validate ANY iOS app's UI with Xcode — building to a simulator, capturing screenshots, driving the app through XCTest click-throughs, and visually verifying the result.
- Primary tools: `xcodebuild build` / `xcodebuild test`, `xcrun simctl`, XCTest UI tests, local screenshot inspection.
- Artifact policy: screenshots and `.xcresult` bundles are local QA artifacts; do not commit them.

This skill is **app-agnostic**. It describes the method; the per-app specifics (project path, scheme, bundle identifier, launch arguments, accessibility identifiers, and the flow that constitutes a passing run) are supplied by the caller. A project that uses this skill repeatedly should keep its own small "config" file enumerating those values and point back here for the method. (Example consumer config: `path/to/project/skills/ios_ui_automation_config.md`.)

## Goal

Produce reproducible evidence that an iOS app works visually and behaves correctly on a simulator, without exposing any private data (mail, endpoint URLs, bearer tokens, account names, local configuration). A successful run proves the relevant user flow through some combination of automated tests, targeted simulator interaction, screenshots, and an explicit read/verify pass over the captured UI state.

This skill is equally useful for **pure visual verification** — e.g. "did this design change actually render the way I intended?" — where you build, launch in a deterministic state, screenshot the screen under review, and inspect the image. You do not always need full XCTest assertions; for a visual-only check, a deterministic launch plus a screenshot plus a careful read is enough.

## Boundaries

This skill validates the iOS app surface only. It does not mutate any production backend except when the caller explicitly asks for live testing and the flow uses synthetic data. Default to deterministic UI-test / fixture mode.

Screenshots may contain visible private data. Keep them under an ignored path such as `tmp/visual_qa/`, inspect each capture before sharing, and never commit screenshots that show real user data, real endpoint URLs, tokens, or private account names.

## Per-App Inputs (caller supplies these)

Before running, gather the following for the target app. If the caller hasn't given them, discover them from the project (`xcodebuild -list`, the `.xcodeproj`, Info.plist) or ask:

- **Xcode project / workspace path** — e.g. `path/to/App.xcodeproj`
- **Scheme** — the buildable scheme name (`xcodebuild -list` enumerates them)
- **Bundle identifier** — for `simctl launch` / `terminate`
- **Simulator destination** — a `platform=iOS Simulator,name=<device>,OS=<version>` whose OS ≥ the app's deployment target
- **Deterministic launch arguments** — any flags that put the app into a fixture / UI-test state with synthetic data (so screenshots are public-safe and reproducible). If the app has none, note that and use the app's normal cold-launch state.
- **Accessibility identifiers** — the `tab.*` / `*.button` / `*.field` identifiers used to drive and assert the flow under review
- **The passing flow** — the minimal sequence of screens/actions that, if correct, means this run passes

A consumer project should freeze these into its own config file rather than rediscovering them each time.

## Acceptance Criteria

A UI automation run is complete when:

- `xcodebuild build` (visual-only) or `xcodebuild test` (behavioral) exits 0 for the chosen destination.
- For a behavioral run, the flow is covered with XCTest assertions or an equivalent deterministic click-through script.
- Any manual `simctl` launch uses deterministic / fixture arguments unless live testing was explicitly requested.
- Screenshots are captured for the screens under review and stored under `tmp/visual_qa/`.
- Each screenshot is inspected after capture for both visual correctness and privacy.
- The agent reports the simulator destination, the commands used, the screenshot paths, the test/build result, and any residual risk.

## Automation Surfaces

Use **XCTest UI tests** for repeatable interactions and rich assertions. They drive the app through accessibility identifiers that the caller supplies (e.g. `tab.<name>`, `<screen>.<control>`). Identifiers should be stable and semantic, not positional.

Use **`simctl`** for app installation, deterministic launches, and screenshots. `simctl` cannot express rich UI assertions on its own, so it is best for visual evidence — either after XCTest has proved the flow, or as the primary tool for a visual-only design check.

## Command Patterns

Discover schemes:

```bash
xcodebuild -list -project "<project>"
```

Run the full test suite (behavioral):

```bash
xcodebuild test \
  -project "<project>" \
  -scheme "<scheme>" \
  -destination 'platform=iOS Simulator,name=<device>,OS=<version>'
```

Build, install, launch deterministically, and capture a screenshot (visual-only):

```bash
xcodebuild build \
  -project "<project>" \
  -scheme "<scheme>" \
  -destination 'platform=iOS Simulator,name=<device>,OS=<version>'

# Resolve the actual built .app under DerivedData (globs don't expand inside quotes;
# prefer the newest product from the build you just ran).
xcrun simctl install "<device-uuid>" "<resolved-derived-data>/<App>.app"
xcrun simctl launch "<device-uuid>" <bundle-id> <deterministic-launch-args>
xcrun simctl io "<device-uuid>" screenshot "tmp/visual_qa/<screen>.png"
```

For full-page detail screenshots that exceed one viewport, prefer an in-test scroll-and-stitch helper over a single `io screenshot`, and consider a launch flag that hides the tab bar.

## Read/Verify Loop

After each screenshot, inspect the image before deciding the flow passed. The inspection should answer:

- Is this the intended screen, or did launch/navigation land somewhere else?
- Are the expected controls visible and enabled/disabled correctly?
- Does the specific visual change / issue under review look right?
- Does the screenshot contain only synthetic / public-safe data?
- Is there any simulator/system alert blocking the app?

If the answer is unclear, capture one more screen after a deterministic action rather than guessing from stale output.

## Known Failure Modes

- `App installation failed: Requires a Newer Version of iOS`: the selected simulator OS is below the deployment target. Pick a newer installed simulator. A booted simulator with an older OS is a bad target because install fails *after* the build already succeeded.
- `simctl screenshot` fails or prints usage: use `xcrun simctl io <device> screenshot <path>`. Recent Xcode versions route screenshots through `io`.
- Screenshot shows stale UI: terminate the app, reinstall the freshly built `.app`, relaunch with the deterministic arguments, and wait briefly before capture.
- UI test fails to launch an xctrunner once but the final result still says `TEST SUCCEEDED`: trust the final `xcodebuild` result and the test-case list, but rerun if the failed launch corresponds to the specific flow under review.
- Standalone SourceKit diagnostics report `No such module Testing` / `No such module XCTest`: use a target-aware `xcodebuild test` as the source of truth for test files, not standalone diagnostics.
- Screenshot contains real user data / real config: discard it, relaunch in deterministic/fixture mode, and do not share or commit the artifact.

## Live Testing

Live API testing is a separate mode. It may use a real backend only with synthetic data and explicit live-test arguments/environment. Do not capture screens that show real tokens or real user content; use tests or scripts that assert status and IDs without dumping sensitive bodies.
