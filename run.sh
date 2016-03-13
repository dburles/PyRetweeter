until "./retweeter.py"; do
    echo "PyRetweeter crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
