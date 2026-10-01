# Doomsday CTF — Web Challenges (Flask)

Four complete, runnable web challenges, all different styles, Doom / Doomsday
themed. Each ships an `app.py`, Dockerfile, and a private `SOLUTION.md`.

| # | Name | Difficulty | Style | Port | Flag |
|---|------|-----------|-------|------|------|
| 1 | **Doom's Vault** | Medium | client-side RE + stego + lore | 5000 | `DOOM{v1ct0r_h0lds_th3_c0smic_k3y}` |
| 2 | **The Time Heist** | Medium | race condition (TOCTOU) | 5001 | `DOOM{r4c1ng_th3_t1m3str34m_b34ts_d00m}` |
| 3 | **The Latverian Signet** | Medium-Hard | Flask session forgery (crypto/auth) | 5002 | `DOOM{th3_s0v3r31gn_s34l_w4s_f0rg3d}` |
| 4 | **Incursion Scanner** | Medium-Hard | SSRF -> internal, 2-hop chain | 5003 | `DOOM{ssrf_thr0ugh_th3_mult1v3rs3_t0_th3_c0r3}` |

Set a fresh `FLAG` per event via the env var in each Dockerfile.

## Player-facing descriptions (challenges 3 & 4)

**The Latverian Signet** -- Web -- Medium-Hard
> Every citizen of Latveria is issued a royal signet the moment they arrive, and
> the Crown insists it cannot be forged. But the throne room, where Doom's final
> Doomsday decree is sealed, admits only the Sovereign himself. The Crown has grown
> careless; its seal has not been changed since the day Doom took power. Become the
> Sovereign.  ->  http://YOUR_IP:5002

**Incursion Scanner** -- Web -- Medium-Hard
> The TVA's scanner probes parallel universes for timeline bleed before Doom
> collapses them all. It will relay to any universe you point it at, any universe
> except the ones it has been told to protect. Somewhere behind that shield sits
> the Sacred Timeline Core, and it has no guard of its own. Reach it.
> ->  http://YOUR_IP:5003

Keep technique words (stego, race, SSRF, cookie) out of player text so the leap stays theirs.

## On AI-resistance
No web challenge is truly AI-proof. These target what models are weakest at in
practice:
- Vault - flag/fragment kept out of the client; gated by stego + an oblique
  Marvel-lore passphrase (Valeria).
- Time Heist - no logic solve; only a landed race wins.
- Signet - blind cracking fails (secret not in any wordlist); you must read and
  synthesise two clues scattered across the site and commit to one exact value.
- Incursion Scanner - the friction is the chain: find the hidden port, pick a
  working loopback bypass, adapt to a second hop revealed only at runtime.

Each SOLUTION.md lists knobs to push further toward human-only.

## Run
    # local
    cd challengeN_* && pip install -r requirements.txt && python app.py
    # docker
    cd challengeN_* && docker build -t <name> . && docker run -p <port>:<port> <name>

For Incursion Scanner publish ONLY 5003 - never -p 9000:9000.

## Hand out vs keep private
- Give players: the URL (+ the sigil image for Vault, optional).
- Keep private: every SOLUTION.md and solve_example.py.
