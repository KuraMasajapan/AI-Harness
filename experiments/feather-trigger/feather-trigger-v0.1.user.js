// ==UserScript==
// @name         Feather Trigger V0.1
// @namespace    AI-HARNESS
// @version      0.1.0
// @description  Inject activity_gap per conversation before ChatGPT user sends
// @match        https://chatgpt.com/*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    const STORAGE_PREFIX = 'feather:v0.1:last_user_message_at:c:';
    const DEDUPE_MS = 1000;

    let lastHandledAt = 0;

    function getConversationId() {
        const match = location.pathname.match(/\/c\/([^/?#]+)/);
        return match ? match[1] : null;
    }

    function getStorageKey() {
        const id = getConversationId();
        return id ? STORAGE_PREFIX + id : null;
    }

    function getComposer() {
        const el = document.querySelector('#prompt-textarea');

        if (!el) return null;

        const rect = el.getBoundingClientRect();

        if (rect.width <= 0 || rect.height <= 0) {
            return null;
        }

        return el;
    }

    function formatGap(ms) {
        const totalSeconds = Math.max(0, Math.floor(ms / 1000));

        if (totalSeconds < 60) {
            return `${totalSeconds}s`;
        }

        const totalMinutes = Math.floor(totalSeconds / 60);

        if (totalMinutes < 60) {
            return `${totalMinutes}m`;
        }

        const totalHours = Math.floor(totalMinutes / 60);

        if (totalHours < 24) {
            const minutes = totalMinutes % 60;
            return minutes
                ? `${totalHours}h ${minutes}m`
                : `${totalHours}h`;
        }

        const days = Math.floor(totalHours / 24);
        const hours = totalHours % 24;

        return hours
            ? `${days}d ${hours}h`
            : `${days}d`;
    }

    function createBadge() {
        const old = document.getElementById('feather-v01-badge');
        if (old) old.remove();

        const badge = document.createElement('div');
        badge.id = 'feather-v01-badge';

        Object.assign(badge.style, {
            position: 'fixed',
            right: '12px',
            bottom: '12px',
            zIndex: '999999',
            padding: '8px 12px',
            borderRadius: '8px',
            background: '#222',
            color: '#fff',
            fontSize: '12px',
            fontFamily: 'sans-serif',
            boxShadow: '0 2px 8px rgba(0,0,0,0.25)'
        });

        document.body.appendChild(badge);
        return badge;
    }

    const badge = createBadge();

    function setStatus(text) {
        badge.textContent = `Feather: ${text}`;
    }

    function composerText(composer) {
        return (composer.textContent || '').trim();
    }

    function putCaretAtStart(el) {
        const walker = document.createTreeWalker(
            el,
            NodeFilter.SHOW_TEXT
        );

        const firstTextNode = walker.nextNode();
        const range = document.createRange();

        if (firstTextNode) {
            range.setStart(firstTextNode, 0);
            range.collapse(true);
        } else {
            range.selectNodeContents(el);
            range.collapse(true);
        }

        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
    }

    function injectGap(composer, gapText) {
        const marker = `[activity_gap: ${gapText}]`;

        if (composerText(composer).startsWith('[activity_gap:')) {
            return true;
        }

        composer.focus();
        putCaretAtStart(composer);

        return document.execCommand(
            'insertText',
            false,
            marker + '\n'
        );
    }

    function handleSend(source) {
        const now = Date.now();

        if (now - lastHandledAt < DEDUPE_MS) {
            return;
        }

        const composer = getComposer();
        if (!composer) return;

        const text = composerText(composer);
        if (!text) return;

        const key = getStorageKey();

        if (!key) {
            setStatus(`${source} / NO CONVERSATION ID`);
            return;
        }

        lastHandledAt = now;

        const previousRaw = localStorage.getItem(key);
        const previous = previousRaw ? Number(previousRaw) : null;

        if (previous && Number.isFinite(previous)) {
            const gapText = formatGap(now - previous);

            const injected = injectGap(composer, gapText);

            if (!injected) {
                setStatus(`${source} / INJECTION FAILED`);
                return;
            }

            setStatus(`${source} / GAP ${gapText}`);
        } else {
            setStatus(`${source} / FIRST SEND`);
        }

        localStorage.setItem(key, String(now));

        console.log('[Feather Trigger]', {
            source,
            conversationId: getConversationId(),
            previous,
            now
        });
    }

    document.addEventListener(
        'keydown',
        (event) => {
            if (event.key !== 'Enter') return;

            const composer = getComposer();
            if (!composer || !composer.contains(event.target)) return;

            if (event.shiftKey) return;
            if (event.isComposing || event.keyCode === 229) return;

            handleSend('ENTER');
        },
        true
    );

    document.addEventListener(
        'click',
        (event) => {
            const target = event.target;
            if (!(target instanceof Element)) return;

            const button = target.closest(
                'button[data-testid="send-button"]'
            );

            if (!button) return;

            handleSend('BUTTON');
        },
        true
    );

    setStatus('READY');
})();
