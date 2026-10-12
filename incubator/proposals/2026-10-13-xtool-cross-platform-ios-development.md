# xtool — Cross-platform iOS development without a Mac

- Date: 2026-10-13
- Source: https://github.com/xtool-org/xtool
- Status: KNOWLEDGE / future validation candidate
- Adoption: HOLD; no installation or implementation approved
- Evidence: official repository README and metadata reviewed 2026-10-13; not independently tested

## Why retain
The user develops on Windows/Linux and uses an iPhone. This may become useful for future iPhone app experiments even though there is no immediate implementation need.

## Verified project claims
xtool is an MIT-licensed cross-platform Xcode alternative for Swift Package Manager-based iOS apps. The README documents building iOS apps, signing and installing them on devices, launching installed apps, and interacting with Apple Developer Services. Its overview describes Linux/WSL/macOS; Windows generally uses WSL. The project requires Apple SDK/toolchain assets; it does not prove full Xcode compatibility or end-to-end App Store submission without macOS.

## Comparison / boundaries
- Alternative to or complement for macOS GitHub Actions runners, not an automatic replacement for every iOS project.
- First future experiment: Windows 11 + WSL2 + xtool + minimal SwiftPM/SwiftUI app; test build, signing, installation, and launch on an iPhone.
- Assess SDK acquisition/licensing, Apple Developer account requirements, iOS version support, WSL device connectivity, build reproducibility, maintenance, security and App Store distribution separately.
- Keep this in the Proposal Incubator for Obsidian semantic recall. No Core, Access, or workflow modifications.

## Recall triggers
Future iPhone application development, SwiftUI prototypes, Mac-free iOS builds, Codex-driven mobile development, Apple signing, GitHub Actions macOS runner alternatives.
