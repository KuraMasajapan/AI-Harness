# Mac.apk — Android app compatibility on Apple Silicon macOS

Date: 2026-10-25
Classification: A / CANDIDATE (technical research), IMPLEMENTATION HOLD
Scope: AI-Harness research only; no implementation or policy change.

## Sources
- X post: https://x.com/wlzh/status/2113807801449697354
- Primary source: https://github.com/kksimp/Mac.apk
- Documentation: https://github.com/kksimp/Mac.apk/wiki

## Verified facts from project README
- Mac.apk implements an Android application environment on macOS directly, without booting a Linux-based Android VM/emulator; ARM64 app code runs on Apple Silicon, with Mac GPU rendering.
- Requires Apple Silicon and macOS 26.4 or later; Alpha status.
- Maintainer's hand-tested compatibility list: 71 apps, 58 fully working, 10 partly, 3 not working. This is **not** a representative Android-wide compatibility percentage.
- AGPL-3.0 open-source license; official app free.
- **Critical security limitation:** Android apps under Mac.apk do not receive Android's normal app sandbox; they run with the current macOS user's permissions and may access files available to that account. Only run trusted APKs.
- Broad independent compatibility/performance/security audit not established by this research.

## Assessment
Technical interest: High. Direct fit to current Windows/Linux local AI-Harness: Low. Future relevance: OS compatibility layers, cross-platform AI-agent application interaction, isolation boundaries.
Main concern is not an observed compromise but the absence of Android-equivalent sandbox isolation. Running untrusted Android APKs can expand the host attack surface. No blanket claim that macOS itself lacks all protections.

## Architectural lesson for AI-Harness
Evaluate capabilities together with blast radius. Shell, filesystem, browser and external app execution must be treated as trust boundaries. Favor least privilege, sandbox/container or VM isolation where practical, scoped access, explicit Human approval for consequential operations, auditable logs and rollback. Evaluate whether a candidate can be made safe with isolation rather than permanently rejecting promising research on security grounds.

## Decision / Next check
A / CANDIDATE, implementation HOLD. No need to install Mac.apk. Reassess after credible sandboxing improvements, independent security review and wider app compatibility tests. Keep research separate from Core/Trinity rules and live projects.
