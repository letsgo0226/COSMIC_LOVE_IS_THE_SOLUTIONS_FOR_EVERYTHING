command -v python3>/dev/null||{ echo python3_required;exit 127;};python3 bleem_riemann_info_zero_system.py verify-manifest "$@" < CURRENT_WINDOW_BLEEM_RIEMANN_MANIFEST.json
